import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .lib.constants import DEFAULT_SAMPLE_RATIO
from .lib.protocol import protocols
from .lib.util import shuffle_and_split
from .payl.payl import Payl


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(
        prog="train",
        description="train a PAYL model",
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

    return parser.parse_args()


def validate_args(opts: Namespace) -> int:
    try:
        assert Path(opts.directory).is_dir()
    except AssertionError:
        logging.error(
            f"Directory does not exist: {str(Path(opts.directory).resolve())}"
        )
        return 1

    try:
        assert protocols.get(opts.protocol, None)
    except AssertionError:
        logging.error(f"Protocol specified not supported: {opts.protocol}")
        return 1

    try:
        assert opts.sample_ratio < 1.0
        assert opts.sample_ratio > 0.0
    except AssertionError:
        logging.error(f"Sample ratio should range from 0.0 to 1.0: {opts.sample_ratio}")

    return 0


def main() -> int:
    opts = get_parsed_args()
    if validate_args(opts):
        return 1

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

    training_data, test_data = shuffle_and_split(
        data=protocol_data, split_ratio=opts.sample_ratio
    )

    model = Payl(smoothing_factor=3, classification_threshold=20, discrete_steps=10)
    model.train(training_data=training_data, test_data=test_data)

    return 0
