# -*- coding: utf-8 -*-
import functools
import operator
import random
import tkinter as tk
import itertools
from typing import Callable, List

from cell import Cell
from direction import Direction


class GameField(tk.Frame):
    _size = 4
    _cell_count = _size * _size - 1

    def __init__(self, parent, *, on_win: Callable[[], None]):
        super().__init__(parent)
        self._on_win = on_win
        self.grid(sticky="NEWS")
        for i in range(self._size):
            self.columnconfigure(i, weight=1, uniform="game_field_column")
            self.rowconfigure(i, weight=1, uniform="game_field_row")

        self.__cells: List[Cell] = []
        self.reset_field()

    def reset_field(self):
        self.__generate_field()
        while self._is_game_won() or self._is_unsolvable():
            # NOTE: В случае, если сгенерированное поле удовлетворяет условию выигрыша или нерешаемо,
            #   перегенерируем его
            self.__generate_field()

    def __generate_field(self):
        for c in self.__cells:
            c.destroy()

        positions = self._get_all_positions()
        random.shuffle(positions)

        self.__cells = [
            Cell(
                self,
                cell_id=i + 1,
                row=positions[i][0],
                column=positions[i][1],
                on_click=self._on_cell_click,
            )
            for i in range(self._cell_count)
        ]

    def _on_cell_click(self, cell: Cell):
        self._move_cell(cell)
        if self._is_game_won():
            self._on_win()

    def _move_cell(self, cell: Cell):
        # find possible directions
        possible_directions = Direction.all_directions()
        for c in self.__cells:
            if c.column - cell.column == 0:
                if c.row - cell.row == 1:
                    possible_directions.remove(Direction.DOWN)
                elif c.row - cell.row == -1:
                    possible_directions.remove(Direction.UP)
            elif c.row - cell.row == 0:
                if c.column - cell.column == 1:
                    possible_directions.remove(Direction.RIGHT)
                elif c.column - cell.column == -1:
                    possible_directions.remove(Direction.LEFT)
        if cell.column == self._size - 1:
            possible_directions.remove(Direction.RIGHT)
        if cell.column == 0:
            possible_directions.remove(Direction.LEFT)
        if cell.row == self._size - 1:
            possible_directions.remove(Direction.DOWN)
        if cell.row == 0:
            possible_directions.remove(Direction.UP)

        # move if possible
        if len(possible_directions) == 0:
            return
        cell.move(list(possible_directions)[0])

    def _is_game_won(self):
        return functools.reduce(
            operator.and_,
            map(lambda c: self._is_positioned_correctly(c), self.__cells),
            True,
        )

    def _is_unsolvable(self) -> bool:
        all_positions = set(self._get_all_positions())
        occupied_positions = set(map(lambda c: (c.row, c.column), self.__cells))
        free_position = list(all_positions - occupied_positions)[0]

        score = (
            1
            + free_position[0]
            + functools.reduce(
                operator.add,
                map(
                    lambda pair: 1 if self._is_cells_permuted(pair[0], pair[1]) else 0,
                    itertools.product(self.__cells, repeat=2),
                ),
                0,
            )
        )
        return score % 2 == 1

    @classmethod
    def _is_positioned_correctly(cls, cell: Cell):
        return cell.id == cell.row * cls._size + cell.column + 1

    @classmethod
    def _get_all_positions(cls):
        return list(itertools.product(range(cls._size), repeat=2))

    @staticmethod
    def _is_cells_permuted(cell: Cell, other: Cell):
        return other.id > cell.id and (
            other.row < cell.row or other.row == cell.row and other.column < cell.column
        )
