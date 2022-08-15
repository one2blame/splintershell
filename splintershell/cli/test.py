"""Testing program for splintershell CLI"""
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path

from sklearn.mixture import GaussianMixture

from splintershell import learning
from splintershell.errors import InvalidPickledObjectError, NonexistentModelFileError


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

    try:
        assert Path(opts.model).exists()
    except AssertionError:
        raise NonexistentModelFileError(
            f"Model file does not exist: {str(Path(opts.model).resolve())}"
        )

    with Path(opts.model).resolve().open(mode="rb") as model_file:
        model = pickle.load(model_file)

    try:
        assert isinstance(model, GaussianMixture)
    except AssertionError:
        raise InvalidPickledObjectError(
            f"Pickled object provided is not a Gaussian mixture model: {str(Path(opts.model).resolve())}"
        )

    likelihood = learning.test_likelihood(shellcode_file=opts.input, model=model)
    print(
        f"Log-likelihood of sample existing within provided distribution: {likelihood}"
    )

    return 0
