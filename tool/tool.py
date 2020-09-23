#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fire import Fire
import kaipred as kp


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
        print(kp.get_version())
        self.user = kp.User(username=username, data_dir=data_dir)

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
