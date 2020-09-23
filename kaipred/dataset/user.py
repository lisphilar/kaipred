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

    def __init__(self, username, data_dir):
        self._data_dirpath = Path(data_dir)
        self._username = username

    def filepath(self, basename):
        """
        Return the filename for the user.

        Returns:
            pathlib.Path: path of the file
        """
        user_path = self._data_dirpath / self._username
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path / basename
