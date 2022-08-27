from abc import ABC, abstractmethod


class Encoder(ABC):
    """Abstract class to define Encoders, intended to be inherited and
    extended by subclasses for encoding shellcodes with different schemes.
    """

    def __init__(self) -> None:
        self.encoded_shellcode: bytes = b""

    def get_encoded_shellcode(self) -> bytes:
        """Returns the encoder's encoded shellcode.

        :return: encoded_shellcode
        :rtype: bytes
        """
        return self.encoded_shellcode

    @abstractmethod
    def encode_shellcode(self, shellcode: bytes, **kwargs) -> None:
        """Abstract method to implement different encoding schemes.

        :param shellcode: A shellcode sample
        :type shellcode: bytes
        :param kwargs: Keyword arguments, different for each encoding scheme
        class inheriting this abstract method
        :type kwargs: dict
        :return: None
        :rtype: None
        """
        pass
