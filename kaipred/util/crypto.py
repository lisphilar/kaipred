#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from cryptography.fernet import Fernet


class Crypto(object):
    """
    Encrypt and decrypto a string with a key.

    Args:
        key (str or None): admin key

    Notes:
        When @key is None, register a random string as the key.
    """

    def __init__(self, key=None):
        key_str = key or self.create_key()
        encoded_key = base64.b64decode(key_str.encode())
        self._cipher = Fernet(encoded_key)

    @staticmethod
    def create_key():
        """
        Create a admin key.

        Returns:
            str: admin key
        """
        raw_key = Fernet.generate_key()
        decoded = base64.b64encode(raw_key).decode()
        return decoded[:(len(decoded) // 4) * 4]

    def encrypt(self, raw):
        """
        Encrypt the string.

        Args:
            raw (str): target string

        Return"
            str: encrypted string
        """
        # str to bytes
        encoded = base64.b64decode(raw.encode())
        # encrypt
        encoded_encrypted = self._cipher.encrypt(encoded)
        # bytes to str
        return base64.b64encode(encoded_encrypted).decode("utf-8")

    def decrypt(self, encrypted):
        """
        Decrypt the encrypted string.

        Args:
            str: encrypted string
        """
        # str to bytes
        encoded_encrypted = base64.b64decode(encrypted.encode())
        # decrypt
        encoded = self._cipher.decrypt(encoded_encrypted)
        # bytes to str
        return base64.b64encode(encoded).decode("utf-8")
