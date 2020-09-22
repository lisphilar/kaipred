#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path


class User(object):
    """
    Information of user.

    Args:
        username (str): user name
        data_dir (str): directory to save data of all users
    """

    def __init__(self, data_dir, username):
        self._data_dirpath = Path(data_dir)
        self._username = username

    def path(self):
        """
        Return the directory name of the user.

        Returns:
            pathlib.Path: directory
        """
        user_path = self._data_dirpath / self._username
        user_path.makedirs(exist_ok=True)
        return user_path
