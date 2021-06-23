"""
Author: rdbende
License: GNU GPLv3
Copyright: 2021 rdbende
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from pygments import lex
from pygments.lexers import *

import json
import os
import warnings

from . import codebox

class CodeEditor(codebox.BaseCodeBox):    
    def __init__(self, master=tk._default_root, language="python", highlighter="mariana", autofocus=False, **kwargs):
        codebox.BaseCodeBox.__init__(self, master, language, highlighter, autofocus, **kwargs)

        self.horizontal_scroll = ttk.Scrollbar(self.frame, orient="horizontal", command=self.xview)
        self.vertical_scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.yview)
        self.configure(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set)
        
        self.horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.vertical_scroll.grid(row=0, column=1, sticky="ns")
        
        self.ctrl_cmd_key = "Command" if self.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        self.bind("<KeyRelease>", self.highlight_line)
        self.bind("<<Paste>>", self.paste)
        self.bind(f"<{self.ctrl_cmd_key}-a>", self.select_all)
        self.bind("<Insert>", self.change_cursor_mode)
        self.bind("<KP_Insert>", self.change_cursor_mode)
            
    def paste(self, event=None):
        """Handles text pasting"""
        if len(self.tag_ranges("sel")) >= 1:
            self.delete(*self.tag_ranges("sel"))
            
        code = self.clipboard_get()

        self.insert("end", code)
        
        self.event_generate("<<TextPasted>>")
        
        return "break"
    
    def select_all(self, event=None):
        """Selects everything"""
        self.tag_add("sel", "1.0", tk.END)
        self.mark_set("insert", "end")
        self.see("insert")
        
        self.event_generate("<<AllSelected>>")
        
        return "break"
    
    def change_cursor_mode(self, event=None):
        """Toggles between | and block cursor"""
        if self.cget("blockcursor"):
            self.config(blockcursor=False)
        else:
            self.config(blockcursor=True)
            
        self.event_generate("<<CursorModeChanged>>")
    
    @property
    def current_line(self) -> int:
        return int(self.index("insert").split(".")[0])
    
    @current_line.setter
    def current_line(self, line_number):
        self.mark_set("insert", f"{line_number}.0")
        self.see(f"{line_number}.0")
        
    @property
    def current_column(self) -> int:
        return int(self.index("insert").split(".")[1])
    
    @current_column.setter
    def current_column(self, col_number):
        self.mark_set("insert", f"{self.current_line}.{col_number}")
        self.see(f"{self.current_line}.{col_number}")
    
    @property
    def current_pos(self) -> str:
        return str(self.index("insert"))
    
    @current_pos.setter
    def current_pos(self, position):
        self.mark_set("insert", position)
        self.see(position)
    
    @property
    def current_linestart(self) -> str:
        return str(self.index("insert linestart"))
    
    @property
    def current_lineend(self) -> str:
        return str(self.index("insert lineend"))
        
