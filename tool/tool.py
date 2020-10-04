#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fire import Fire
from kaipred import KAIPred


class KAIPredTool(object):
    """
    Command line tool of KAIPred.

    Args:
        username (str): user name
        data_dir (str): directory to save data of all users

    Examples:
        >>> ./tool.py add --username=main
    """

    def __init__(self, username="main", data_dir="data"):
        kaipred = KAIPred(data_dir=data_dir)
        # Set password with dialog or clipboard
        password = ""
        kaipred.login(username=username, password=password)
        self.user = kaipred.login_user

    def add(self):
        """
        Add records of the user to the database.
        """
        print(self.user.filepath("a.txt"))

    def show(self):
        """
        Show records of the user.
        """
        NotImplementedError


if __name__ == "__main__":
    Fire(KAIPredTool)
