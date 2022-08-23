"""Encoding-related exception types"""
from .base import SplinterShellError


class EncodingError(SplinterShellError):
    """ """


class UnsupportedEncodingSchemeError(EncodingError):
    """ """
