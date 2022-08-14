"""Generic exception types"""

from .base import SplinterShellError


class ArgumentError(SplinterShellError):
    """ """


class NonexistentTrainingDirectoryError(ArgumentError):
    """ """


class NonexistentTestingSampleError(ArgumentError):
    """ """


class UnfitModelError(ArgumentError):
    """ """
