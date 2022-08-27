"""Classes to extract data from different protocols"""
from splintershell.errors import InvalidParserClassError

from .http import HttpPcapParser
from .pcapparser import PcapParser

protocol_dict = {"http": HttpPcapParser}


def define_protocol_parser(new_protocol: str, new_parser) -> None:
    """A method to extend splintershell at runtime with new PcapParser
    definitions for unsupported protocols.

    :param new_protocol: The protocol name this new PcapParser supports
    :type new_protocol: str
    :param new_parser: A subclass of PcapParser that parses the new_protocol
    from a packet capture
    :return: None
    :rtype: None
    """
    if not issubclass(new_parser, PcapParser):
        raise InvalidParserClassError(
            "Parser class provided does not inherit from PcapParser class"
        )

    protocol_dict[str(new_protocol).lower()] = new_parser
