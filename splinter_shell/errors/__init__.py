"""splinter_shell error types"""

from .arguments import (
    NonexistentTestingSampleError,
    NonexistentTrainingDirectoryError,
    UnfitModelError,
)
from .base import SplinterShellError
from .protocols import UnsupportedProtocolError
