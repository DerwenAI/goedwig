#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample code.
"""

import json
import pathlib
import sys

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611
import goedwig


if __name__ == "__main__":
    filename = "q1.tsv"  # pylint: disable=C0103
    testing = False  # pylint: disable=C0103

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    # load the parsed AST trees
    q = goedwig.QueryPlan()
    ast_path = pathlib.Path("dat/cyp") / filename
    tsv_iter = iter(ast_path.open(encoding="utf-8").readlines())
    q.load_ast(tsv_iter)

    # print a representation
    print(goedwig.__version__)

    for item in q.items:
        print(item)

    # define a query plan
    q.parse_items(debug=True)
    plan = eval(str(q))  # pylint: disable=W0123
    print(json.dumps(plan, indent=1, sort_keys=False))

    # testing assertions
    if testing:
        assert len(q.items) == 14
        assert q.items[-1].literal == "p"
