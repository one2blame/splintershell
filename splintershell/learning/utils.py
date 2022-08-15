"""Common model training and testing utilities"""
import numpy as np


def ascii_to_int(text: str) -> list:
    return [ord(char) for char in text]


def freq_dist(samples: list) -> np.ndarray:
    return np.array(
        [
            np.bincount(np.array(ascii_to_int(sample)), minlength=256)
            for sample in samples
        ]
    )
