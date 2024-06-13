"""
text.substitution.py

This module provides substitution cipher classes for text encoding and decoding operations.

Classes:
    CaesarCipher -- A class for encoding and decoding text using the Caesar Cipher technique.
    AtbashCipher -- A class for encoding and decoding text using the Atbash Cipher technique.
    AffineCipher -- A class for encoding and decoding text using the Affine Cipher technique.
    VigenereCipher -- A class for encoding and decoding text using the Vigenere Cipher technique.
"""

import warnings

from encoding.utils import TextEncoder
import numpy as np


class CaesarCipher(metaclass=TextEncoder):
    """
    CaesarCipher class for encoding and decoding text using the Caesar Cipher technique.

    Attributes:
        - key (int): The key for the Caesar Cipher shift (default: 3).
        - alpha_only (bool): Flag to indicate if the cipher should only shift alphabetic characters (default: False).

    Methods:
        - __init__(self, key: int = 3, alpha_only: bool = False):
            Initializes the CaesarCipher object with the specified key and mode.
        - encode(self, text: str) -> str:
            Encodes the input text using the Caesar Cipher.
        - decode(self, text: str) -> str:
            Decodes the input text using the Caesar Cipher.
    """

    def __init__(self, key: int = 3, alpha_only: bool = False):
        """
        Initializes the CaesarCipher object with the specified key and mode.

        Parameters:
            - key (int, optional): The key for the Caesar Cipher shift (default: 3).
            - alpha_only (bool, optional): Flag to indicate if the cipher should only shift alphabetic characters (default: False).

        Warns:
            UserWarning: If alpha_only is set to True, a warning is issued indicating that the cipher is in
                Alphabet only mode.
        """

        self.key = key
        self.__is_key_default = True
        self.alpha_only = alpha_only

        if self.alpha_only:
            warnings.warn(
                message="Caesar Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

    def encode(self, text: str) -> str:
        """
        Encodes the input text using the Caesar Cipher.

        Parameters:
            - text (str): The input text to be encoded.

        Returns:
            - str: The encoded text.

        Raises:
            - ValueError: If the input text contains characters with ASCII > 127.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")
        enc_text = ""

        for i in text:
            ascii_val = ord(i)

            if self.alpha_only:
                char_value = (ascii_val + self.key)
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(char_value) if char_value <= 90 else chr(char_value - 26)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(char_value) if char_value <= 122 else chr(char_value - 26)
                else:
                    rep_letter = i
            else:
                rep_letter = chr(((ascii_val - 32 + self.key) % 95) + 32)
            enc_text += rep_letter


        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the input text using the Caesar Cipher.

        Parameters:
            - text (str): The input text to be decoded.

        Returns:
            - str: The decoded text.

        Raises:
            - ValueError: If the input text contains characters with ASCII > 127.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        if self.alpha_only:
            dec_text = ""
            for i in text:
                ascii_val = ord(i)
                char_val = ascii_val - self.key
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(char_val) if char_val >= 65 else chr(char_val + 26)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(char_val) if char_val >= 97 else chr(char_val + 26)
                else:
                    rep_letter = i
                dec_text += rep_letter
            return dec_text
        else:
            self.key *= -1
            self.__is_key_default = not self.__is_key_default
            return self.encode(text=text)


class AtbashCipher(metaclass=TextEncoder):
    """
    AtbashCipher class for encoding and decoding text using the Atbash Cipher technique.

    Attributes:
        - alpha_only (bool): Flag to indicate if the cipher should only shift alphabetic characters (default: False).

    Methods:
        - __init__(self, alpha_only: bool = False):
            Initializes the AtbashCipher object with the specified mode.
        - encode(self, text: str) -> str:
            Encodes the input text using the Atbash Cipher.
        - decode(self, text: str) -> str:
            Decodes the input text using the Atbash Cipher.
    """

    def __init__(self, alpha_only: bool = False):
        """
        Initializes the AtbashCipher object with the specified mode.

        Parameters:
            - alpha_only (bool, optional): Flag to indicate if the cipher should only shift alphabetic characters (default: False).

        Warns:
            UserWarning: If alpha_only is set to True, a warning is issued indicating that the cipher is in
                Alphabet only mode.
        """

        self.alpha_only = alpha_only
        if self.alpha_only:
            warnings.warn(
                message="Atbash Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

    def encode(self, text: str) -> str:
        """
        Encodes the input text using the Atbash Cipher.

        Parameters:
            - text (str): The input text to be encoded.

        Returns:
            - str: The encoded text.

        Raises:
            - ValueError: If the input text contains characters with ASCII > 127.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if self.alpha_only:
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(155 - ascii_val)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(219 - ascii_val)
                else:
                    rep_letter = i
            else:
                rep_letter = chr(126 - (ascii_val - 32))
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the input text using the Atbash Cipher.

        Parameters:
            - text (str): The input text to be decoded.

        Returns:
            - str: The decoded text.

        Raises:
            - ValueError: If the input text contains characters with ASCII > 127.
        """
        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        return self.encode(text=text)


class AffineCipher(metaclass=TextEncoder):
    """
    AffineCipher class for encoding and decoding text using the Affine Cipher technique.

    Attributes:
        key_a (int): The multiplicative key for the Affine Cipher (default: 1).
        key_b (int): The additive key for the Affine Cipher (default: 3).
        alpha_only (bool): Flag to indicate if the cipher should only shift alphabetic characters (default: False).

    Methods:
        __init__(self, key_a: int = 1, key_b: int = 3, alpha_only: bool = False):
            Initializes the AffineCipher object with the specified keys and mode.
        encode(self, text: str) -> str:
            Encodes the input text using the Affine Cipher.
        decode(self, text: str) -> str:
            Decodes the input text using the Affine Cipher.

    Private Methods:
        __mod_inverse(self, m):
            Private method to calculate the modular inverse of a number.
        __coprime(self) -> bool:
            Private method to check if key_a is coprime with 26 (if alpha_only) or 128.
    """

    def __init__(self, key_a: int = 3, key_b: int = 3, alpha_only: bool = False):
        """
        Initializes the AffineCipher object with the specified keys and mode.

        Parameters:
            key_a (int, optional): The multiplicative key for the Affine Cipher (default: 3).
            key_b (int, optional): The additive key for the Affine Cipher (default: 3).
            alpha_only (bool, optional): Flag to indicate if the cipher should only shift alphabetic characters
                (default: False).

        Raises:
            ValueError: If key_a is not within the specified range or not coprime with 26 (if alpha_only) or 128.

        Warns:
            UserWarning: If alpha_only is set to True, a warning is issued indicating that the cipher is in
                Alphabet only mode.
        """

        self.key_a = key_a
        self.key_b = key_b
        self.alpha_only = alpha_only

        if self.alpha_only:
            warnings.warn(
                message="Affine Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

        if not 0 <= self.key_a <= 26 and self.alpha_only:
            raise ValueError(
                f"'key_a' cannot have a value {self.key_a}. Value must be within the range: 0 <= 'key_a' <= 26.")

        if not 0 <= self.key_a <= 127 and not self.alpha_only:
            raise ValueError(
                f"'key_a' cannot have a value {self.key_a}. Value must be within the range: 0 <= 'key_a' <= 127.")

        if not self.__coprime():
            raise ValueError(f"'key_a' cannot have a value {self.key_a}. Value must be coprime with",
                             "26" if self.alpha_only else "128")

    def encode(self, text: str) -> str:
        """
        Encodes the input text using the Affine Cipher.

        Parameters:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.

        Raises:
            ValueError: If any character in the input text has ASCII value greater than 127.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if 65 <= ascii_val <= 90:
                x = ascii_val - 65 if self.alpha_only else ascii_val
            elif 97 <= ascii_val <= 122:
                x = ascii_val - 97 if self.alpha_only else ascii_val
            else:
                if self.alpha_only:
                    enc_text += i
                    continue
                else:
                    x = ascii_val
            m = 26 if self.alpha_only else 95
            rep_letter = chr(((self.key_a * (x - 32) + self.key_b) % m) + (65 if self.alpha_only else 32))
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the input text using the Affine Cipher.

        Parameters:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.

        Raises:
            ValueError: If any character in the input text has ASCII value greater than 127.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")
        dec_text = ""

        for i in text:
            ascii_val = ord(i)
            if 65 <= ascii_val <= 90:
                x = ascii_val - 65 if self.alpha_only else ascii_val
            elif 97 <= ascii_val <= 122:
                x = ascii_val - 97 if self.alpha_only else ascii_val
            else:
                if self.alpha_only:
                    dec_text += i
                    continue
                else:
                    x = ascii_val

            m = 26 if self.alpha_only else 95
            key_inv = self.__mod_inverse(m)
            if not key_inv:
                raise ValueError("Unexpected error occurred.")
            rep_letter = chr((key_inv * (x - 32 - self.key_b) % m) + (65 if self.alpha_only else 32))
            dec_text += rep_letter

        return dec_text

    def __mod_inverse(self, m):
        """
        Private method to calculate the modular inverse of a number.

        Parameters:
            m: The number for which the modular inverse is to be calculated.

        Returns:
            int or None: The modular inverse if found, None otherwise.
        """

        for i in range(1, m):
            if (self.key_a * i) % m == 1:
                return i
        return None

    def __coprime(self) -> bool:
        """
        Private method to check if key_a is coprime with 26 (if alpha_only) or 95.

        Returns:
            bool: True if key_a is coprime with the specified range, False otherwise.
        """

        a = self.key_a
        b = 26 if self.alpha_only else 95
        while b != 0:
            a, b = b, a % b
        return a == 1


class VigenereCipher(metaclass=TextEncoder):
    """
        VigenereCipher class for encoding and decoding text using the Vigenère Cipher technique.

        Attributes:
            key (str): The key for the Vigenère Cipher Swap (default: 'KEY').
            alpha_only (bool) : Flag to determine if the cipher should only handle alphabetic characters (default: False).

        Methods:
            __init__(self, key: str = 'KEY', alpha_only: bool = False):
                Initializes the VigenereCipher object with the specified keys and mode.
            encode(self, text: str) -> str:
                Encodes the input text using the Vigenère Cipher.
            decode(self, text: str) -> str:
                Decodes the input text using the Vigenère Cipher.

        Private Methods:
            __generate_matrix(self)
                Private method to generate a Vigenère square matrix for alphabet-only encoding and decoding.
        """
    def __init__(self, key: str = 'KEY', alpha_only: bool = False):
        """
            Initializes the VigenereCipher object with the specified key and mode.

            Parameters:
                key (str): The key for the Vigenère Cipher (default: 'KEY').
                alpha_only (bool): Flag to determine if the cipher should only handle alphabetic characters (default: False).

            Raises:
                ValueError: If the key is an empty string.

            Warns:
                UserWarning: If alpha_only is set to True, a warning is issued indicating that the cipher is in
                    Alphabet only mode.
        """

        self.key = key
        self.alpha_only = alpha_only
        self.final_key = ""
        if self.alpha_only:
            warnings.warn(
                message="Vigenere Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )
        if self.key == "":
            raise ValueError("Key value cannot be null")

    def encode(self, text: str) -> str:
        """
            Encodes the input text using the Vigenère Cipher.

            Parameters:
                text (str): The text to be encoded.

            Returns:
                str: The encoded text.

            Raises:
                ValueError: If the text contains characters with ASCII < 32 or ASCII > 126.
                ValueError: If the key contains non-alphabetic characters in alpha_only mode.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        self.final_key = (self.key * (len(text) // len(self.key) + 1)).upper()
        enc_text = ""
        if self.alpha_only:
            matrix = self.__generate_matrix()

        for i in range(len(text)):
            if self.alpha_only:
                if self.final_key[i].isalpha():
                    if 65 <= ord(text[i]) <= 90:
                        rep_letter = matrix[ord(text[i]) - 65][ord(self.final_key[i].upper()) - 65]
                    elif 97 <= ord(text[i]) <= 122:
                        rep_letter = matrix[ord(text[i]) - 97][ord(self.final_key[i].lower()) - 97]
                        rep_letter = rep_letter.lower()
                    else:
                        rep_letter = text[i]
                else:
                    raise ValueError("Key must be composed of alphabets in Alphabet Only mode")
            else:
                rep_letter = chr((((ord(text[i]) - 32) + (ord(self.final_key[i])- 32)) % 95) + 32)
            enc_text += rep_letter
        return enc_text

    def decode(self, text: str) -> str:
        """
            Decodes the input text using the Vigenère Cipher.

            Parameters:
                text (str): The text to be decoded.

            Returns:
                str: The decoded text.

            Raises:
                ValueError: If the text contains characters with ASCII < 32 or ASCII > 126.
                ValueError: If the key contains non-alphabetic characters in alpha_only mode.
        """

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        self.final_key = (self.key * (len(text) // len(self.key) + 1)).upper()
        dec_text = ""
        if self.alpha_only:
            matrix = self.__generate_matrix()

        for i in range(len(text)):
            if self.alpha_only:
                index = np.where(matrix[0] == self.final_key[i])
                letter = text[i].upper() if self.alpha_only else text[i]

                if not self.final_key[i].isalpha():
                    raise ValueError("Key must be composed of alphabets in Alphabet Only mode")

                for j in range(len(matrix)):
                    if matrix[j][index] == letter:
                        break

                if 65 <= ord(text[i]) <= 90:
                    rep_letter = matrix[j][0]
                elif 97 <= ord(text[i]) <= 122:
                    rep_letter = matrix[j][0]
                    rep_letter = rep_letter.lower()
                else:
                    rep_letter = text[i]
            else:
                rep_letter = chr((((ord(text[i]) - 32) - (ord(self.final_key[i]) - 32)) % 95) + 32)

            dec_text += rep_letter
        return dec_text

    def __generate_matrix(self):
        """
            Generates a Vigenère square matrix for alphabet-only encoding and decoding.

            Returns:
                np.ndarray: A 26x26 matrix used for the Vigenère Cipher.
        """

        elements = np.array([chr(i) for i in range(65, 91)], dtype='<U1')
        matrix = np.empty((26, 26), dtype='<U1')

        for i in range(len(elements)):
            matrix[i] = np.roll(elements, -i)

        return matrix
