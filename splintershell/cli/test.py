"""Testing program for splintershell CLI"""
from argparse import ArgumentParser, Namespace

from splintershell import learning

from .utils import verify_model


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
    model = verify_model(model_filename=opts.model)
    distance = learning.test_distance(shellcode_file=opts.input, model=model)
    print(
        f"Distance of sample's frequency distribution (normalized) from model mean (normalized): {distance}"
    )

    return 0
