from argparse import ArgumentParser, Namespace
from pathlib import Path

from .lib.payl import Payl
from .lib.protocol import protocols


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(
        prog="test",
        description="test data against a calibrated PAYL model",
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
        "--model",
        "-m",
        dest="model",
        required=True,
        help="JSON file containing calibrated PAYL model",
    )
    parser.add_argument(
        "--input",
        "-i",
        dest="input",
        required=True,
        help="data file to test against calibrated PAYL model",
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
        assert Path(opts.model).exists()
    except AssertionError:
        print(f"Model file does not exist: {str(Path(opts.model).resolve())}")
        return 1

    try:
        assert Path(opts.input).exists()
    except AssertionError:
        print(f"Input file does not exist: {str(Path(opts.input).resolve())}")
        return 1

    try:
        assert protocols.get(opts.protocol, None)
    except AssertionError:
        print(f"Protocol specified not supported: {opts.protocol}")
        return 1

    return 0


def main() -> int:
    opts = get_parsed_args()
    if validate_args(opts):
        return 1

    calibrated_thresholds, protocol, bucket_sizes, feature_vectors = Payl.parse_model(
        model_file=Path(opts.model).resolve()
    )

    if protocol != opts.protocol:
        print(
            f"Protocol provided ({opts.protocol}) doesn't match input file protocol: ({protocol})!"
        )
        return 1

    model = Payl(discrete_steps=len(bucket_sizes), verbose=opts.verbose)
    model.bucket_sizes = bucket_sizes
    model.feature_vectors = feature_vectors

    if opts.verbose:
        print(f"Reading input data file...")
    with Path(opts.input).resolve().open("rb") as input_file:
        input_data = [input_file.read().decode("utf8")]

    print(
        model.test(
            classification_thresholds=calibrated_thresholds,
            testing_data=input_data,
        )
    )

    return 0
