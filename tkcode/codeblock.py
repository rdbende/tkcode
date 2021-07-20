"""
Author: rdbende
License: GNU GPLv3
Copyright: 2021 rdbende
"""

import tkinter as tk

from . import codebox


class CodeBlock(codebox.BaseCodeBox):
    def __init__(
        self,
        master: tk.Misc,
        language="python",
        highlighter="mariana",
        autofocus=False,
        **kwargs
    ):
        kwargs.update({"state": "disabled"})
        kwargs.pop("xscrollcommand", None)
        kwargs.pop("yscrollcommand", None)
        codebox.BaseCodeBox.__init__(
            self, master, language, highlighter, autofocus, **kwargs
        )

    def disabler(func):
        def wrapper(self, *args, **kwargs):
            codebox.BaseCodeBox.config(self, state="normal")
            func(self, *args, **kwargs)
            codebox.BaseCodeBox.config(self, state="disabled")

        return wrapper

    @disabler
    def insert(self, *args, **kwargs):
        codebox.BaseCodeBox.insert(self, *args, **kwargs)

    @disabler
    def delete(self, *args, **kwargs):
        codebox.BaseCodeBox.delete(self, *args, **kwargs)

    @property
    def content(self):
        return self.get("1.0", "end")

    @content.setter
    @disabler
    def content(self, new_content):
        self.delete("1.0", "end")
        self.insert("end", new_content)
