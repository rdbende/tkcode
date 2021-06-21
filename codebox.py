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

class CodeBox(tk.Text):
    languages = {"Ada",
                 "C",
                 "CSS",
                 "C#",
                 "C++",
                 "Dart",
                 "Delphi",
                 "Go",
                 "Haskell",
                 "HTML",
                 "Java",
                 "JavaScript",
                 "Kotlin",
                 "Lisp",
                 "Lua",
                 "Matlab",
                 "Objective-C",
                 "Perl",
                 "PHP",
                 "Python",
                 "R",
                 "Ruby",
                 "Swift",
                 "Tcl",
                 "TypeScript"
                 }
    
    def __init__(self, master=None, language="python", highlighter="mariana", **kwargs):
        kwargs.update({"highlightthickness": 0})
        kwargs.update({"wrap": "none"})
        tab_length = kwargs.pop("tabs", "    ")
        
        self.frame = ttk.Frame(master)
        tk.Text.__init__(self, self.frame, **kwargs)
        self.horizontal_scroll = ttk.Scrollbar(self.frame, orient="horizontal", command=self.xview)
        self.vertical_scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.yview)
        self.configure(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set)
        
        tk.Text.grid(self, row=0, column=0, sticky="nsew")
        self.horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.vertical_scroll.grid(row=0, column=1, sticky="ns")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.font = tkfont.Font(family="monospace", size=10)
        tab = self.font.measure(tab_length)
        
        self.config(font=self.font, tabs=tab, spacing1=0, spacing2=0, spacing3=0)
        
        package_path = os.path.dirname(os.path.realpath(__file__))
        
        if highlighter in {"mariana"}: # There will be more
            highlighter = os.path.join(package_path, "schemes", highlighter + ".json")
            
        with open(highlighter) as file:
            self.configuration = json.load(file)
        
        general_props = self.configuration.pop("general")
        selection_props = self.configuration.pop("selection")
        
        self.config(**general_props)
        self.tag_configure("sel", **selection_props)
        
        for key, value in self.configuration.items():
            self.tag_configure(key, foreground=value)
        
        self.ctrl_cmd_key = "Command" if self.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        self.bind("<KeyRelease>", self.highlight_line)
        self.bind("<<Paste>>", self.paste)
        self.bind(f"<{self.ctrl_cmd_key}-a>", self.select_all)
        self.bind("<Insert>", self.change_cursor_mode)
        self.bind("<KP_Insert>", self.change_cursor_mode)
        
        self.update_lexer(language)

    def highlight_line(self, event=None, line=None):
        """Highlights the specified or the current row"""
        if line is None:
            line = int(self.current_line)
        
        for tag in self.tag_names(index=None):
            self.tag_remove(tag, f"{line}.0", f"{line}.end")
        
        line_text = self.get(f"{line}.0", f"{line}.end")
        start = f"{line}.0"

        for token, content in lex(line_text, self.lexer()):
            end = f"{start.split('.')[0]}.{int(start.split('.')[1]) + len(content)}"
            self.tag_add(str(token), start, end)
            start = end

    def highlight_all(self, event=None):
        """Loops through the entire content and highlights it"""
        for tag in self.tag_names(index=None):
            self.tag_remove(tag, "1.0", "end")
        
        for i in range(len(self.get("1.0", "end-1c").splitlines())):
            self.highlight_line(line=i)
            self.update()
            i += 1
            
    def paste(self, event=None):
        """Handles text pasting"""
        if len(self.tag_ranges("sel")) >= 1:
            self.delete(*self.tag_ranges("sel"))
            
        code = self.clipboard_get()
        
        if len(code.splitlines()) > 1:
            for line in code.splitlines():
                self.insert("insert", line + "\n")
                self.highlight_line(line=self.current_line - 1)
        else:
            self.insert("insert", code)
            self.highlight_line(line=self.current_line)
            
        return "break"        
    
    def select_all(self, event=None):
        """Selects everything"""
        self.tag_add("sel", "1.0", tk.END)
        self.mark_set("insert", "end")
        self.see("insert")
        return "break"
    
    def change_cursor_mode(self, event=None):
        """Toggles between | and block cursor"""
        if self.cget("blockcursor"):
            self.config(blockcursor=False)
        else:
            self.config(blockcursor=True)
            
    def update_lexer(self, language=None):
        """Sets or changes the Pygments lexer"""
        if language:
            self._language = language.lower()
            lang = self._language
        
        if lang == "ada":
            self.lexer = AdaLexer
        elif lang == "c":
            self.lexer = CLexer
        elif lang == "css":
            self.lexer = CssLexer
        elif lang == "c sharp" or lang == "cs" or lang == "c#":
            self.lexer = CSharpLexer
        elif lang == "c plus plus" or lang == "cpp" or lang == "c++":
            self.lexer = CppLexer
        elif lang == "dart":
            self.lexer = DartLexer
        elif lang == "delphi":
            self.lexer = DelphiLexer
        elif lang == "haskell":
            self.lexer = HaskellLexer
        elif lang == "html":
            self.lexer = HtmlLexer
        elif lang == "go" or lang == "golang":
            self.lexer = GoLexer
        elif lang == "java":
            self.lexer = JavaLexer
        elif lang == "javascript" or lang == "js" :
            self.lexer = JavascriptLexer
        elif lang == "kotlin":
            self.lexer = KotlinLexer
        elif lang == "lisp":
            self.lexer = CommonLispLexer
        elif lang == "lua":
            self.lexer = LuaLexer
        elif lang == "matlab":
            self.lexer = MatlabLexer
        elif lang == "objective-c" or lang == "objectivec":
            self.lexer = ObjectiveCLexer
        elif lang == "perl":
            self.lexer = PerlLexer
        elif lang == "php":
            self.lexer = PhpLexer
        elif lang == "r" or lang == "erlang":
            self.lexer = ErlangLexer
        elif lang == "python":
            self.lexer = PythonLexer
        elif lang == "ruby":
            self.lexer = RubyLexer
        elif lang == "swift":
            self.lexer = SwiftLexer
        elif lang == "tcl":
            self.lexer = TclLexer
        elif lang == "typescript" or lang == "ts" :
            self.lexer = TypeScriptLexer
        else:
            self.lexer = PythonLexer # Fallback to Python
            warnings.warn(f"Bad language specifier: '{lang}', falling back to Python. See 'CodeBox.languages' for a list of supported languages.")
        
        self.event_generate("<<CodeBoxLanguageChanged>>")

    @property
    def content(self):
        return self.get("1.0", "end")
    
    @content.setter
    def content(self, new_content):
        self.delete("1.0", "end")
        self.insert("1.0", new_content)
    
    @property
    def current_line(self) -> int:
        return int(self.index("insert").split(".")[0])
    
    @current_line.setter
    def current_line(self, line_number):
        self.mark_set("insert", f"{line_number}.0")
        self.see(f"{line_number}.0")
        
    @property
    def current_column(self) -> int:
        return int(self.index("insert").split(".")[0])
    
    @current_line.setter
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
    
    @property
    def number_of_lines(self) -> str:
        return str(self.index("end-1c").split(".")[0])
    
    @property
    def language(self):
        return self._language
    
    @language.setter
    def language(self, language):
        self.update_lexer(language)

    @property
    def font_family(self):
        return self.font.actual("family")
    
    @font_family.setter
    def font_family(self, family):
        self.font.config(family=family)
        
    @property
    def font_size(self):
        return self.font.actual("size")
    
    @font_size.setter
    def font_size(self, size):
        self.font.config(size=size)
        
    def load_from_file(self, file_name):
        with open(file_name, "r") as file:
            self.delete("1.0", "end")
            self.insert("1.0", file.read())
        
    def insert_from_file(self, file_name, index=None):
        if index is None:
            index = self.current_pos
            
        with open(file_name, "r") as file:
            self.insert(index, file.read())
        
    def save_to_file(self, file_name, start="1.0", end="end-1c"):
        with open(file_name, "w") as file:
            file.write(self.get(start, end))
            
    def configure(self, *args, **kwargs):
        lang = kwargs.pop("language", None)
        if lang:
            self.update_lexer(lang)
            self.highlight_all()
        tk.Text.configure(self, *args, **kwargs)
            
    config = configure

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

