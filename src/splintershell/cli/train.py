"""Training program for splintershell CLI"""
import pickle
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from splintershell.learning import train_model


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(
        prog="train", description="train a model on packet captures"
    )
    parser.add_argument(
        "--protocol",
        "-p",
        dest="protocol",
        type=str.lower,
        required=True,
        help="specify protocol to train model on",
    )
    parser.add_argument(
        "--directory",
        "-d",
        dest="directory",
        required=True,
        help="directory containing packet captures",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        type=str,
        default=f"{Path.joinpath(Path.cwd(), 'splintershell-model')}-{int(time.time())}.pickle",
        help="output file for pickled, trained model",
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

    with Path(opts.output).resolve().open(mode="wb") as output_file:
        pickle.dump(
            obj=train_model(
                training_dirname=opts.directory,
                protocol=opts.protocol,
                verbose=opts.verbose,
            ),
            file=output_file,
            protocol=pickle.HIGHEST_PROTOCOL,
        )
        print(f"splintershell model written to: {Path(opts.output).resolve()}")

    return 0
