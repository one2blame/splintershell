"""Functions to encode a shellcode against a trained Gaussian mixture model"""
import numpy as np
from sklearn.mixture import GaussianMixture

from splintershell.errors import InvalidModelObjectError
from splintershell.utils import ascii_freq_dict, freq_dist


def blend_shellcode(shellcode: bytes, model: GaussianMixture) -> bytes:
    if not isinstance(model, GaussianMixture):
        raise InvalidModelObjectError("Model provided is not a GaussianMixture")

    if not model.converged_:
        raise InvalidModelObjectError(f"Model provided has not been trained")

    sample = str("".join(map(chr, shellcode)))
    sample_freq_dist = freq_dist(samples=[sample])[0]
    norm_sample_freq_dist = sample_freq_dist / np.sum(sample_freq_dist)
    shellcode_freq_dict = {
        k: v for k, v in ascii_freq_dict(dist=norm_sample_freq_dist).items() if v != 0
    }
    sorted_shellcode_freq_dict = sorted(
        shellcode_freq_dict.items(), reverse=True, key=lambda item: item[1]
    )
    print(sorted_shellcode_freq_dict)
