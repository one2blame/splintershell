"""System operation-related exception types"""
from .base import SplinterShellError


class OperationError(SplinterShellError):
    """Base exception type for failed system operations."""


class DecoderReadError(OperationError):
    """An exception type for failing to read decoders from the filesystem"""
