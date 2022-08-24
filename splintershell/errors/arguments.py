"""Generic exception types"""
from .base import SplinterShellError


class ArgumentError(SplinterShellError):
    """ """


class InvalidTrainingDirectoryError(ArgumentError):
    """ """


class InvalidFreqDistError(ArgumentError):
    """ """


class InvalidModelObjectError(ArgumentError):
    """ """


class InvalidParserClassError(ArgumentError):
    """ """


class InvalidEncoderClassError(ArgumentError):
    """ """
