"""Generic exception types"""
from .base import SplinterShellError


class ArgumentError(SplinterShellError):
    """Base exception type for invalid arguments."""


class InvalidTrainingDirectoryError(ArgumentError):
    """An exception type for when invalid or nonexistent training directories
    are provided as arguments."""


class InvalidFreqDistError(ArgumentError):
    """An exception type for nonexistent or misshaped frequency distributions
    are provided as arguments."""


class InvalidModelObjectError(ArgumentError):
    """An exception type for GMM object type mismatches when objects are
    provided as arguments."""


class InvalidParserClassError(ArgumentError):
    """An exception type for PcapParser class type mismatches when classes are
    provided as arguments."""


class InvalidEncoderClassError(ArgumentError):
    """An exception type for Encoder class type mismatches when classes are
    provided as arguments."""
