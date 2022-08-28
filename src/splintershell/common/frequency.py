"""Utilities for frequency distributions"""
from typing import Dict, List

import numpy as np

from splintershell.errors import InvalidFreqDistError


def ascii_to_int(text: str) -> List[int]:
    """Converts a string to a list of integer, ascii character values.

    :param text: A string
    :type text: str
    :return: A list of integer, ascii character values for each char in text
    :rtype: List[int]
    """
    return [ord(char) for char in text]


def freq_dist(samples: List[str]) -> np.ndarray:
    """Converts a list of strings to a list of integer, ascii character value
    frequency distributions for each string.

    :param samples: A list of strings
    :type samples: List[str]
    :return: A NumPy 2-dimensional array containing a frequency distribution for
    each string in samples
    :rtype: numpy.ndarray
    """
    return np.array(
        [
            np.bincount(np.array(ascii_to_int(sample)), minlength=256)
            for sample in samples
        ]
    )


def ascii_freq_dict(dist: np.ndarray) -> Dict[int, float]:
    """Converts a 1-dimensional NumPy array representing a frequency
    distribution to a mapping of integer, ascii character values to respective
    frequency distributions.

    :param dist: 1-dimensional NumPy array representing a frequency distribution
    :type dist: numpy.ndarray
    :return: A dictionary mapping of integer, ascii character values to
    frequency distributions
    :rtype: Dict[int, float]
    """
    if not isinstance(dist, np.ndarray) and len(dist.shape) != 1:
        raise InvalidFreqDistError(
            "Frequency distribution provided is not a 1-dimensional NumPy array"
        )

    return dict(zip([char for char in range(len(dist))], dist))
