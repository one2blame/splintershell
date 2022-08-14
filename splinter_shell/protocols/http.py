from scapy.all import *
from scapy.layers.http import *

from .pcapparser import PcapParser


class HttpPcapParser(PcapParser):
    def parse_pcap(self) -> None:
        try:
            packets = sniff(offline=str(self.filepath))

            for packet in packets:
                if packet.haslayer(HTTPRequest):
                    http_data = str("".join(map(chr, bytes(packet[HTTPRequest]))))
                    if http_data and all(ord(c) < 256 for c in http_data):
                        self.payload_list.append(http_data)

                if packet.haslayer(HTTPResponse):
                    http_data = str("".join(map(chr, bytes(packet[HTTPResponse]))))
                    if http_data and all(ord(c) < 256 for c in http_data):
                        self.payload_list.append(http_data)

        except Exception as e:
            print(f"Failed to read provided file: {str(self.filepath)}")
            raise e
