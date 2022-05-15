import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from .constants import PAYL_METADATA_KEY


class Payl:
    def __init__(
        self,
        discrete_steps: int,
        verbose: bool = False,
    ):
        self.discrete_steps = discrete_steps
        self.verbose = verbose

        self.thresholds: List[int] = []
        self.feature_vectors: Dict[int, np.ndarray] = {}

    @staticmethod
    def _get_freq_from_str(string: str) -> list:
        return [string.count(chr(ordinal)) for ordinal in range(256)]

    def train(self, training_data: list) -> None:
        stepsize = int(np.ceil(len(max(training_data, key=len)) / self.discrete_steps))

        if self.verbose:
            print(f"Separating training data into buckets of size ({stepsize})...")

        training_data_element_lengths = sorted(
            set([len(element) for element in training_data])
        )

        self.thresholds = [
            min(
                training_data_element_lengths,
                key=lambda x: abs(x - ((i + 1) * stepsize)),
            )
            for i in range(self.discrete_steps - 1)
        ]
        self.thresholds.append(training_data_element_lengths[-1])
        self.thresholds = list(sorted(set(self.thresholds)))

        if self.verbose:
            print(f"Buckets: {self.thresholds}")
            print(
                f"Sorting ({len(training_data)}) training data elements into buckets..."
            )

        buckets: Dict[int, list] = {}
        for element in training_data:
            threshold = min(self.thresholds, key=lambda x: abs(len(element) - x))
            if not buckets.get(threshold, None):
                buckets[threshold] = [element]
            else:
                buckets[threshold].append(element)

        if self.verbose:
            print(f"Training the PAYL model...")

        for threshold, bucket in sorted(buckets.items()):
            freq_array = np.array(
                [self._get_freq_from_str(string=string) for string in bucket]
            )
            stddev_freq_array = np.std(freq_array, axis=0)
            mean_freq_array = np.mean(freq_array, axis=0)
            self.feature_vectors[threshold] = np.vstack(
                (mean_freq_array, stddev_freq_array)
            ).T

        if self.verbose:
            print(f"Training complete!")

    def test(
        self,
        smoothing_factor: float,
        classification_threshold: float,
        testing_data: list,
    ) -> float:
        true_positives = 0.0

        for element in testing_data:
            bucket = min(self.thresholds, key=lambda x: abs(len(element) - x))

            if bucket:
                testpoints = self._get_freq_from_str(element)
                features = self.feature_vectors[bucket]

                distances = [
                    (abs(testpoints[char] - features[char][0]))
                    / (features[char][1] + smoothing_factor)
                    for char in range(256)
                ]
                distance = sum(distances)
            else:
                distance = np.inf

            if distance <= classification_threshold:
                true_positives += 1.0

        return (true_positives / float(len(testing_data))) * 100.0

    @staticmethod
    def parse_model(model_file: Path) -> tuple:
        with model_file.open("r") as input_file:
            model = json.load(input_file)

        if not model.get(PAYL_METADATA_KEY, None):
            raise IndexError(
                f"Model metadata not provided in PAYL model file: {str(Path(model_file).resolve())}"
            )

        smoothing_factor, classification_threshold, protocol = model.pop("metadata")
        thresholds = model.keys()

        feature_vectors = dict()
        for threshold, feature_vector in model.items():
            feature_vectors[threshold] = np.asarray(feature_vector)

        return (
            smoothing_factor,
            classification_threshold,
            protocol,
            thresholds,
            feature_vectors,
        )
