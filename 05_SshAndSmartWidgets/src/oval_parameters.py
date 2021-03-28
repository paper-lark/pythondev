# -*- coding: utf-8 -*-


class OvalParameters:
    def __init__(
        self,
        id: int,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        outline_width: int,
        outline_color: str,
        fill_color: str,
    ):
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.fill_color = fill_color

    def __str__(self):
        return f"OvalParameters(id={self.id}, x0={self.x0}, y0={self.y0}, x1={self.x1}, y1={self.y1}, outline_width={self.outline_width}, outline_color={self.outline_color}, fill_color={self.fill_color})"
