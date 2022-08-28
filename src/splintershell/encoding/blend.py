"""Functions to encode a shellcode against a trained Gaussian mixture model"""
from random import shuffle
from typing import List

from loguru import logger
from sklearn.mixture import GaussianMixture

from splintershell.common import ascii_freq_dict, freq_dist
from splintershell.errors import InvalidModelObjectError, UnsupportedEncodingSchemeError

from .schemes import XorEncoder, encoder_dict


def blend_shellcode(
    shellcode: bytes, model: GaussianMixture, scheme: str, padding: bool, verbose: bool
) -> bytes:
    """Blends a shellcode sample to match a trained, single-cluster Gaussian
    Mixture Model using a specified encoding scheme. Optionally pads the
    shellcode to also match the size of the Gaussian Mixture Model cluster mean.

    :param shellcode: A shellcode sample
    :type shellcode: bytes
    :param model: A trained, single-cluster GaussianMixture
    :type model: GaussianMixture
    :raises InvalidModelObjectError: An exception raised when the model
    parameter provided is not a trained GaussianMixture
    :param scheme: An encoding scheme
    :type scheme: str
    :raises UnsupportedEncodingSchemeError: An exception raised when the
    encoding scheme request is unsupported
    :param padding: Enabling shellcode padding
    :type padding: bool
    :return: An encoded shellcode sample, complete with decoder stub
    :rtype: bytes
    """
    if not isinstance(model, GaussianMixture):
        raise InvalidModelObjectError("Model provided is not a GaussianMixture")

    if not model.converged_:
        raise InvalidModelObjectError(f"Model provided has not been trained")

    encoder = encoder_dict.get(scheme, None)
    if encoder is None:
        raise UnsupportedEncodingSchemeError(
            f"Encoding scheme specified not supported: {scheme}"
        )

    if verbose:
        logger.info(
            f"Blending [{len(shellcode)}] shellcode bytes using an [{scheme}] encoding scheme"
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

    model_mean_size = int(sum(model.means_[0]))
    if padding:
        encoded_shellcode = list(encoder_inst.get_encoded_shellcode())
        encoded_shellcode_size = len(encoded_shellcode)

        if encoded_shellcode_size < model_mean_size:
            shellcode_padding: List[int] = []
            if verbose:
                logger.info(
                    f"Padding shellcode with [{model_mean_size - encoded_shellcode_size}] bytes"
                )

            while len(encoded_shellcode + shellcode_padding) < model_mean_size:
                encoded_shellcode_ascii_freq_dict = ascii_freq_dict(
                    dist=freq_dist(
                        samples=[
                            str(
                                "".join(
                                    map(
                                        chr,
                                        bytes(encoded_shellcode + shellcode_padding),
                                    )
                                )
                            )
                        ]
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
                shellcode_padding += [pad_byte for _ in range(pad_byte_count)]

            shuffle(shellcode_padding)
            return bytes(encoded_shellcode + shellcode_padding)
        else:
            logger.warning(
                f"Shellcode provided is already [{encoded_shellcode_size - model_mean_size}] bytes longer than model mean"
            )
            logger.info("Returning shellcode without padding...")

    return encoder_inst.get_encoded_shellcode()
