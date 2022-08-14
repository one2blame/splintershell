"""Functions to operate on packet captures and Gaussian mixture models"""

from pathlib import Path

from sklearn.mixture import GaussianMixture

from splinter_shell.errors import (
    NonexistentTestingSampleError,
    NonexistentTrainingDirectoryError,
    UnfitModelError,
)

from .utils import freq_dist, get_protocol_parser


def train_model(
    training_directory: str, protocol: str, verbose: bool = False
) -> GaussianMixture:
    try:
        assert Path(training_directory).is_dir()
    except AssertionError:
        raise NonexistentTrainingDirectoryError(
            f"Training directory does not exist: {str(Path(training_directory).resolve())}"
        )

    protocol_parser = get_protocol_parser(protocol=protocol)

    if verbose:
        print(f"Acquiring packet capture data from ({training_directory})...")

    protocol_parsers = [
        protocol_parser(filepath=filepath)  # type: ignore
        for filepath in Path(training_directory).iterdir()
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
            f"splinter_shell Gaussian mixture model successfully trained on {len(protocol_data)} samples"
        )

    return model


def test_sample(
    testing_sample: str, protocol: str, model: GaussianMixture, verbose: bool = False
):
    try:
        assert Path(testing_sample).exists()
    except AssertionError:
        raise NonexistentTestingSampleError(
            f"Testing sample does not exist: {str(Path(testing_sample).resolve())}"
        )

    protocol_parser = get_protocol_parser(protocol=protocol)

    try:
        assert model.converged_
    except AssertionError:
        raise UnfitModelError(f"Model provided has not been fit to training data")

    if verbose:
        print(f"Acquiring packet capture data from ({testing_sample})...")

    protocol_data = [
        entry
        for entry in protocol_parser(filepath=Path(testing_sample)).get_parsed_pcap()
    ]

    if verbose:
        print(f"Packet capture data retrieved for protocol ({protocol})!")

    probability = model.predict_proba(X=freq_dist(samples=protocol_data))

    if verbose:
        print(f"Probability of sample existing in model: {probability}")

    return probability
