#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from kaipred.util.crypto import Crypto


class User(object):
    """
    Information of user.

    Args:
        username (str): username
        data_dir (str): directory to save data of all users
    """
    USERNAME = "username"
    PASSPHRASE = "passphrase"
    # Setting filename
    SETTING_FILENAME = "setting.json"
    # Keys in setting file
    SETTING_KEYS = [USERNAME, PASSPHRASE]
    HIDDEN_KEYS = [PASSPHRASE]

    def __init__(self, username, data_dir):
        self._username = username.replace(" ", "")
        self._data_dirpath = Path(data_dir)
        self._authorized = False

    def login(self, password, admin_key):
        """
        Login as the user.

        Args:
            password (str): password of the user
            admin_key (str): main key to encrypt/decrypt passwords
        """
        setting_dict = self._read()
        passphrase = setting_dict[self.PASSPHRASE]
        crypto = Crypto(key=admin_key)
        if passphrase is None:
            setting_dict[self.PASSPHRASE] = crypto.encrypt(password)
            self._save(setting_dict)
        else:
            if password != crypto.decrypt(passphrase):
                raise KeyError("Sorry try again with your password.")
        self._authorized = True

    def filepath(self, basename):
        """
        Return the filename for the user.

        Returns:
            pathlib.Path: path of the file
        """
        user_path = self._data_dirpath / self._username
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path / basename

    def _read(self):
        """
        Read user data from JSON file.

        Return:
            dict(str, str): setting name and values

        Notes:
            The keys are defined with User.SETTING_KEYS and unregistered values will be None.
        """
        filepath = self.filepath(self.SETTING_FILENAME)
        if not filepath.exists():
            return {k: None for k in self.SETTING_KEYS}
        with filepath.open("r") as fh:
            loaded_dict = json.load(fh)
        return {k: loaded_dict.get(k, None) for k in self.SETTING_KEYS}

    def read(self, key):
        """
        Show setting of the user when authorized.

        Args:
            key (str): key in User.SETTING_KEYS and not in User.HIDDEN_KEYS

        Returns:
            str: setting value
        """
        if not self._authorized:
            raise ValueError("Please login in advance.")
        setting_dict = self._read()
        if key in setting_dict:
            setting_dict[key]
        allowed_key_set = set(self.SETTING_KEYS) - set(self.HIDDEN_KEYS)
        keys_str = ", ".join(allowed_key_set)
        raise KeyError(f"@key must be in {keys_str}, but {key} was applied.")

    def _save(self, setting_dict):
        """
        Save user data to the JSON file.

        Args:
            dict(str, str): user data

        Notes:
            keys must be in in User.SETTING_KEYS and not in User.HIDDEN_KEYS
        """
        cleaned_dict = {k: setting_dict.get(k, "") for k in self.SETTING_KEYS}
        filepath = self.filepath(self.SETTING_FILENAME)
        with filepath.open("w") as fh:
            json.dump(cleaned_dict, fh, indent=4)

    def save(self, **kwargs):
        """
        Register the value to the user data.

        Args:
            kwargs: keyword arguments to register

        Notes:
            keys must be in in User.SETTING_KEYS and not in User.HIDDEN_KEYS
        """
        if not self._authorized:
            raise ValueError("Please login in advance.")
        setting_dict = self._read()
        setting_dict.update(kwargs)
        self._save(setting_dict)
