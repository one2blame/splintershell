"""Training class for splinter-shell"""
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from sklearn.mixture import GaussianMixture

from .lib.protocol import protocols
from .lib.utils import freq_dist


class Train:
    def __init__(
        self,
        protocol: str = None,
        num_clusters: int = 2,
        directory: str = None,
        output: str = f"{Path.joinpath(Path.cwd(), 'splinter-shell-model')}-{int(time.time())}.json",
        verbose: bool = False,
    ):
        self.protocol = protocol
        self.num_clusters = num_clusters
        self.directory = directory
        self.output = output
        self.verbose = verbose

        if protocol is None or directory is None:
            self._get_parsed_args()

        if self._validate_args():
            raise AssertionError(
                "Bad parameters provided for Train class initialization!"
            )

    def _get_parsed_args(self) -> None:
        parser = ArgumentParser(
            prog="train",
            description="train a model on provided packet captures",
        )
        parser.add_argument(
            "--protocol",
            "-p",
            dest="protocol",
            type=str.lower,
            required=True,
            help="specify protocol to train model on",
        )
        parser.add_argument(
            "--num-clusters",
            "-n",
            dest="num_clusters",
            type=int,
            default=self.num_clusters,
            help="specify number of clusters to fit in model",
        )
        parser.add_argument(
            "--directory",
            "-d",
            dest="directory",
            required=True,
            help="directory containing training data",
        )
        parser.add_argument(
            "--output",
            "-o",
            dest="output",
            type=str,
            default=self.output,
            help="output file for trained model",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            dest="verbose",
            action="store_true",
            default=self.verbose,
            help=f"print verbose output",
        )

        opts = parser.parse_args()
        self.protocol = opts.protocol
        self.num_clusters = opts.num_clusters
        self.directory = opts.directory
        self.output = opts.output
        self.verbose = opts.verbose

    def _validate_args(self) -> int:
        try:
            assert Path(self.directory).is_dir()
        except AssertionError:
            print(f"Directory does not exist: {str(Path(self.directory).resolve())}")
            return 1

        try:
            assert protocols.get(self.protocol, None)
        except AssertionError:
            print(f"Protocol specified not supported: {self.protocol}")
            return 1

        try:
            assert 3 > self.num_clusters > 0
        except AssertionError:
            print(f"Number of clusters provided out of range (1 or 2)")
            return 1

        return 0


def main() -> int:
    opts = get_parsed_args()
    if validate_args(opts):
        return 1

    if opts.verbose:
        print(f"Acquiring packet capture data from ({opts.directory})...")

    protocol_parser = protocols.get(opts.protocol, None)
    protocol_parsers = [
        protocol_parser(filepath=filepath)  # type: ignore
        for filepath in Path(opts.directory).iterdir()
    ]

    protocol_data = []
    for parser in protocol_parsers:
        parser.parse_pcap()
        for entry in parser.get_parsed_pcap():
            protocol_data.append(entry)

    if opts.verbose:
        print(f"Packet capture data retrieved for protocol ({opts.protocol})!")

    model = GaussianMixture(n_components=opts.num_clusters, verbose=int(opts.verbose))
    model.fit(X=freq_dist(samples=protocol_data))

    return 0
