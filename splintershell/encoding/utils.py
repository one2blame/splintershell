import numpy as np

from splintershell.errors import InvalidFreqDistError


def freq_dict(freq_dist: np.ndarray) -> dict:
    try:
        assert isinstance(freq_dist, np.ndarray) and len(freq_dist.shape) == 1
    except AssertionError:
        raise InvalidFreqDistError(
            f"Frequency distribution provided is not a 1-dimensional NumPy array"
        )

    return dict(zip([char for char in range(256)], freq_dist))
