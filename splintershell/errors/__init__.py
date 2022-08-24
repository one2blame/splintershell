"""splintershell error types"""
from .arguments import (
    InvalidEncoderClassError,
    InvalidFreqDistError,
    InvalidModelObjectError,
    InvalidParserClassError,
    InvalidTrainingDirectoryError,
)
from .base import SplinterShellError
from .encoding import UnsupportedEncodingSchemeError
from .operations import DecoderReadError
from .protocols import ProtocolParsingError, UnsupportedProtocolError
