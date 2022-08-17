"""Encoding program for splintershell CLI"""
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from splintershell import encoding

from .utils import verify_model


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(
        prog="encode", description="encode shellcode against a trained model"
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
        "--output",
        "-o",
        dest="output",
        type=str,
        default=f"{Path.joinpath(Path.cwd(), 'encoded-shellcode')}-{int(time.time())}.bin",
        help="output file for encoded shellcode",
    )
    parser.add_argument(
        "--model",
        "-m",
        dest="model",
        type=str,
        required=True,
        help="pickled, trained model input file",
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


def main() -> int:
    opts = get_parsed_args()
    model = verify_model(model_filename=opts.model)
    with Path(opts.output).open("wb") as output_file:
        output_file.write(
            encoding.blend_shellcode(shellcode_file=opts.input, model=model)
        )
    if opts.verbose:
        print(f"Encoded shellcode written to: {Path(opts.output).resolve()}")

    return 0
