# -*- coding: utf-8 -*-

import tkinter as tk
from typing import Callable


class MenuBar(tk.LabelFrame):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        on_new_game: Callable[[], None],
        on_exit: Callable[[], None],
    ):
        super().__init__(parent, text="Menu")
        self.grid(sticky="NEWS")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self._new_btn = tk.Button(self, text="New", command=on_new_game)
        self._new_btn.grid(row=0, column=0)
        self._exit_btn = tk.Button(self, text="Exit", command=on_exit)
        self._exit_btn.grid(row=0, column=1)
