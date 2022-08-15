"""splintershell error types"""
from .arguments import (
    InvalidPickledObjectError,
    NonexistentModelFileError,
    NonexistentShellcodeFileError,
    NonexistentTrainingDirectoryError,
    UnfitModelError,
)
from .base import SplinterShellError
from .protocols import ProtocolParsingError, UnsupportedProtocolError
