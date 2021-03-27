# -*- coding: utf-8 -*-


class ParseError:
    def __init__(self, line: int, start_col: int, end_col: int):
        self.line = line
        self.start_col = start_col
        self.end_col = end_col
