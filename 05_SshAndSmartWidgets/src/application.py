# -*- coding: utf-8 -*-

import tkinter as tk
from typing import List

from ParseError import ParseError
from geometry_syntax import GeometrySyntax
from oval_parameters import OvalParameters
from preview import Preview


class Application(tk.Frame):
    _syntax_error_tag = "syntax_error"

    def __init__(self, master, title: str):
        super().__init__(master)
        self._master = master
        self._text = ""

        self.grid(sticky="NEWS")
        self.columnconfigure(0, weight=1, uniform="app_column")
        self.columnconfigure(1, weight=1, uniform="app_column")
        self.rowconfigure(0, weight=1)

        self.winfo_toplevel().title(title)
        self._create_widgets()
        self._bind_event_handlers()

    def _create_widgets(self):
        editor_frame = tk.LabelFrame(self, text="Editor")
        editor_frame.grid(row=0, column=0, sticky="NEWS")
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)

        preview_frame = tk.LabelFrame(self, text="Preview")
        preview_frame.grid(row=0, column=1, sticky="NEWS")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        self.__text_field = tk.Text(
            editor_frame,
            undo=True,
            wrap=tk.WORD,
            font="fixed",
        )
        self.__text_field.grid(sticky="NEWS")
        self.__text_field.tag_config(
            self._syntax_error_tag, background="red", foreground="white"
        )

        self.__preview = Preview(
            preview_frame, self._on_new_figure_created, self._on_figure_updated
        )

    def _bind_event_handlers(self):
        self.__text_field.bind("<Leave>", lambda _: self._on_update_text())
        self.__text_field.bind("<FocusOut>", lambda _: self._on_update_text())
        self.__text_field.bind("<Key-Return>", lambda _: self._on_update_text())
        # FIXME: remove syntax error when line is edited

    def _on_update_text(self):
        self._remove_syntax_errors()
        self._text = self.__text_field.get("0.0", tk.END)
        figures, errs = GeometrySyntax.parse(self._text)
        self._display_errors(errs)
        self.__preview.draw_figures(figures)

    def _display_errors(self, errors: List[ParseError]):
        self._remove_syntax_errors()
        for err in errors:
            self.__text_field.tag_add(
                self._syntax_error_tag,
                f"{err.line+1}.{err.start_col}",
                f"{err.line+1}.{err.end_col}",
            )

    def _remove_syntax_errors(self):
        x = self.__text_field.tag_ranges(self._syntax_error_tag)
        for i in x:
            self.__text_field.tag_remove(self._syntax_error_tag, i)

    def _on_new_figure_created(self, params: OvalParameters):
        new_lines = GeometrySyntax.serialize([params])
        self.__text_field.insert(tk.END, "\n" + new_lines)
        self._on_update_text()

    def _on_figure_updated(self, idx: int, params: OvalParameters):
        # FIXME:
        pass

    def _on_exit(self):
        self._master.destroy()
