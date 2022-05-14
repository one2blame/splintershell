from math import ceil
from random import shuffle
from typing import Tuple


def shuffle_and_split(data: list, split_ratio: float) -> Tuple:
    # Shuffle provided list, in place
    shuffle(data)
    split_index = int(ceil(len(data) * split_ratio))
    return data[0: split_index], data[split_index: len(data)]
