from abc import ABC, abstractmethod


class Encoder(ABC):
    def __init__(self) -> None:
        self.encoded_shellcode: bytes = b""

    def get_encoded_shellcode(self) -> bytes:
        return self.encoded_shellcode

    @abstractmethod
    def encode_shellcode(self, shellcode: bytes, **kwargs) -> None:
        pass
