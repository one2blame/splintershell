"""PcapParser definition for HTTP requests and responses"""
from scapy.all import *
from scapy.layers.http import *

from splintershell.errors import ProtocolParsingError

from .pcapparser import PcapParser


class HttpPcapParser(PcapParser):
    def parse_pcap(self) -> None:
        try:
            packets = sniff(offline=str(self.filepath), session=TCPSession)

            for packet in packets:
                if packet.haslayer(HTTP):
                    http_data = str("".join(map(chr, bytes(packet[HTTP]))))
                    if http_data and all(ord(c) < 256 for c in http_data):
                        self.payload_list.append(http_data)

        except Exception as e:
            raise ProtocolParsingError(str(e))
