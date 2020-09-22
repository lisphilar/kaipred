#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kaipred.__info__ import __name__, __version__
from kaipred.dataset.user import User


def get_version():
    """
    Return the version number, like "KAIPred version 1.0.0"
    """
    return f"{__name__} version {__version__}"


__all__ = [
    "User",
]
