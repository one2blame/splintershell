"""Functions to encode a shellcode against a trained Gaussian mixture model"""
from random import shuffle

from sklearn.mixture import GaussianMixture

from splintershell.errors import InvalidModelObjectError, UnsupportedEncodingSchemeError
from splintershell.utils import ascii_freq_dict, freq_dist

from .schemes import XorEncoder, encoder_dict


# TODO verbose
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

    encoder_inst = encoder()
    if isinstance(encoder_inst, XorEncoder):
        sample = str("".join(map(chr, shellcode)))
        shellcode_freq_dist = freq_dist(samples=[sample])[0]
        encoder_inst.encode_shellcode(
            shellcode=shellcode,
            shellcode_freq_dist=shellcode_freq_dist,
            target_freq_dist=model.means_[0],
        )
    else:
        # TODO support more encoders
        pass

    if padding:
        encoded_shellcode = [byte for byte in encoder_inst.get_encoded_shellcode()]
        padding = []

        while len(encoded_shellcode + padding) < int(sum(model.means_[0])):
            encoded_shellcode_ascii_freq_dict = ascii_freq_dict(
                dist=freq_dist(
                    samples=[str("".join(map(chr, bytes(encoded_shellcode + padding))))]
                )[0]
            )
            model_ascii_freq_dict = ascii_freq_dict(dist=model.means_[0])
            pad_byte, pad_byte_count = sorted(
                [
                    (p, int(x - y))
                    for (p, x), (q, y) in zip(
                        model_ascii_freq_dict.items(),
                        encoded_shellcode_ascii_freq_dict.items(),
                    )
                    if x > y
                ],
                key=lambda x: x[1],
                reverse=True,
            )[0]
            padding += [pad_byte for _ in range(pad_byte_count)]

        shuffle(padding)
        return bytes(encoded_shellcode + padding)
    else:
        return encoder_inst.get_encoded_shellcode()
