"""Common model training and testing utilities"""
import numpy as np

from splinter_shell.errors import UnsupportedProtocolError
from splinter_shell.protocols import protocol_dict


def ascii_to_int(text: str) -> list:
    return [ord(char) for char in text]


def freq_dist(samples: list) -> np.ndarray:
    return np.array(
        [
            np.bincount(np.array(ascii_to_int(sample)), minlength=256)
            / np.sum(ascii_to_int(sample))
            for sample in samples
        ]
    )


def get_protocol_parser(protocol: str):
    try:
        protocol_parser = protocol_dict.get(protocol, None)
        assert protocol_parser is not None
    except AssertionError:
        raise UnsupportedProtocolError(f"Protocol specified not supported: {protocol}")

    return protocol_parser
