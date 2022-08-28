"""Functions to train Gaussian mixture models on packet captures and test shellcodes"""
from pathlib import Path
from typing import Tuple

import numpy as np
from loguru import logger
from sklearn.mixture import GaussianMixture

from splintershell.common import freq_dist
from splintershell.errors import (
    InvalidModelObjectError,
    InvalidTrainingDirectoryError,
    UnsupportedProtocolError,
)
from splintershell.protocols import protocol_dict


def train_model(
    training_dirname: str, protocol: str, verbose: bool = False
) -> GaussianMixture:
    """Trains a Gaussian Mixture Model on specified protocol data for packet
    captures contained in a training directory.

    :param training_dirname: A directory of packet capture files (.pcap)
    :type training_dirname: str
    :raises InvalidTrainingDirectoryError: An exception raised if the training
    directory does not exist
    :param protocol: A protocol
    :type protocol: str
    :raises UnsupportedProtocolError: An exception raised if the protocol
    provided is not supported by splintershell
    :param verbose: Enable verbose output
    :type verbose: bool
    :return: A trained GaussianMixture object
    :rtype: GaussianMixture
    """
    if not Path(training_dirname).is_dir():
        raise InvalidTrainingDirectoryError(
            f"Training directory does not exist: {Path(training_dirname).resolve()}"
        )

    protocol_parser = protocol_dict.get(protocol, None)
    if protocol_parser is None:
        raise UnsupportedProtocolError(f"Protocol specified not supported: {protocol}")

    if verbose:
        logger.info(
            f"Parsing [{protocol}] packet capture data from ({Path(training_dirname).resolve()})..."
        )

    protocol_parsers = [
        protocol_parser(filepath=filepath)  # type: ignore
        for filepath in Path(training_dirname).iterdir()
    ]

    protocol_data = []
    for parser in protocol_parsers:
        parser.parse_pcap()
        for entry in parser.get_parsed_pcap():
            protocol_data.append(entry)

    if verbose:
        logger.success(
            f"Parsed {len(protocol_data)} [{protocol}] samples from packet capture data!"
        )
        logger.info("Training a Gaussian mixture model...")

    model = GaussianMixture(verbose=int(verbose))
    model.fit(X=freq_dist(samples=protocol_data))

    if verbose:
        logger.success(
            f"Gaussian mixture model trained on {len(protocol_data)} [{protocol}] samples!"
        )

    return model


def get_distance(shellcode: bytes, model: GaussianMixture) -> Tuple[float, float]:
    """Calculates the distance of a shellcode sample from the mean value of a
    single-cluster, trained Gaussian Mixture Model.

    :param shellcode: A sample shellcode for inspection
    :type shellcode: bytes
    :param model: A single-cluster, trained GaussianMixture
    :type model: GaussianMixture
    :return: A tuple of distance, and size difference between the shellcode and
    GMM cluster mean
    :rtype: Tuple[float, float]
    """
    if not isinstance(model, GaussianMixture):
        raise InvalidModelObjectError("Model provided is not a GaussianMixture")

    if not model.converged_:
        raise InvalidModelObjectError("Model provided has not been trained")

    model_means = model.means_[0]
    norm_mean = model_means / np.sum(model_means)
    sample = str("".join(map(chr, shellcode)))
    sample_freq_dist = freq_dist(samples=[sample])[0]
    norm_sample = sample_freq_dist / np.sum(sample_freq_dist)

    return np.linalg.norm(norm_mean - norm_sample, axis=0), np.sum(
        sample_freq_dist
    ) - np.sum(model_means)
