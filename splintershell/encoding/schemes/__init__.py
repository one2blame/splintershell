"""Classes to encode shellcodes given frequency distributions"""
from .xor import XorEncoder

encoder_dict = {"xor": XorEncoder}
