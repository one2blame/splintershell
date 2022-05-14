import json
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

import numpy as np

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
)
from .lib.protocol import protocols
from .lib.qlearner import QLearner
from .lib.util import shuffle_and_split
from .payl.payl import Payl


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

    print(f"{Payl.parse_model(model_file=Path(opts.model).resolve())}")

    return 0
