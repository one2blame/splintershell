"""Classes to extract data from different protocols"""
from splintershell.errors import InvalidParserClassError

from .http import HttpPcapParser
from .pcapparser import PcapParser

protocol_dict = {"http": HttpPcapParser}


def define_protocol_parser(new_protocol: str, new_parser) -> None:
    if not issubclass(new_parser, PcapParser):
        raise InvalidParserClassError(
            "Parser class provided does not inherit from PcapParser class"
        )

    protocol_dict[new_protocol] = new_parser
