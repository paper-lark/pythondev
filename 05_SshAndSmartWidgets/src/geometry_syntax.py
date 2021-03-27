# -*- coding: utf-8 -*-
import re
import functools
from typing import Tuple, List, Any

from ParseError import ParseError
from oval_parameters import OvalParameters


class GeometrySyntax:
    _figure_re = re.compile(
        r"^\((?P<x0>\-?\d+);\s*(?P<y0>\-?\d+)\)\s*\((?P<x1>\-?\d+);(?P<y1>\-?\d+)\)\s*"
        r"(?P<fill_color>\w+|)\s*\+(?P<outline_width>\-?\d+)\s+"
        r"(?P<outline_color>\w+)$"
    )
    _color_re = re.compile(r"")

    # noinspection PyTypeChecker
    @classmethod
    def parse(cls, text: str) -> Tuple[List[OvalParameters], List[ParseError]]:
        return tuple(
            map(
                cls.__filter_empty,
                cls.__group_results(
                    map(
                        lambda l: cls._parse_line(l[0], l[1]),
                        enumerate(text.splitlines()),
                    )
                ),
            )
        )

    @classmethod
    def serialize(cls, params: List[OvalParameters]) -> str:
        return "\n".join(
            map(
                lambda p: f"({p.x0};{p.y0}) ({p.x1};{p.y1}) {p.fill_color} +{p.outline_width} {p.outline_color}",
                params,
            )
        )

    @classmethod
    def _parse_line(cls, line_no: int, line: str):
        if len(line) == 0:
            return None, None

        match = cls._figure_re.match(line)
        if not match:
            # FIXME: highlight specific invalid part
            return None, ParseError(line=line_no, start_col=0, end_col=len(line))
        return (
            OvalParameters(
                x0=int(match.group("x0")),
                y0=int(match.group("y0")),
                x1=int(match.group("x1")),
                y1=int(match.group("y1")),
                fill_color=match.group("fill_color"),
                outline_width=int(match.group("outline_width")),
                outline_color=match.group("outline_color"),
            ),
            None,
        )

    @staticmethod
    def __filter_empty(l):
        return list(filter(lambda x: x is not None, l))

    @staticmethod
    def __group_results(results):
        return functools.reduce(
            lambda acc, current: (
                acc[0] + [current[0]],
                acc[1] + [current[1]],
            ),
            results,
            ([], []),
        )


if __name__ == "__main__":
    i = (
        "(0;0) (10;20) #AAAAAA +0 #FFFFFF\n"
        "(;200) #AAAAAA +1 #FFFFFF\n"
        "(100;200) (100;200) #AAAAAA +1 #FFFFFF"
    )
    result = GeometrySyntax.parse(i)
    print(result[0])
    print(result[1])
