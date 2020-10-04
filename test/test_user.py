#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from kaipred import KAIPred


class TestUser(object):
    @pytest.mark.parametrize("username, password", [("main", "main")])
    def test_login(self, username, password):
        # Delete all data
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
        kaipred.delete(backup=False)
        # Create main user
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
        # Re-login main user
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
