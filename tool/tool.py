#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fire import Fire
import kaipred as kp


class KAIPredTool(object):
    """
    Command line tool of KAIPred.

    Examples:
        >>> ./tool.py init_user --username=main
    """

    def __init__(self, username="main"):
        print(kp.get_version())
        self.user = kp.User("./", username=username)
        self.login()

    def init_user(self):
        NotImplementedError

    def login(self):
        NotImplementedError

    def add(self):
        """
        Add records of the user to the database.
        """
        NotImplementedError

    def show(self):
        """
        Show records of the user.
        """
        NotImplementedError


if __name__ == "__main__":
    Fire(KAIPredTool)
