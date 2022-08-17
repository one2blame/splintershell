"""Functions to train Gaussian mixture models on packet captures and test shellcodes"""
from pathlib import Path

import numpy as np
from sklearn.mixture import GaussianMixture

from splintershell.errors import (
    NonexistentShellcodeFileError,
    NonexistentTrainingDirectoryError,
    UnfitModelError,
    UnsupportedProtocolError,
)
from splintershell.protocols import protocol_dict

from .utils import freq_dist


def train_model(
    training_dirname: str, protocol: str, verbose: bool = False
) -> GaussianMixture:
    try:
        assert Path(training_dirname).is_dir()
    except AssertionError:
        raise NonexistentTrainingDirectoryError(
            f"Training directory does not exist: {str(Path(training_dirname).resolve())}"
        )

    try:
        protocol_parser = protocol_dict.get(protocol, None)
        assert protocol_parser is not None
    except AssertionError:
        raise UnsupportedProtocolError(f"Protocol specified not supported: {protocol}")

    if verbose:
        print(
            f"Acquiring packet capture data from ({Path(training_dirname).resolve()})..."
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
        print(f"Packet capture data retrieved for protocol ({protocol})!")

    model = GaussianMixture(verbose=int(verbose))
    model.fit(X=freq_dist(samples=protocol_data))

    if verbose:
        print(
            f"splintershell Gaussian mixture model successfully trained on {len(protocol_data)} samples"
        )

    return model


def test_distance(shellcode_file: str, model: GaussianMixture) -> float:
    try:
        assert Path(shellcode_file).exists()
    except AssertionError:
        raise NonexistentShellcodeFileError(
            f"Shellcode file does not exist: {str(Path(shellcode_file).resolve())}"
        )

    try:
        assert model.converged_
    except AssertionError:
        raise UnfitModelError(f"Model provided has not been fit to training data")

    with Path(shellcode_file).open(mode="rb") as shellcode:
        sample = str("".join(map(chr, shellcode.read())))

    model_means = model.means_[0]
    norm_mean = model_means / np.sum(model_means)
    sample_freq_dist = freq_dist(samples=[sample])[0]
    norm_sample = sample_freq_dist / np.sum(sample_freq_dist)

    return np.linalg.norm(norm_mean - norm_sample, axis=0)
