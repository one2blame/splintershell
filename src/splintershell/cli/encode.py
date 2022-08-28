"""Encoding program for splintershell CLI"""
import pickle
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from splintershell.encoding import blend_shellcode


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
        "--scheme",
        "-s",
        dest="scheme",
        type=str.lower,
        default="xor",
        help="shellcode encoding scheme",
    )
    parser.add_argument(
        "--padding",
        "-p",
        dest="padding",
        action="store_true",
        default=False,
        help="pad shellcode to fit model size, if necessary",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="verbose",
        action="store_true",
        default=False,
        help="print verbose output",
    )
    return parser.parse_args()


def main() -> int:
    opts = get_parsed_args()

    with Path(opts.model).resolve().open(mode="rb") as model_file:
        model = pickle.load(model_file)

    with Path(opts.input).resolve().open(mode="rb") as shellcode_file:
        shellcode = shellcode_file.read()

    with Path(opts.output).resolve().open("wb") as output_file:
        output_file.write(
            blend_shellcode(
                shellcode=shellcode,
                model=model,
                scheme=opts.scheme,
                padding=opts.padding,
                verbose=opts.verbose,
            )
        )
        print(f"Encoded shellcode written to: {Path(opts.output).resolve()}")

    return 0
