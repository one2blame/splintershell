"""Testing program for splintershell CLI"""
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path

from splintershell.learning import get_distance


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(
        prog="test", description="test shellcode against a trained model"
    )
    parser.add_argument(
        "--input",
        "-i",
        dest="input",
        type=str,
        required=True,
        help="shellcode input file",
    )
    parser.add_argument(
        "--model",
        "-m",
        dest="model",
        type=str,
        required=True,
        help="pickled, trained model input file",
    )
    return parser.parse_args()


def main() -> int:
    opts = get_parsed_args()

    with Path(opts.model).resolve().open(mode="rb") as model_file:
        model = pickle.load(model_file)

    with Path(opts.input).resolve().open(mode="rb") as shellcode_file:
        shellcode = shellcode_file.read()

    distance, size_diff = get_distance(shellcode=shellcode, model=model)

    print(
        f"Distance of shellcode's frequency distribution (normalized) from model mean (normalized): {distance}"
    )
    print(f"Size difference between shellcode and model mean: {size_diff}")

    return 0
