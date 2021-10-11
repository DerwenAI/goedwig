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

    q = goedwig.QueryPlan()
    tsv_iter = iter(ast_path.open(encoding="utf-8").readlines())
    q.load_ast(tsv_iter)

    for item in q.items:
        print(item)

    q.parse_items()
    print(q)

    assert len(q.items) == 14
    assert q.items[-1].literal == "p"
