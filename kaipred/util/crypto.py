#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import random
import string
from Crypto.Cipher import AES


class Crypto(object):
    """
    Encrypt and decrypto a string with a key.

    Args:
        key (str or None): master key

    Notes:
        When @key is None, register a random string as the key.
    """

    def __init__(self, key=None):
        self.key = key or self.create_key()
        self.cipher = AES.new(self.key)

    @staticmethod
    def create_key():
        """
        Create a master key.

        Returns:
            str: master key
        """
        choices = list(string.ascii_letters + string.digits)
        random_list = random.choices(choices, k=32)
        return "".join(random_list)

    def encrypt(self, raw):
        """
        Encrypt the string.

        Args:
            raw (str): target string

        Return"
            str: encrypted string
        """
        number = ((len(raw) // 16) + 1) * 16
        try:
            raw16 = raw.ljust(number, u" ")
        except TypeError:
            raw16 = raw.ljust(number, b" ")
        encrypted = self.cipher.encrypt(raw16)
        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, encrypted):
        """
        Decrypt the encrypted string.

        Args:
            str: encrypted string
        """
        encoded = base64.b64decode(encrypted.encode())
        raw = self.cipher.decrypt(encoded).decode()
        return raw.rstrip()
