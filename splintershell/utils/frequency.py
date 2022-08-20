"""Utilities for frequency distributions"""
import numpy as np

from splintershell.errors import InvalidFreqDistError


def ascii_to_int(text: str) -> list:
    return [ord(char) for char in text]


def freq_dist(samples: list) -> np.ndarray:
    return np.array(
        [
            np.bincount(np.array(ascii_to_int(sample)), minlength=256)
            for sample in samples
        ]
    )


def ascii_freq_dict(dist: np.ndarray) -> dict:
    if not isinstance(dist, np.ndarray) and len(dist.shape) != 1:
        raise InvalidFreqDistError(
            f"Frequency distribution provided is not a 1-dimensional NumPy array"
        )

    return dict(zip([char for char in range(len(dist))], dist))
