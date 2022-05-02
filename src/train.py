import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .lib.constants import DEFAULT_SAMPLE_RATIO
from .lib.protocol import protocols


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

    return 0


def main() -> int:
    opts = get_parsed_args()
    if validate_args(opts):
        return 1

    protocol_parsers = [
        opts.protocol(filepath=filepath) for filepath in Path(opts.directory).iterdir()
    ]

    protocol_data = []
    for parser in protocol_parsers:
        parser.parse_pcap()
        protocol_data.append(parser.get_parsed_pcap())
    # TODO remove
    print(protocol_data)

    return 0
