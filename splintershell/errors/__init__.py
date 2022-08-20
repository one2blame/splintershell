"""splintershell error types"""
from .arguments import (
    InvalidFreqDistError,
    InvalidModelObjectError,
    InvalidTrainingDirectoryError,
)
from .base import SplinterShellError
from .protocols import ProtocolParsingError, UnsupportedProtocolError
