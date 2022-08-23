"""Functions to encode a shellcode against a trained Gaussian mixture model"""
from sklearn.mixture import GaussianMixture

from splintershell.errors import InvalidModelObjectError, UnsupportedEncodingSchemeError
from splintershell.utils import freq_dist

from .schemes import encoder_dict


def blend_shellcode(
    shellcode: bytes, model: GaussianMixture, scheme: str, padding: bool
) -> bytes:
    if not isinstance(model, GaussianMixture):
        raise InvalidModelObjectError("Model provided is not a GaussianMixture")

    if not model.converged_:
        raise InvalidModelObjectError(f"Model provided has not been trained")

    encoder = encoder_dict.get(scheme, None)
    if encoder is None:
        raise UnsupportedEncodingSchemeError(
            f"Encoding scheme specified not supported: {scheme}"
        )

    sample = str("".join(map(chr, shellcode)))
    shellcode_freq_dist = freq_dist(samples=[sample])[0]
    encoder_inst = encoder()
    encoder_inst.encode_shellcode(
        shellcode=shellcode,
        shellcode_freq_dist=shellcode_freq_dist,
        target_freq_dist=model.means_[0],
    )

    return encoder_inst.get_encoded_shellcode()
