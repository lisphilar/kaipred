#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import kaipred


class TestKAIPred(object):
    def test_version(self):
        version_str = kaipred.get_version()
        assert re.match(r"[A-z]+ version [0-9]\.[0-9]\.[0-9].*", version_str)
