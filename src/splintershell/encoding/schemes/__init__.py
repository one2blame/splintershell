"""Classes to encode shellcodes given frequency distributions"""
from splintershell.errors import InvalidEncoderClassError

from .encoder import Encoder
from .xor import XorEncoder

encoder_dict = {"xor": XorEncoder}


def define_encoder(new_scheme: str, new_encoder) -> None:
    """A method to extend splintershell at runtime with new Encoder
    definitions for unsupported encoding schemes.

    :param new_scheme: The encoding scheme this new Encoder supports
    :type new_scheme: str
    :param new_encoder: A subclass of Encoder that implements the new_scheme
    encoding scheme
    :return: None
    :rtype: None
    """
    if not issubclass(new_encoder, Encoder):
        raise InvalidEncoderClassError(
            "Encoder class provided does not inherit from Encoder class"
        )

    encoder_dict[str(new_scheme).lower()] = new_encoder
