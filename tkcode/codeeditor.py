"""
Author: rdbende
License: GNU GPLv3
Copyright: 2021 rdbende
"""

import tkinter as tk
from tkinter import ttk

from . import codebox


class CodeEditor(codebox.BaseCodeBox):
    def __init__(
        self,
        master: tk.Misc,
        language="python",
        highlighter="mariana",
        autofocus=False,
        **kwargs,
    ):

        codebox.BaseCodeBox.__init__(
            self, master, language, highlighter, autofocus, **kwargs
        )

        self.horizontal_scroll = ttk.Scrollbar(
            self.frame, orient="horizontal", command=self.xview
        )
        self.vertical_scroll = ttk.Scrollbar(
            self.frame, orient="vertical", command=self.yview
        )
        self.configure(
            xscrollcommand=self.horizontal_scroll.set,
            yscrollcommand=self.vertical_scroll.set,
        )

        self.horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.vertical_scroll.grid(row=0, column=1, sticky="ns")

        self.ctrl_cmd_key = (
            "Command" if self.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        )

        self.bind("<KeyRelease>", self.highlight_line, add=True)
        self.bind("<<Paste>>", self.paste, add=True)
        self.bind(f"<{self.ctrl_cmd_key}-a>", self.select_all)
        try:
            self.bind("<Insert>", self.change_cursor_mode, add=True)
            self.bind("<KP_Insert>", self.change_cursor_mode, add=True)
        except tk.TclError:
            pass

    def paste(self, *_):
        """Handles text pasting"""
        if self.tag_ranges("sel"):
            sel_start = self.index("sel.first")
            self.delete(sel_start, self.index("sel.last"))
            self.mark_set("insert", sel_start)

        self.insert(self.current_pos, self.clipboard_get())

        self.event_generate("<<TextPasted>>")
        return "break"

    def select_all(self, *_):
        """Selects everything"""
        self.mark_set("insert", "end")
        self.tag_add("sel", "1.0", "end")
        self.see("insert")

        self.event_generate("<<AllSelected>>")
        return "break"

    def change_cursor_mode(self, *_):
        """
        Toggles between thin line and block cursor.
        Can be a little bit confusing, that some program,
        like Vim uses the insert key to switch between the insert
        and owerwrite mode, and others, like Sublime,
        Gedit, KWrite or even Gtk widgets uses it to change the cursor appearance
        """
        self.configure(
            blockcursor=not self["blockcursor"],
            insertwidth=1 if self["blockcursor"] else 0,
        )
        self.event_generate("<<CursorModeChanged>>")
        return "break"

    @property
    def current_line(self) -> int:
        return int(self.index("insert").split(".")[0])

    @current_line.setter
    def current_line(self, line_number: int):
        self.mark_set("insert", f"{line_number}.0")
        self.see(f"{line_number}.0")

    @property
    def current_column(self) -> int:
        return int(self.index("insert").split(".")[1])

    @current_column.setter
    def current_column(self, col_number: int):
        self.mark_set("insert", f"{self.current_line}.{col_number}")
        self.see(f"{self.current_line}.{col_number}")

    @property
    def current_pos(self) -> str:
        return str(self.index("insert"))

    @current_pos.setter
    def current_pos(self, position: str) -> None:
        self.mark_set("insert", position)
        self.see(position)

    @property
    def current_linestart(self) -> str:
        return str(self.index("insert linestart"))

    @property
    def current_lineend(self) -> str:
        return str(self.index("insert lineend"))
