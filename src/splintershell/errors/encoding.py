"""Encoding-related exception types"""
from .base import SplinterShellError


class EncodingError(SplinterShellError):
    """Base exception type for encoding-related errors."""


class UnsupportedEncodingSchemeError(EncodingError):
    """An exception type for unsupported encoding schemes."""
