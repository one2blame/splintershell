"""Classes to encode shellcodes given frequency distributions"""
from splintershell.errors import InvalidEncoderClassError

from .encoder import Encoder
from .xor import XorEncoder

encoder_dict = {"xor": XorEncoder}


def define_encoder(new_scheme: str, new_encoder) -> None:
    if not issubclass(new_encoder, Encoder):
        raise InvalidEncoderClassError(
            "Encoder class provided does not inherit from Encoder class"
        )

    encoder_dict[new_scheme] = new_encoder
