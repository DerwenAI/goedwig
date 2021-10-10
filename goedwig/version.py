#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git tag sets a version string.
"""

from os.path import dirname
import pathlib
import typing

repo_path = pathlib.Path(dirname(__file__))
tag_file = repo_path.parents[0] / "TAG"
__version__ = tag_file.read_text().strip()

MIN_PY_VERSION: typing.Tuple = (3, 8,)
