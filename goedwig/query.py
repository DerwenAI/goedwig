#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Query planning.
"""

from collections.abc import Iterator
import typing

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611

from .cypher import CypherItem


class NodeVariable:  # pylint: disable=R0903
    """
Represent a node variable within a query.
    """
    def __init__ (
        self,
        name: str,
        item: int,
        ) -> None:
        """
Constructor.
        """
        self.name: str = name
        self.item: int = item


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "name": self.name,
            "item": self.item,
        }

        return str(_repr)


class PredicateMap:  # pylint: disable=R0903
    """
Represent a predicate that maps a property key/value pair onto a variable.
    """
    def __init__ (
        self,
        var: typing.Any,
        key: str,
        val: str,
        ) -> None:
        """
Constructor.
        """
        self.var: typing.Any = var
        self.key: str = key
        self.val: str = val


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "name": self.var.name,
            "key": self.key,
            "val": self.val,
        }

        return str(_repr)


class ProjectionElement:  # pylint: disable=R0903
    """
Represent an element of the returned projection.
    """
    def __init__ (
        self,
        name: str,
        prop: typing.Optional[str],
        ) -> None:
        """
Constructor.
        """
        self.name: str = name
        self.prop: typing.Optional[str] = prop


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "name": self.name,
            "prop": self.prop,
        }

        return str(_repr)


class QueryPlan:
    """
Manage the lifecycle of a query plan.
    """
    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.items: typing.List[CypherItem] = []
        self.bindings: typing.Dict[str, typing.Any] = {}
        self.predicates: typing.List[PredicateMap] = []
        self.projections: typing.List[ProjectionElement] = []


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "bindings": self.bindings,
            "predicates": self.predicates,
            "projections": self.projections,
        }

        return str(_repr)


    def load_ast (
        self,
        tsv_iter: Iterator,
        ) -> "QueryPlan":
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

        # support method chaining
        return self


    def parse_items (
        self,
        *,
        i: int = 0,
        ) -> None:
        """
Develop a query plan from the given AST items, traversed using
recursive descent.
        """
        typestr = self.items[i].ast_typestr

        if typestr in ["line_comment"]:
            # ignore
            pass

        elif typestr == "statement":
            ## for now, only handle the "query" statements
            if self.items[i + 1].ast_typestr == "query":
                match_i, return_i = self.items[i + 1].children

                for j in self.items[match_i].children:
                    self.parse_items(i = j)

                for j in self.items[return_i].children:
                    self.parse_items(i = j)

        elif typestr == "pattern":
            # begin building a new predicate
            pat_i = self.items[i].children[0]
            self.parse_items(i = pat_i)

        elif typestr == "pattern path":
            # HERE: instantiate a triple/pattern and pass into recursion
            pat_path_i = self.items[i].children[0]
            self.parse_items(i = pat_path_i)

        elif typestr == "node pattern":
            # represent a node pattern
            ident_i, map_i = self.items[i].children

            node_var = NodeVariable(
                self.items[ident_i].literal,  # pylint: disable=W0621
                map_i,
                )

            self.bindings[node_var.name] = node_var

            ## selection
            prop_i, val_i = self.items[map_i].children

            pred = PredicateMap(
                node_var,
                self.items[prop_i].literal,  # pylint: disable=W0621
                self.items[val_i].literal.strip("'"),  # pylint: disable=W0621
            )

            self.predicates.append(pred)

        elif typestr == "projection":
            ## projection
            ident_i = self.items[i].children[0]

            proj_elem = ProjectionElement(
                self.items[ident_i].literal,  # pylint: disable=W0621
                None,
                )

            self.projections.append(proj_elem)
