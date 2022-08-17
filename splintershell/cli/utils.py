import pickle
from pathlib import Path

from sklearn.mixture import GaussianMixture

from splintershell.errors import InvalidPickledObjectError, NonexistentModelFileError


def verify_model(model_filename: str) -> GaussianMixture:
    try:
        assert Path(model_filename).exists()
    except AssertionError:
        raise NonexistentModelFileError(
            f"Model file does not exist: {str(Path(model_filename).resolve())}"
        )

    with Path(model_filename).resolve().open(mode="rb") as model_file:
        model = pickle.load(model_file)

    try:
        assert isinstance(model, GaussianMixture)
    except AssertionError:
        raise InvalidPickledObjectError(
            f"Pickled object provided is not a Gaussian mixture model: {str(Path(model_filename).resolve())}"
        )

    return model
