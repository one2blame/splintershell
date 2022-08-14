from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class PcapParser(ABC):
    def __init__(self, filepath: Path) -> None:
        self.payload_list: List[str] = []

        if not filepath.exists():
            raise FileNotFoundError(f"File provided does not exist: {str(filepath)}")
        else:
            self.filepath = filepath

    def get_parsed_pcap(self) -> List:
        return self.payload_list

    @abstractmethod
    def parse_pcap(self) -> None:
        pass
