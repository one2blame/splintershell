"""Functions to encode a shellcode against a trained splintershell Gaussian mixture model"""
from pathlib import Path

import numpy as np
from sklearn.mixture import GaussianMixture

from splintershell.errors import NonexistentShellcodeFileError, UnfitModelError
from splintershell.learning import freq_dist

from .utils import freq_dict


def blend_shellcode(shellcode_file: str, model: GaussianMixture) -> bytes:
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

    sample_freq_dist = freq_dist(samples=[sample])[0]
    norm_sample_freq_dist = sample_freq_dist / np.sum(sample_freq_dist)
    shellcode_freq_dict = {
        k: v for k, v in freq_dict(freq_dist=norm_sample_freq_dist).items() if v != 0
    }
    sorted_shellcode_freq_dict = sorted(
        shellcode_freq_dict.items(), reverse=True, key=lambda x: x[1]
    )
    print(sorted_shellcode_freq_dict)
