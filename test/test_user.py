#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from kaipred import User, KAIPred


class TestUser(object):
    def test_user(self):
        user = User("demo", "data_test")
        user2 = User("demo2", "data_test")
        assert str(user) == user.username
        with pytest.raises(NotImplementedError):
            user == "demo"
        assert user != user2
        assert user.dir == "data_test"

    @pytest.mark.parametrize("username, password", [("demo", "demopassword")])
    def test_login(self, username, password):
        # Delete all data
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
        kaipred.delete(backup=False)
        # Create/login main user
        with pytest.raises(ValueError):
            new_user = User("new", data_dir="data_test")
            new_user.save(info="info")
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
        user = kaipred.login_user
        # Re-login with incorrect password
        with pytest.raises(KeyError):
            kaipred.login(username=username, password="demo")
        # Read user setting
        assert user.read("username") == username
        with pytest.raises(KeyError):
            user.read("new")
        # Save user setting
        user.save(info="information")
