# -*- coding: utf-8 -*-

import tkinter as tk
from collections import namedtuple
from typing import Dict, Union, Callable, Any

import re

_AxisParams = namedtuple("_AxisParams", ["position", "weight", "span"])


class Application(tk.Frame):
    __geom_axis_re = re.compile(
        r"^(?P<position>\d+)(\.(?P<weight>\d+)|)(\+(?P<span>\d+)|)$"
    )
    __geom_re = re.compile(
        r"^(?P<row>[0-9.+]+):(?P<column>[0-9.+]+)(/(?P<sticky>[SEWN]+)|)$"
    )

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.__children: Dict[str, tk.Widget] = {}
        self.grid(sticky="NEWS")

    def __getattr__(self, item) -> Union[tk.Widget, Callable[[Any, Any], tk.Widget]]:
        if item in self.__children:
            return self.__children[item]

        app = self
        widget_name = item
        parent = app
        if "." in item:
            parent_name, widget_name = item.rsplit(".", 2)
            if parent_name not in self.__children:
                raise RuntimeError(f"Parent widget '{parent_name}' does not exist")
            parent = self.__children[parent_name]

        def create_object(cls, geom: str, **kwargs) -> tk.Widget:
            class Wrapper(cls):
                def __init__(self, master: tk.Widget, name: str):
                    super().__init__(master=master, **kwargs)
                    self.__name = name

                def __getattr__(
                    self, it
                ) -> Union[tk.Widget, Callable[[Any, Any], tk.Widget]]:
                    return getattr(app, f"{self.__name}.{it}")

            obj = Wrapper(parent, name=widget_name)
            try:
                self._setup_geometry(obj, geom)
            except RuntimeError as err:
                obj.destroy()
                raise err
            if item in self.__children:
                raise RuntimeError(f"Widget '{item}' already exists")
            self.__children[item] = obj
            return obj

        return create_object

    def _setup_geometry(self, obj: tk.Widget, geom: str):
        geom_match = self.__geom_re.match(geom)
        if not geom_match:
            raise RuntimeError(f"Invalid geometry: '{geom}'")
        row_pattern = geom_match["row"]
        column_pattern = geom_match["column"]

        if geom_match["sticky"] is not None:
            obj.grid(sticky=geom_match["sticky"])

        row = self._parse_axis_configuration(row_pattern)
        column = self._parse_axis_configuration(column_pattern)

        obj.grid(
            column=column.position,
            row=row.position,
            rowspan=1 + row.span,
            columnspan=1 + column.span,
        )
        obj.master.rowconfigure(row.position, weight=row.weight)
        obj.master.columnconfigure(column.position, weight=column.weight)

    def _parse_axis_configuration(self, params: str) -> _AxisParams:
        match = self.__geom_axis_re.match(params)
        if not match:
            raise RuntimeError(f"Invalid axis configuration: '{params}'")
        return _AxisParams(
            position=int(match["position"]),
            weight=int(match["weight"]) if match["weight"] is not None else 1,
            span=int(match["span"]) if match["span"] is not None else 0,
        )
