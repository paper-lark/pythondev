# -*- coding: utf-8 -*-

import tkinter as tk
from typing import List, Callable, Dict
import math

from oval_parameters import OvalParameters


class Preview(tk.Canvas):
    def __init__(
        self,
        master,
        on_figure_created: Callable[[OvalParameters], None],
        on_figure_updated: Callable[[OvalParameters], None],
    ):
        super().__init__(master)
        self._on_figure_created = on_figure_created
        self._on_figure_updated = on_figure_updated
        self._previous_point = None
        self._new_figure = None
        self._moved_figure = None
        self._id_by_obj_id = {}

        self.grid(sticky="NEWS")
        self.bind("<Button>", self._on_mouse_pressed)
        self.bind("<Motion>", self._on_mouse_move)
        self.bind("<ButtonRelease>", self._on_mouse_released)

    def draw_figures(self, figures: List[OvalParameters]) -> List[int]:
        self.remove_figures()
        failed_ids: List[int] = []
        for f in figures:
            try:
                oval_id = self.create_oval(
                    f.x0,
                    f.y0,
                    f.x1,
                    f.y1,
                    fill=f.fill_color,
                    outline=f.outline_color,
                    width=f.outline_width,
                )
                self._id_by_obj_id[oval_id] = f.id
            except tk.TclError:
                failed_ids.append(f.id)
        # FIXME: if failed to create oval, highlight error
        return failed_ids

    def remove_figures(self):
        for obj in self.find_all():
            self.delete(obj)
        self._id_by_obj_id = {}
        self._reset_action_state()

    def _reset_action_state(self):
        if self._new_figure is not None:
            self.delete(self._new_figure)
        self._moved_figure = None
        self._new_figure = None

    def _on_mouse_pressed(self, event):
        # reset possible state
        self._reset_action_state()

        # check if there is a figure to move
        overlapping_figures = self.find_overlapping(
            event.x, event.y, event.x + 1, event.y + 1
        )
        if len(overlapping_figures) > 0:
            self._moved_figure = overlapping_figures[0]
            self._previous_point = (event.x, event.y)
            return

        # create new figure
        self._new_figure = self.create_oval(event.x, event.y, event.x, event.y)
        self._previous_point = (event.x, event.y)

    def _on_mouse_move(self, event):
        if event.state & 0x0100 == 0:
            return

        if self._moved_figure is not None:
            # move figure
            if event.state & 0x0100 != 0 and self._previous_point is not None:
                self.move(
                    self._moved_figure,
                    event.x - self._previous_point[0],
                    event.y - self._previous_point[1],
                )
                self._previous_point = (event.x, event.y)

        elif self._new_figure is not None:
            # scale new figure
            x0, y0, x1, y1 = self.coords(self._new_figure)
            self.delete(self._new_figure)
            self._new_figure = self.create_oval(
                self._previous_point[0],
                self._previous_point[1],
                event.x,
                event.y,
            )

    def _on_mouse_released(self, event):
        if self._moved_figure is not None:
            # submit changes
            params = self._get_figure_params(self._moved_figure)
            self.delete(self._moved_figure)
            if params.id > 0:
                self._on_figure_updated(params)

        elif self._new_figure is not None:
            # submit new figure
            params = self._get_figure_params(self._new_figure)
            self.delete(self._new_figure)
            self._on_figure_created(params)

        # reset state
        self._reset_action_state()

    def _get_figure_params(self, figure_id) -> OvalParameters:
        x0, y0, x1, y1 = self.coords(figure_id)
        return OvalParameters(
            id=self._id_by_obj_id[figure_id] if figure_id in self._id_by_obj_id else 0,
            x0=int(float(x0)),
            y0=int(float(y0)),
            x1=int(float(x1)),
            y1=int(float(y1)),
            fill_color=self.itemcget(figure_id, "fill"),
            outline_width=int(float(self.itemcget(figure_id, "width"))),
            outline_color=self.itemcget(figure_id, "outline"),
        )
