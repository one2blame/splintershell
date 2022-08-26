"""Base class definition for PcapParser"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class PcapParser(ABC):
    """Abstract class to define PcapParsers, intended to be inherited and
    extended by subclasses for parsing of different protocols.

    :param filepath: A Path object for a .pcap file
    :type filepath: pathlib.Path
    """

    def __init__(self, filepath: Path) -> None:
        self.payload_list: List[str] = []

        if not filepath.exists():
            raise FileNotFoundError(f"File provided does not exist: {str(filepath)}")
        else:
            self.filepath = filepath

    def get_parsed_pcap(self) -> List[str]:
        """Returns the object's parsed packet capture data.

        :return: A list of strings parsed packet capture data
        :rtype: List[str]
        """
        return self.payload_list

    @abstractmethod
    def parse_pcap(self) -> None:
        """Parses the object's packet capture data.

        :return: None
        :rtype: None
        """
        pass
