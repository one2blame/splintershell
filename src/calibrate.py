import json
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .lib.constants import (
    CONVERGENCE_CONSTANT,
    DEFAULT_DISCOUNT_RATE,
    DEFAULT_DISTANCE_STEP,
    DEFAULT_DISTANCE_VECTOR,
    DEFAULT_LEARNING_RATE,
    DEFAULT_NUMBER_OF_BUCKETS,
    DEFAULT_RANDOM_ACTION_DECAY_RATE,
    DEFAULT_RANDOM_ACTION_RATE,
    DEFAULT_SAMPLE_RATIO,
    DEFAULT_SMOOTHING_FACTOR,
    MAX_EPOCHS,
    MAX_SAMPLE_RATIO,
    MIN_SAMPLE_RATIO,
    PAYL_METADATA_KEY,
)
from .lib.protocol import protocols
from .lib.qlearner import QLearner
from .lib.util import shuffle_and_split
from .lib.payl import Payl


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(
        prog="calibrate",
        description="train a PAYL model, calibrating it to provided packet captures",
    )
    parser.add_argument(
        "--protocol",
        "-p",
        dest="protocol",
        type=str.lower,
        required=True,
        help="specify protocol to train PAYL model on",
    )
    parser.add_argument(
        "--directory",
        "-d",
        dest="directory",
        required=True,
        help="directory containing training data",
    )
    parser.add_argument(
        "--sample-ratio",
        "-s",
        dest="sample_ratio",
        type=float,
        default=DEFAULT_SAMPLE_RATIO,
        help=f"specify the ratio of training to testing data, default: {DEFAULT_SAMPLE_RATIO}",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        type=str,
        default=f"{Path.joinpath(Path.cwd(), 'payl')}-{int(time.time())}.json",
        help="output file for trained PAYL model",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="verbose",
        action="store_true",
        default=False,
        help=f"print verbose output",
    )

    return parser.parse_args()


def validate_args(opts: Namespace) -> int:
    try:
        assert Path(opts.directory).is_dir()
    except AssertionError:
        print(f"Directory does not exist: {str(Path(opts.directory).resolve())}")
        return 1

    try:
        assert protocols.get(opts.protocol, None)
    except AssertionError:
        print(f"Protocol specified not supported: {opts.protocol}")
        return 1

    try:
        assert opts.sample_ratio < MAX_SAMPLE_RATIO
        assert opts.sample_ratio > MIN_SAMPLE_RATIO
    except AssertionError:
        print(f"Sample ratio should range from 0.0 to 1.0: {opts.sample_ratio}")

    return 0


def main() -> int:
    opts = get_parsed_args()
    if validate_args(opts):
        return 1

    if opts.verbose:
        print(f"Acquiring packet capture data from ({opts.directory})...")

    protocol_parser = protocols.get(opts.protocol, None)
    protocol_parsers = [
        protocol_parser(filepath=filepath)  # type: ignore
        for filepath in Path(opts.directory).iterdir()
    ]

    protocol_data = []
    for parser in protocol_parsers:
        parser.parse_pcap()
        for entry in parser.get_parsed_pcap():
            protocol_data.append(entry)

    if opts.verbose:
        print(f"Packet capture data retrieved for protocol ({opts.protocol})!")

    training_data, testing_data = shuffle_and_split(
        data=protocol_data, split_ratio=opts.sample_ratio
    )

    model = Payl(discrete_steps=DEFAULT_NUMBER_OF_BUCKETS, verbose=opts.verbose)
    model.train(training_data=training_data)

    if opts.verbose:
        print(
            f"Testing the trained PAYL model against ({len(testing_data)}) testing data elements..."
        )
        print(f"Using reinforcement learning to tune classification threshold...")

    distances = DEFAULT_DISTANCE_VECTOR
    qlearner = QLearner(
        num_states=(2 * len(distances)),
        num_actions=2,
        alpha=DEFAULT_LEARNING_RATE,
        gamma=DEFAULT_DISCOUNT_RATE,
        rar=DEFAULT_RANDOM_ACTION_RATE,
        radr=DEFAULT_RANDOM_ACTION_DECAY_RATE,
        dyna=0,
        verbose=opts.verbose,
    )

    action = 0
    distances_index = 0
    converged = 0
    prev_reward = 0
    classification_threshold = distances[distances_index] * DEFAULT_DISTANCE_STEP
    for epoch in range(MAX_EPOCHS):
        state = int(str(f"{action}{distances[distances_index] - 1}"))

        reward = 0.0
        classification_threshold = distances[distances_index] * DEFAULT_DISTANCE_STEP
        if epoch == 0:
            action = qlearner.querysetstate(s=state)
        else:
            reward = model.test(
                smoothing_factor=DEFAULT_SMOOTHING_FACTOR / 10,
                classification_threshold=classification_threshold,
                testing_data=testing_data,
            )
            action = qlearner.query(s_prime=state, r=reward)

        curr_reward = int(reward)
        if curr_reward == prev_reward:
            converged += 1
            if converged > CONVERGENCE_CONSTANT:
                if opts.verbose:
                    print("Classification threshold has reached convergence!")
                break
        else:
            converged = 0
            prev_reward = curr_reward

        if action == 0:
            if distances_index + 1 < len(distances):
                distances_index += 1
        elif action == 1:
            if distances_index > 0:
                distances_index -= 1
        else:
            print(f"Unknown action ({action}) provided!")
            return 1

        if opts.verbose:
            print(f"Current classification threshold: ({classification_threshold})")

    if opts.verbose:
        print(
            f"Discovered classification threshold for provided packet captures: ({classification_threshold})"
        )

    print(f"Writing trained PAYL model to: {opts.output}")
    with Path(opts.output).open(mode="w") as output_file:
        for threshold, feature_vector in model.feature_vectors.items():
            model.feature_vectors[threshold] = feature_vector.tolist()
        model.feature_vectors[PAYL_METADATA_KEY] = (  # type: ignore
            DEFAULT_SMOOTHING_FACTOR,
            classification_threshold,
            opts.protocol,
        )
        output_file.write(json.dumps(model.feature_vectors))

    return 0
