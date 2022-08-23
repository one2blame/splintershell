"""System operation-related exception types"""
from .base import SplinterShellError


class OperationError(SplinterShellError):
    """ """


class DecoderReadError(OperationError):
    """ """
