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
    ADMIN_MAIN = "main-user"
    ADMIN_ALL = "all-users"
    SEP = ", "
    # Keys in admin file
    ADMIN_KEYS = [ADMIN, ADMIN_MAIN, ADMIN_ALL]

    def __init__(self, data_dir="data"):
        # Filepath
        self._data_dir = data_dir
        admin_dirpath = Path(data_dir)
        admin_dirpath.mkdir(exist_ok=True)
        self._adminpath = admin_dirpath / self.ADMIN_FILENAME
        admin_dict = self._read_admin()
        # Login user
        self._login_user = None
        # Main user
        if admin_dict[self.ADMIN_MAIN] is None:
            self._main_user = None
        else:
            self._main_user = User(admin_dict[self.ADMIN_MAIN], data_dir)
        # All users
        if admin_dict[self.ADMIN_ALL] is None:
            self._all_users = []
        else:
            self._all_users = [
                User(name, data_dir) for name in admin_dict[self.ADMIN_ALL].split(self.SEP)]

    @property
    def login_user(self):
        """
        kaipred.User: the user currently login
        """
        return self._login_user

    def _read_admin(self):
        """
        Read information of admin file.

        Returns:
            dict(str, str): admin information

        Notes:
            Keys of information is determined by KAIPred.ADMIN_KEYS
        """
        if not self._adminpath.exists():
            return {k: None for k in self.ADMIN_KEYS}
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
        if admin_dict[self.ADMIN] is None:
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
        if user not in self._all_users:
            self._all_users.append(user)
            self._main_user = self._main_user or user
            admin_dict = self._read_admin()
            admin_dict[self.ADMIN_MAIN] = self._main_user.username
            admin_dict[self.ADMIN_ALL] = self.SEP.join(
                [str(user) for user in self._all_users])
            self._save(admin_dict)
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
        if self._login_user == self._main_user:
            shutil.rmtree(self._data_dir)
        else:
            shutil.rmtree(self._login_user.dir)

    def backup(self):
        pass
