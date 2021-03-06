# -*- coding: utf-8 -*-

import tkinter as tk
from typing import Callable, List, Set

from direction import Direction


class GameField(tk.LabelFrame):
    _size = 4
    _cell_count = _size * _size - 1

    def __init__(self, parent, *, on_win: Callable[[], None]):
        super().__init__(parent, text="App")
        self._on_win = on_win
        self.grid(sticky="NEWS")
        for i in range(self._size):
            self.columnconfigure(i, weight=1, uniform="game_field_column")
            self.rowconfigure(i, weight=1, uniform="game_field_row")

        self.__cells: List[tk.Button] = []
        self.reset_field()

    def reset_field(self):
        self.__generate_field()
        while self._is_game_won():
            # NOTE: В случае, если сгенерированное поле удовлетворяет условию выигрыша, перегенерируем его
            self.__generate_field()

    def __generate_field(self):
        for c in self.__cells:
            c.destroy()

        # TODO: generate random positions
        self.__cells = [
            self._create_button_at_position(
                i, column=i // self._size, row=i % self._size
            )
            for i in range(self._cell_count)
        ]

    def _create_button_at_position(self, label: int, *, column: int, row: int):
        # TODO: use a separate class for a cell
        text = f"{label}"
        btn = tk.Button(self, text=text, command=lambda: self._on_cell_click(text))
        btn.grid(sticky="NEWS", row=row, column=column)
        return btn

    def _on_cell_click(self, text: str):
        found = list(filter(lambda c: c.cget("text") == text, self.__cells))
        if len(found) == 0:
            return
        clicked_cell = found[0]
        self._move_cell(clicked_cell)
        if self._is_game_won():
            self._on_win()

    def _move_cell(self, cell: tk.Button):
        # TODO: prettify move logic
        cell_info = cell.grid_info()
        cell_i, cell_j = cell_info["row"], cell_info["column"]
        filled_directions: Set[Direction] = set()
        for c in self.__cells:
            info = c.grid_info()
            i, j = info["row"], info["column"]
            if j - cell_j == 0:
                if i - cell_i == 1:
                    filled_directions.add(Direction.DOWN)
                elif i - cell_i == -1:
                    filled_directions.add(Direction.UP)
            elif i - cell_i == 0:
                if j - cell_j == 1:
                    filled_directions.add(Direction.RIGHT)
                elif j - cell_j == -1:
                    filled_directions.add(Direction.LEFT)
        if cell_j == self._size - 1:
            filled_directions.add(Direction.RIGHT)
        if cell_j == 0:
            filled_directions.add(Direction.LEFT)
        if cell_i == self._size - 1:
            filled_directions.add(Direction.DOWN)
        if cell_i == 0:
            filled_directions.add(Direction.UP)

        empty_direction = Direction.all_directions() - filled_directions
        if len(empty_direction) == 0:
            return
        free_direction = list(empty_direction)[0]
        if free_direction == Direction.LEFT:
            cell_j -= 1
        elif free_direction == Direction.RIGHT:
            cell_j += 1
        elif free_direction == Direction.UP:
            cell_i -= 1
        elif free_direction == Direction.DOWN:
            cell_i += 1
        cell.grid(row=cell_i, column=cell_j)

    def _is_game_won(self):
        # TODO: implement winning conditions
        return False
