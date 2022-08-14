"""Classes to extract data from different protocols"""

from .http import HttpPcapParser

protocol_dict = {"http": HttpPcapParser}
