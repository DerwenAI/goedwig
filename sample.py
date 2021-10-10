#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample code.
"""

import pathlib

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611
import goedwig


if __name__ == "__main__":
    print(goedwig.__version__)

    ast_path = pathlib.Path("dat/cyp") / "q1.tsv"

    q = goedwig.Query()
    q.load_ast(ast_path)

    for item in q.items:
        print(item)

    ic(q.query_plan())
