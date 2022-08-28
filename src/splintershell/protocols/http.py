"""PcapParser definition for HTTP"""
from scapy.layers.http import HTTP
from scapy.sendrecv import sniff
from scapy.sessions import TCPSession

from splintershell.errors import ProtocolParsingError

from .pcapparser import PcapParser


class HttpPcapParser(PcapParser):
    def parse_pcap(self) -> None:
        """Extracts all HTTP data from a packet capture.

        :raises ProtocolParsingError: Exceptions raised when operating on the
        packet capture with scapy
        :return: None
        :rtype: None
        """
        try:
            packets = sniff(offline=str(self.filepath), session=TCPSession)

            for packet in packets:
                if packet.haslayer(HTTP):
                    http_data = str("".join(map(chr, bytes(packet[HTTP]))))
                    if http_data and all(ord(c) < 256 for c in http_data):
                        self.payload_list.append(http_data)

        except Exception as exc:
            raise ProtocolParsingError(str(exc))
