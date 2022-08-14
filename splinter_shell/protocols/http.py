from dpkt import ethernet, pcap

from .pcapparser import PcapParser


class HttpPcapParser(PcapParser):
    def parse_pcap(self) -> None:
        try:
            with self.filepath.open(mode="rb") as pcap_file:
                pcap_data = pcap.Reader(pcap_file)
                for _, buf in pcap_data:
                    protocol_data = ethernet.Ethernet(buf).data.data
                    if protocol_data.sport == 80 or protocol_data.dport == 80:
                        http_data = str("".join(map(chr, protocol_data.data)))
                        if http_data and all(ord(c) < 256 for c in http_data):
                            self.payload_list.append(http_data)
        except Exception as e:
            print(f"Failed to read provided file: {str(self.filepath)}")
            raise e
