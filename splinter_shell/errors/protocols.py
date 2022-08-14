"""Protocol-related exception types"""

from .base import SplinterShellError


class ProtocolError(SplinterShellError):
    """ """


class UnsupportedProtocolError(ProtocolError):
    """ """
