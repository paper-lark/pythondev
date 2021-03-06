# -*- coding: utf-8 -*-

from __future__ import annotations
import tkinter as tk
from typing import Callable

from direction import Direction


class Cell(tk.Button):
    def __init__(
        self,
        parent: tk.Widget,
        id: int,
        row: int,
        column: int,
        on_click: Callable[[Cell], None],
    ):
        super().__init__(parent, text=f"{id}", command=lambda: on_click(self))
        self._id = id
        self._row = row
        self._column = column
        self.grid(sticky="NEWS", row=row, column=column)

    @property
    def id(self) -> int:
        return self._id

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self._column -= 1
        elif direction == Direction.RIGHT:
            self._column += 1
        elif direction == Direction.UP:
            self._row -= 1
        elif direction == Direction.DOWN:
            self._row += 1
        self.grid(sticky="NEWS", row=self._row, column=self._column)
