#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cypher ASTs.
"""

import typing


class CypherItem:  # pylint: disable=R0902,R0903
    """
Represent data for one AST tree item in a parsed Cypher query.
    """
    REPR_STR = "@{:<3}[{:3}] {:3}..{:<3}\t{:<4}{:<16}{:<16} |> {}"

    def __init__ (
        self,
        row: typing.List[str],
        ) -> None:
        """
Constructor.
        """
        ordinal, parent, depth, s0, s1, ast_typestr, literal = row  # pylint: disable=C0103

        self.ordinal: int = int(ordinal)
        self.parent: int = int(parent)
        self.depth: int = int(depth)
        self.s0: int = int(s0)  # pylint: disable=C0103
        self.s1: int = int(s1)  # pylint: disable=C0103
        self.ast_typestr: str = ast_typestr
        self.literal: str = literal.strip()
        self.children: typing.List[int] = []


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        kiddos = ",".join(map(lambda x: str(x), self.children))  # pylint: disable=W0108

        return self.REPR_STR.format(
            self.ordinal,
            self.parent,
            self.s0,
            self.s1,
            self.depth,
            kiddos,
            self.ast_typestr,
            self.literal,
            )
