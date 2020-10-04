#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from kaipred import KAIPred


class TestUser(object):
    @pytest.mark.parametrize("username, password", [("demo", "demo")])
    def test_login(self, username, password):
        kaipred = KAIPred(data_dir="data_test")
        kaipred.login(username=username, password=password)
