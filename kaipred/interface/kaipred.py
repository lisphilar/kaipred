#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import shutil
from kaipred.util.crypto import Crypto
from kaipred.admin.user import User


class KAIPred(object):
    """
    Interface of KAIPred.

    Args:
        data_dir (str): directory to save data of all users
    """
    ADMIN = "admin"
    ADMIN_FILENAME = "admin.json"
    # Keys in admin file
    ADMIN_KEYS = [ADMIN]

    def __init__(self, data_dir="data"):
        # Filepath
        self._data_dir = data_dir
        admin_dirpath = Path(data_dir)
        admin_dirpath.mkdir(exist_ok=True)
        self._adminpath = admin_dirpath / self.ADMIN_FILENAME
        # Login user
        self._login_user = None

    @property
    def login_user(self):
        """
        The user currently login.
        """
        self._login_user

    def _read_admin(self):
        """
        Read information of admin file.

        Returns:
            dict(str, str): admin information

        Notes:
            Keys of information is determined by KAIPred.ADMIN_KEYS
        """
        if not self._adminpath.exists():
            return {}
        with self._adminpath.open("r") as fh:
            loaded_dict = json.load(fh)
        return {k: loaded_dict.get(k, None) for k in self.ADMIN_KEYS}

    def _save(self, admin_dict):
        """
        Save admin information.

        Args:
            admin_dict (dict(str, str)): admin information

        Notes:
            Keys of information is determined by KAIPred.ADMIN_KEYS
        """
        cleaned_dict = {k: admin_dict.get(k, "") for k in self.ADMIN_KEYS}
        with self._adminpath.open("w") as fh:
            json.dump(cleaned_dict, fh, indent=4)

    def _find_key(self):
        """
        Find the key to encrypt/decrypt the passwords of users.

        Returns:
            str: admin key
        """
        admin_dict = self._read_admin()
        print(admin_dict)
        if self.ADMIN not in admin_dict:
            key = Crypto.create_key()
            self._save({self.ADMIN: key})
            return key
        return admin_dict[self.ADMIN]

    def login(self, username, password):
        """
        Login as the user.

        Args:
            username (str): username
            password (str): password of the user
        """
        user = User(username=username, data_dir=self._data_dir)
        user.login(password=password, admin_key=self._find_key())
        self._login_user = user

    def delete(self, backup=True):
        """
        Delete all data of the user.
        If main user, all records of all users will be deleted.

        Args:
            backup (bool): if True, back up the files.
        """
        if self._login_user is None:
            raise ValueError("Must login in advance.")
        if backup:
            self.backup()
        if self._login_user.username == "main":
            shutil.rmtree(self._data_dir)
        else:
            shutil.rmtree(self._login_user.dir)

    def backup(self, username):
        pass
