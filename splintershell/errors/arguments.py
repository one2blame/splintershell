"""Generic exception types"""
from .base import SplinterShellError


class ArgumentError(SplinterShellError):
    """ """


class NonexistentTrainingDirectoryError(ArgumentError):
    """ """


class NonexistentShellcodeFileError(ArgumentError):
    """ """


class NonexistentModelFileError(ArgumentError):
    """ """


class InvalidPickledObjectError(ArgumentError):
    """ """


class InvalidFreqDistError(ArgumentError):
    """ " """


class UnfitModelError(ArgumentError):
    """ """
