import numpy as np
from typing import Dict


class Payl:
    def __init__(
        self,
        smoothing_factor: float,
        classification_threshold: float,
        discrete_steps: int,
        verbose: bool = False,
    ):
        self.smoothing_factor = smoothing_factor
        self.classification_threshold = classification_threshold
        self.discrete_steps = discrete_steps
        self.verbose = verbose

        self.feature_vectors: Dict[int, np.ndarray] = {}

    @staticmethod
    def _get_freq_from_str(string: str) -> list:
        return [string.count(chr(ordinal)) for ordinal in range(256)]

    def train(self, training_data: list, test_data: list) -> None:
        stepsize = int(np.ceil(len(max(training_data, key=len)) / self.discrete_steps))
        training_data_element_lengths = sorted(
            set([len(element) for element in training_data])
        )

        thresholds = [
            min(
                training_data_element_lengths,
                key=lambda x: abs(x - ((i + 1) * stepsize)),
            )
            for i in range(self.discrete_steps - 1)
        ]
        thresholds.append(training_data_element_lengths[-1])

        buckets: Dict[int, list] = {}
        for element in training_data:
            for i in range(self.discrete_steps):
                if len(element) <= thresholds[i]:
                    if not buckets.get(thresholds[i], None):
                        buckets[thresholds[i]] = [element]
                    else:
                        buckets[thresholds[i]].append(element)
                    break

        for threshold, bucket in sorted(buckets.items()):
            freq_array = np.array(
                [self._get_freq_from_str(string=string) for string in bucket]
            )
            stddev_freq_array = np.std(freq_array, axis=0)
            mean_freq_array = np.mean(freq_array, axis=0)
            self.feature_vectors[threshold] = np.vstack(
                (mean_freq_array, stddev_freq_array)
            ).T
