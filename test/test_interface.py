#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from kaipred import KAIPred


class TestInterface(object):
    @pytest.mark.parametrize("username, password", [("main", "main")])
    def test_login(self, username, password):
        # Delete all data
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
        kaipred.delete(backup=False)
        # Create main user
        kaipred = KAIPred(data_dir="data_test")
        with pytest.raises(ValueError):
            kaipred.delete()
        kaipred.login(username=username, password=password)
        # Re-login main user
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
        # Create second user
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username="second", password=password)
        # Re-login second user
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username="second", password=password)
        # Delete second user
        assert str(kaipred.login_user) == "second"
        kaipred.delete(backup=True)
