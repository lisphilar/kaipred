#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kaipred.admin.user import User


class Demo(object):
    """
    Demo dataset of KAIPred.
    """

    def __init__(self):
        self._user = User(username="demo", data_dir="data")
        self._user.login("demo", "demo")

    @property
    def user(self):
        """
        Return demo user.

        Returns:
            kaipred.User: demo user
        """
        return self._user
