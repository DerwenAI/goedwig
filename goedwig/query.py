#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Query planning.
"""

from collections.abc import Iterator
import typing

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611

from .cypher import CypherItem


class Variable:  # pylint: disable=R0903
    """
Represent a node or edge variable within a query.
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
        self.predicates: typing.List[Predicate] = []


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "name": self.name,
            "item": self.item,
            "predicates": self.predicates,
        }

        return str(_repr)


class Predicate:  # pylint: disable=R0903
    """
Represent a simple predicate.
    """
    def __init__ (
        self,
        var: Variable,
        ) -> None:
        """
Constructor.
        """
        self.var: Variable = var


class PredicateMap (Predicate):  # pylint: disable=R0903
    """
Represent a predicate that maps a property key/value pair onto a variable.
    """
    def __init__ (
        self,
        var: Variable,
        key: str,
        val: str,
        ) -> None:
        """
Constructor.
        """
        super().__init__(var)
        self.key: str = key
        self.val: str = val


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "kind": "map",
            "key": self.key,
            "val": self.val,
        }

        return str(_repr)


class PredicateLabel (Predicate):  # pylint: disable=R0903
    """
Represent a predicate that specifies a label.
    """
    def __init__ (
        self,
        var: Variable,
        label: str,
        ) -> None:
        """
Constructor.
        """
        super().__init__(var)
        self.label: str = label


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "kind": "label",
            "label": self.label,
        }

        return str(_repr)


class PredicateDirection (Predicate):  # pylint: disable=R0903
    """
Represent a predicate that specifies a direction.
    """
    def __init__ (
        self,
        var: Variable,
        direction: str,
        ) -> None:
        """
Constructor.
        """
        super().__init__(var)
        self.direction: str = direction


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "kind": "direction",
            "dir": self.direction,
        }

        return str(_repr)


class Path:  # pylint: disable=R0903
    """
Represent a path pattern, with multiple node/edge/regex elements.
    """
    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.elem: list = []


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        return str(self.elem)


class ProjectionElement:  # pylint: disable=R0903
    """
Represent an element of the returned projection.
    """
    def __init__ (
        self,
        bind: typing.Optional[str],
        prop: typing.Optional[str],
        alias: typing.Optional[str],
        ) -> None:
        """
Constructor.
        """
        self.bind: typing.Optional[str] = bind
        self.prop: typing.Optional[str] = prop
        self.alias: typing.Optional[str] = alias


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "bind": self.bind,
            "prop": self.prop,
            "alias": self.alias,
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
        self.blank_count: int = 0

        self.bindings: typing.Dict[str, Variable] = {}
        self.paths: typing.List[Path] = []
        self.projections: typing.List[ProjectionElement] = []


    def __repr__ (
        self,
        ) -> str:
        """
Text representation.
        """
        _repr = {
            "bindings": self.bindings,
            "paths": self.paths,
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


    def blankify (
        self,
        ident_lit: str,
        ) -> str:
        """
Represent a unique name for a blank node or edge.
        """
        if len(ident_lit) < 1:
            ident_lit = "blank_{}".format(self.blank_count)
            self.blank_count += 1

        return ident_lit


    def parse_items (  # pylint: disable=R0912,R0914,R0915
        self,
        *,
        i: int = 0,
        debug: bool = False,
        ) -> typing.Optional[typing.Any]:
        """
Develop a query plan from the given AST items, using recursive
descent to traverse them.
        """
        typestr = self.items[i].ast_typestr

        if debug:
            ic(i, typestr)
            print("", self.items[i].children)

        if typestr in ["line_comment"]:
            # ignore
            pass

        elif typestr == "statement":
            ## for now, only handle the "query" statements
            if self.items[i + 1].ast_typestr == "query":
                match_i, return_i = self.items[i + 1].children

                for j in self.items[match_i].children:
                    self.parse_items(i = j, debug=debug)

                for j in self.items[return_i].children:
                    self.parse_items(i = j, debug=debug)

        elif typestr == "pattern":
            # begin building a new predicate @ child
            pat_i = self.items[i].children[0]
            self.parse_items(i = pat_i, debug=debug)

        elif typestr == "pattern path":
            # populate a path pattern
            path = Path()
            self.paths.append(path)

            for j in self.items[i].children:
                child_type = self.items[j].ast_typestr

                if child_type == "node pattern":
                    path.elem.append(self.parse_items(i = j, debug=debug))

                elif child_type == "rel pattern":
                    path.elem.append(self.parse_items(i = j, debug=debug))

            return path


        elif typestr == "node pattern":
            # represent a node pattern
            ident_i = self.items[i].children[0]
            ident_lit = self.blankify(self.items[ident_i].literal)

            node_var = Variable(ident_lit, i)
            self.bindings[ident_lit] = node_var

            ## selection
            for j in self.items[i].children[1:]:
                child_type = self.items[j].ast_typestr

                if child_type == "label":
                    node_var.predicates.append(PredicateLabel(
                        node_var,
                        self.items[j].literal.strip(":"),
                    ))

                elif child_type == "map":
                    key_i, val_i = self.items[j].children

                    node_var.predicates.append(PredicateMap(
                        node_var,
                        self.items[key_i].literal,  # pylint: disable=W0621
                        self.items[val_i].literal.strip("'"),  # pylint: disable=W0621
                    ))

            return node_var

        elif typestr == "rel pattern":
            # represent a rel pattern
            ident_i = self.items[i].children[0]
            ident_lit = self.blankify(self.items[ident_i].literal)

            edge_var = Variable(ident_lit, i)
            self.bindings[ident_lit] = edge_var

            ## selection
            for j in self.items[i].children[1:]:
                child_type = self.items[j].ast_typestr

                if child_type == "label":
                    edge_var.predicates.append(PredicateLabel(
                        edge_var,
                        self.items[j].literal.strip(":"),
                    ))

                elif child_type == "map":
                    key_i, val_i = self.items[j].children

                    edge_var.predicates.append(PredicateMap(
                        edge_var,
                        self.items[key_i].literal,  # pylint: disable=W0621
                        self.items[val_i].literal.strip("'"),  # pylint: disable=W0621
                    ))

                elif child_type == "rel type":
                    edge_var.predicates.append(PredicateDirection(
                        edge_var,
                        self.items[j].literal.strip(":"),
                    ))

            return edge_var

        elif typestr == "projection":
            ## projection
            bind_lit = None
            prop_lit = None
            alias_lit = None

            for j in self.items[i].children:
                child_type = self.items[j].ast_typestr

                if child_type == "identifier":
                    alias_lit = self.items[j].literal.strip("`")

                elif child_type == "property":
                    ident_i, prop_i = self.items[j].children
                    bind_lit = self.items[ident_i].literal
                    prop_lit = self.items[prop_i].literal

            if not bind_lit:
                # direct reference; no alias given
                bind_lit = alias_lit

            self.projections.append(ProjectionElement(bind_lit, prop_lit, alias_lit))

        return None
