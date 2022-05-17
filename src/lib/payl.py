import json
from pathlib import Path
from typing import Dict, List

import numpy as np
from scipy.spatial.distance import cityblock

from .constants import PAYL_METADATA_KEY


class Payl:
    def __init__(
        self,
        discrete_steps: int,
        verbose: bool = False,
    ):
        self.discrete_steps = discrete_steps
        self.verbose = verbose
        self.bucket_sizes: List[int] = []
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

        self.bucket_sizes = [
            min(
                training_data_element_lengths,
                key=lambda x: abs(x - ((i + 1) * stepsize)),
            )
            for i in range(self.discrete_steps - 1)
        ]
        self.bucket_sizes.append(training_data_element_lengths[-1])
        self.bucket_sizes = list(sorted(set(self.bucket_sizes)))

        if self.verbose:
            print(f"Buckets: {self.bucket_sizes}")
            print(
                f"Sorting ({len(training_data)}) training data elements into buckets..."
            )

        buckets: Dict[int, list] = {}
        for element in training_data:
            bucket_size = min(self.bucket_sizes, key=lambda x: abs(len(element) - x))
            if not buckets.get(bucket_size, None):
                buckets[bucket_size] = [element]
            else:
                buckets[bucket_size].append(element)

        if self.verbose:
            print(f"Training the PAYL model...")

        for bucket_size, bucket in sorted(buckets.items()):
            freq_array = np.array(
                [self._get_freq_from_str(string=string) for string in bucket]
            )
            mean_freq_array = np.mean(freq_array, axis=0)
            self.feature_vectors[bucket_size] = mean_freq_array

        if self.verbose:
            print(f"Training complete!")

    def test(
        self,
        classification_thresholds: dict,
        testing_data: list,
    ) -> dict:
        results = dict.fromkeys(self.bucket_sizes, (0.0, 0.0))

        for i in range(len(self.bucket_sizes)):
            true_positives = 0.0

            classification_threshold = classification_thresholds.get(self.bucket_sizes[i], None)
            features = self.feature_vectors.get(self.bucket_sizes[i], None)

            if i > 0:
                this_testing_data = [element for element in testing_data if len(element) <= self.bucket_sizes[i] and len(element) > self.bucket_sizes[i-1]]
            else:
                this_testing_data = [element for element in testing_data if
                                     len(element) <= self.bucket_sizes[i]]

            if not len(this_testing_data):
                continue

            testpoints = np.array([self._get_freq_from_str(element) for element in this_testing_data])
            distances = np.array([cityblock(testpoint, features) for testpoint in testpoints])
            max_distance = distances.max()

            for distance in distances:
                if distance <= classification_threshold:
                    true_positives += 1.0

            results[self.bucket_sizes[i]] = (true_positives / float(len(this_testing_data))) * 100.0, max_distance

        return results

    @staticmethod
    def parse_model(model_file: Path) -> tuple:
        with model_file.open("r") as input_file:
            model = json.load(input_file)

        if not model.get(PAYL_METADATA_KEY, None):
            raise IndexError(
                f"Model metadata not provided in PAYL model file: {str(Path(model_file).resolve())}"
            )

        classification_thresholds, protocol = model.pop(PAYL_METADATA_KEY)
        bucket_sizes = list(map(int, list(model.keys())))

        calibrated_thresholds = dict()
        for bucket_size, distance in classification_thresholds.items():
            calibrated_thresholds[int(bucket_size)] = distance

        feature_vectors = dict()
        for bucket_size, feature_vector in model.items():
            feature_vectors[int(bucket_size)] = np.asarray(feature_vector)

        return (
            calibrated_thresholds,
            protocol,
            bucket_sizes,
            feature_vectors,
        )
