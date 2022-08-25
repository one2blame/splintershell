"""Protocol-related exception types"""
from .base import SplinterShellError


class ProtocolError(SplinterShellError):
    """Base exception type for protocol-related errors."""


class UnsupportedProtocolError(ProtocolError):
    """An exception type for unsupported protocols requested by user."""


class ProtocolParsingError(ProtocolError):
    """An exception type for pcap parsing-related errors."""
