import pkgutil
from typing import Tuple

import numpy as np

from splintershell.common import ascii_freq_dict
from splintershell.errors import DecoderReadError, InvalidFreqDistError

from .encoder import Encoder


class XorEncoder(Encoder):
    @staticmethod
    def _calc_substitution_dict(
        shellcode_freq_dist: list, target_freq_dist: list
    ) -> dict:
        shellcode_ascii_freq = sorted(
            {
                k: v
                for k, v in ascii_freq_dict(
                    dist=shellcode_freq_dist / np.sum(shellcode_freq_dist)
                ).items()
                if v != 0
            }.items(),
            reverse=True,
            key=lambda item: item[1],
        )

        target_ascii_freq = sorted(
            {
                k: v
                for k, v in ascii_freq_dict(
                    dist=target_freq_dist / np.sum(target_freq_dist)
                ).items()
                if v != 0
            }.items(),
            reverse=True,
            key=lambda item: item[1],
        )

        m = len(shellcode_ascii_freq)
        substitution_dict = {}
        shellcode_totals_dict = {}
        shellcode_ascii_freq_dict = {}

        for i in range(m):
            shellcode_char, shellcode_char_freq = shellcode_ascii_freq[i]
            substitution_dict[shellcode_char] = [target_ascii_freq[i]]
            shellcode_ascii_freq_dict[shellcode_char] = shellcode_char_freq
            shellcode_totals_dict[shellcode_char] = target_ascii_freq[i][1]

        for i in range(m):
            target_ascii_freq.pop(0)

        for character_tuple in target_ascii_freq:
            next_shellcode_char = sorted(
                [
                    (
                        shellcode_char,
                        shellcode_ascii_freq_dict[shellcode_char]
                        / shellcode_totals_dict[shellcode_char],
                    )
                    for shellcode_char in shellcode_ascii_freq_dict.keys()
                ],
                key=lambda x: x[1],
                reverse=True,
            )[0][0]

            substitution_dict[next_shellcode_char].append(character_tuple)
            shellcode_totals_dict[next_shellcode_char] += character_tuple[1]

        return substitution_dict

    @staticmethod
    def _substitute(shellcode: bytes, substitution_dict: dict) -> Tuple[list, list]:
        xor_table = []
        encoded_shellcode = []

        norm_substitution_dict = {}
        for char, substitutions in substitution_dict.items():
            total = sum([substitution[1] for substitution in substitutions])
            norm_substitutions = [
                (substitution[0], substitution[1] / total)
                for substitution in substitutions
            ]
            norm_substitution_dict[char] = norm_substitutions

        for byte in shellcode:
            substitutions = norm_substitution_dict[byte]
            choices = [substitution[0] for substitution in substitutions]
            probabilities = [substitution[1] for substitution in substitutions]
            replacement = np.random.choice(choices, p=probabilities)
            encoded_shellcode.append(replacement)
            xor_table.append(byte ^ replacement)

        return xor_table, encoded_shellcode

    def encode_shellcode(self, shellcode: bytes, **kwargs) -> None:
        """Encodes a shellcode sample using the XOR encoding scheme. Returns an
        encoded shellcode with decoder stub and XOR table.

        :param shellcode: A shellcode sample
        :type shellcode: bytes
        :param kwargs: Expected keyword arguments: shellcode_freq_dist,
        target_freq_dist
        :raises InvalidFreqDistError: An exception raised if a frequency
        distribution is not provided or misshaped
        :type kwargs: dict
        :return: None
        :rtype: None
        """
        shellcode_freq_dist = kwargs.get("shellcode_freq_dist", None)

        if shellcode_freq_dist is None:
            raise InvalidFreqDistError(
                "Shellcode frequency distribution provided is None"
            )

        if (
            not isinstance(shellcode_freq_dist, np.ndarray)
            and len(shellcode_freq_dist.shape) != 1
        ):
            raise InvalidFreqDistError(
                "Shellcode frequency distribution provided is not a 1-dimensional NumPy array"
            )

        target_freq_dist = kwargs.get("target_freq_dist", None)

        if target_freq_dist is None:
            raise InvalidFreqDistError("Target frequency distribution provided is None")

        if (
            not isinstance(target_freq_dist, np.ndarray)
            and len(target_freq_dist.shape) != 1
        ):
            raise InvalidFreqDistError(
                "Target frequency distribution provided is not a 1-dimensional NumPy array"
            )

        substitution_dict = self._calc_substitution_dict(
            shellcode_freq_dist=shellcode_freq_dist.tolist(),
            target_freq_dist=target_freq_dist.tolist(),
        )

        xor_table, encoded_shellcode = self._substitute(
            shellcode=shellcode, substitution_dict=substitution_dict
        )

        alignment_char = sorted(
            {
                k: v
                for k, v in ascii_freq_dict(dist=target_freq_dist).items()
                if v != 0
            }.items(),
            reverse=True,
            key=lambda item: item[1],
        )[0][0]

        while (len(xor_table)) % 4:
            xor_table.append(alignment_char)

        while (len(encoded_shellcode)) % 4:
            encoded_shellcode.append(alignment_char)

        # TODO support more architectures
        decoder = pkgutil.get_data(__name__, "bin/xor_decoder.bin")
        if decoder is None:
            raise DecoderReadError("Failed to acquire decoder stub")

        stamped_decoder = decoder.replace(
            b"\x62\x62\x62\x62\x62\x62\x62\x62",
            len(encoded_shellcode).to_bytes(8, "little"),
        )

        self.encoded_shellcode = b"".join(
            [stamped_decoder, bytes(encoded_shellcode), bytes(xor_table)]
        )
