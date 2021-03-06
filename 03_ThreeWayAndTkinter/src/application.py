# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tk_msg

from game_field import GameField
from menubar import MenuBar


class Application(tk.Frame):
    _title = "Game of 15"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.winfo_toplevel().title(self._title)
        self.grid(sticky="NEWS")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.__menu = MenuBar(
            self, on_new_game=self._on_new_game, on_exit=self._on_exit
        )
        self.__menu.grid(row=0, column=0)
        self.__game_field = GameField(self, on_win=self._on_win)
        self.__game_field.grid(row=1, column=0)

    def _on_new_game(self):
        self.__game_field.reset_field()

    def _on_win(self):
        tk_msg.showinfo(self._title, "You won!")
        self._on_new_game()

    def _on_exit(self):
        self._parent.destroy()
