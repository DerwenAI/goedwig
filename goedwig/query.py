#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Query planning.
"""

from collections.abc import Iterator
import typing

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611

from .cypher import CypherItem


class Query:
    """
Manage the lifecycle of query plan.
    """
    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.items: typing.List[CypherItem] = []
        self.bindings: dict = {}


    def load_ast (
        self,
        tsv_iter: Iterator,
        ) -> None:
        """
Load a TSV file of AST items.
        """
        for tsv_row in tsv_iter:
            row = tsv_row.split("\t")
            item = CypherItem(row)

            # back-link the parent item
            if item.parent >= 0:
                self.items[item.parent].children.append(item.ordinal)

            self.items.append(item)


    def query_plan (  # pylint: disable=R0914
        self,
        ) -> typing.Tuple[str, str, str, str]:
        """
Develop a query plan from the given AST items.
        """
        i = 0

        while i < len(self.items):
            if self.items[i].ast_typestr == "statement":
                break

            i += 1

        query_i = self.items[i].children[0]
        match_i, ret_i = self.items[query_i].children

        ## bindings
        pat_i = self.items[match_i].children[0]
        pat_path_i = self.items[pat_i].children[0]
        node_pat_i = self.items[pat_path_i].children[0]

        ident_i, map_i = self.items[node_pat_i].children
        node_name = self.items[ident_i].literal  # pylint: disable=W0621

        self.bindings[node_name] = map_i

        ## selection
        prop_i, val_i = self.items[map_i].children
        prop_key = self.items[prop_i].literal  # pylint: disable=W0621
        prop_val = self.items[val_i].literal.strip("'")  # pylint: disable=W0621

        ## projection
        proj_i = self.items[ret_i].children[0]
        ident_i = self.items[proj_i].children[0]
        ret_name = self.items[ident_i].literal  # pylint: disable=W0621

        print(self.bindings)

        return (node_name, prop_key, prop_val, ret_name)
