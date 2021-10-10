#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git tag sets a version string.
"""

from os.path import dirname
import pathlib

from git import Repo  # type: ignore  # pylint: disable=E0401

repo_path = pathlib.Path(dirname(__file__))
repo = Repo(repo_path.parents[0])
__version__ = str(repo.tags[0])
