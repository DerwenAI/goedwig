#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample code.
"""

import pathlib

from icecream import ic
import goedwig


if __name__ == "__main__":
    ast_path = pathlib.Path("dat/cyp") / "q1.tsv"
    items = goedwig.load_ast(ast_path)

    for item in items:
        print(item)

    ic(goedwig.query_plan(items))
