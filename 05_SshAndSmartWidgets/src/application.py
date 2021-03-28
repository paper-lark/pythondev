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

    def _on_update_text(self):
        self._remove_syntax_errors()
        text = self.__text_field.get("1.0", tk.END)
        figures, errs = GeometrySyntax.parse(text)
        failed_line_no = self.__preview.draw_figures(figures)
        errs += list(map(lambda l: ParseError(line=l), failed_line_no))
        self._display_errors(errs)

    def _display_errors(self, errors: List[ParseError]):
        self._remove_syntax_errors()
        for err in errors:
            self.__text_field.tag_add(
                self._syntax_error_tag,
                f"{err.line}.0",
                f"{err.line}.0 + 1l - 1c",
            )

    def _remove_syntax_errors(self):
        x = self.__text_field.tag_ranges(self._syntax_error_tag)
        for start, end in zip(x[::2], x[1::2]):
            self.__text_field.tag_remove(self._syntax_error_tag, start, end)

    def _on_new_figure_created(self, params: OvalParameters):
        new_text = GeometrySyntax.serialize([params])
        line_count = self._count_lines()
        if (
            len(self.__text_field.get(f"{line_count}.0", f"{line_count}.0 + 1l - 1c"))
            > 0
        ):
            new_text = "\n" + new_text
        self.__text_field.insert(tk.END, new_text)
        self._on_update_text()

    def _on_figure_updated(self, params: OvalParameters):
        new_text = GeometrySyntax.serialize([params])
        edited_line = params.id
        line_count = self._count_lines()
        if line_count >= edited_line:
            start = f"{edited_line}.0"
            end = f"{edited_line}.0 + 1l - 1c"
            self.__text_field.delete(start, end)
            self.__text_field.insert(start, new_text)
            self._on_update_text()

    def _count_lines(self) -> int:
        return int(self.__text_field.index(tk.END + "-1c").split(".")[0])

    def _on_exit(self):
        self._master.destroy()
