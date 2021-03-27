#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

from application import Application


def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = Application(master=root, title="Graphics Editor")
    app.mainloop()


if __name__ == "__main__":
    main()
