#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Query planning.
"""

import csv
import pathlib
import typing

from icecream import ic


class CypherItem:
    ordinal: int = -1
    parent: int = -1
    depth: int = -1
    s0: int = -1
    s1: int = -1
    ast_typestr: str = None
    literal: str = ""
    children: typing.List[int] = None

    def __repr__ (
        self,
        ) -> str:
        """
Printed representation for an AST item.
        """
        kiddos = str(self.children)
        return f"@{self.ordinal}[{self.parent}]\t{self.s0}..{self.s1}\t{self.depth:<4}{kiddos:<10}{self.ast_typestr:<16} |> {self.literal}"


def load_ast (
    ast_path: pathlib.Path,
    ) -> typing.List[CypherItem]:
    """
Load a TSV file of AST items.
    """
    items: typing.List[CypherItem] = []

    with open(ast_path, "r") as f:
        for row in csv.reader(f, delimiter="\t"):
            ordinal, parent, depth, s0, s1, ast_typestr, literal = row

            item = CypherItem()
            item.ordinal = int(ordinal)
            item.parent = int(parent)
            item.depth = int(depth)
            item.s0 = int(s0)
            item.s1 = int(s1)
            item.ast_typestr = ast_typestr
            item.literal = literal
            item.children = []

            # back-link the parent item
            if item.parent >= 0:
                items[item.parent].children.append(item.ordinal)

            items.append(item)

    return items


def query_plan (  # pylint: disable=R0914,W0621
    items: typing.List[CypherItem],
    ) -> typing.Any:
    """
Develop a query plan from the given AST items.

(THIS NEEDS LOTS OF WORK)
    """
    i = 0

    while i < len(items):
        if items[i].ast_typestr == "statement":
            break

        i += 1

    # at "statement"
    query_i = items[i].children[0]
    # at "query"
    match_i, ret_i = items[query_i].children

    pat_i = items[match_i].children[0]
    pat_path_i = items[pat_i].children[0]
    node_pat_i = items[pat_path_i].children[0]

    ident_i, map_i = items[node_pat_i].children
    node_name = items[ident_i].literal  # pylint: disable=W0621

    prop_i, val_i = items[map_i].children
    prop_key = items[prop_i].literal  # pylint: disable=W0621
    prop_val = items[val_i].literal.strip("'")  # pylint: disable=W0621

    proj_i = items[ret_i].children[0]
    ident_i = items[proj_i].children[0]
    ret_name = items[ident_i].literal  # pylint: disable=W0621

    return node_name, prop_key, prop_val, ret_name
