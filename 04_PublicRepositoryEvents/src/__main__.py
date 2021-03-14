#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tk_msg

from Simplified import Application


class App(Application):
    def __init__(self, title: str, parent: tk.Tk):
        super().__init__(parent)
        self.__message = "Congratulations!\nYou've found a secret level!"
        self.winfo_toplevel().title(title)
        self.create_widgets()

    def create_widgets(self):
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind(
            "<Any-Key>",
            lambda event: tk_msg.showinfo(self.__message.split()[0], self.__message),
        )


def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = App(title="Sample application", parent=root)
    app.mainloop()


if __name__ == "__main__":
    main()
