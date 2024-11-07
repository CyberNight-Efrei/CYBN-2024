import base64
from graphviz import Source
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)
from sympy.printing.dot import dotprint
import typing


abc_dict: dict[str, typing.Any] = {}
functions_dict: dict[str, typing.Any] = {}
core_dict: dict[str, typing.Any] = {}

exec("from sympy.abc import *", abc_dict)
exec("from sympy.functions import *", functions_dict)
exec("from sympy.core import *", core_dict)

global_dict = abc_dict | functions_dict | core_dict

del global_dict["__builtins__"]


def convert_expr(argument: str) -> typing.Any:
    parsed_arg = parse_expr(
        argument,
        transformations=(
            standard_transformations
            + (implicit_multiplication_application,)
        ),
        evaluate=False,
        global_dict=global_dict,
    )

    return parsed_arg


def graph_expr(expr: typing.Any) -> str:
    digraph = dotprint(expr)
    raw_bytes = Source(digraph).pipe(format="png")

    return base64.b64encode(raw_bytes).decode()
