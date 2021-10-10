#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git tag sets a version string.
"""

import typing

from .tag import TAG

__version__ = TAG

MIN_PY_VERSION: typing.Tuple = (3, 8,)
