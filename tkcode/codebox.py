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

class TextLineNumbers(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.text_widget = args[0]

    def redraw(self, *args):
        self.delete("all")

        for i in range(self.text_widget.number_of_lines):
            dline = self.text_widget.dlineinfo(f"{i}.0")
            if dline is None:
                break
            y_pos = dline[1]
            self.create_text(2, y_pos, anchor="nw", text=i+1)

class BaseCodeBox(tk.Text):
    languages = ("Ada",
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
                 )
    
    def __init__(self, master, language, highlighter, autofocus, **kwargs):
        kwargs.update({"wrap": "none"})
        
        tab_length = kwargs.pop("tabs", "4ch")
        if tab_length[len(tab_length)-2:] == "ch":
            tab_length = int(tab_length[:len(tab_length)-2])
        else:
            raise ValueError(f"Invalid tab length '{tab_length}', please give it in characters, eg: '4ch'")
            
        self.frame = ttk.Frame(master)
        tk.Text.__init__(self, self.frame, **kwargs)
        
        tk.Text.grid(self, row=0, column=0, sticky="nsew")
        
        self.font = tkfont.Font(font=kwargs.pop("font", ("monospace", 10)))
        tab = self.font.measure(" " * tab_length)
        
        self.configure(font=self.font, tabs=tab)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self._highlighter, self._language = None, None
        
        self.update_highlighter(highlighter)
        self.update_lexer(language)
        
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        
        if autofocus:
            self.focus()

    def _proxy(self, command, *args):
        """Thanks to Bryan Oakley on StackOverflow: https://stackoverflow.com/a/40618152/"""
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        # Generate a <<TextModified>> event if the widget content was modified
        if command in ("insert", "replace", "delete"):
            self.event_generate("<<TextModified>>")

        return result # Returns what it would actually return

    def insert(self, index, content):
        if len(content.splitlines()) > 1:
            for line in content.splitlines():
                tk.Text.insert(self, index, line + "\n")
                self.highlight_line(line=int(self.index("insert").split(".")[0]) - 1)
        else:
            tk.Text.insert(self, index, content)
            self.highlight_line(line=int(self.index("insert").split(".")[0]))

        return "break"

    def highlight_line(self, event=None, line=None):
        """Highlights the specified or the current row"""
        if line is None:
            line = int(self.index("insert").split(".")[0])
        
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
            
        self.event_generate("<<AllHighlighted>>")

    def load_from_file(self, file_name):
        with open(file_name, "r") as file:
            self.delete("1.0", "end")
            self.insert("end", file.read())
        self.event_generate("<<TextLoadedFromFile>>")
        
    def save_to_file(self, file_name, start="1.0", end="end-1c"):
        with open(file_name, "w") as file:
            file.write(self.get(start, end))
        self.event_generate("<<TextSavedToFile>>")

    @property
    def content(self):
        return self.get("1.0", "end")
    
    @content.setter
    def content(self, new_content):
        self.delete("1.0", "end")
        self.insert("end", new_content)

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

    @property
    def number_of_lines(self) -> int:
        return int(self.index("end-1c").split(".")[0])

    @property
    def is_empty(self) -> bool:
        return True if self.get("1.0", "end") == "\n" else False

    def update_highlighter(self, highlighter):
        """Sets or changes the highlighter configuration"""
        highlight_file = highlighter

        package_path = os.path.dirname(os.path.realpath(__file__))
        
        if highlighter in {"azure", "mariana", "monokai"}: # There will be more
            highlight_file = os.path.join(package_path, "schemes", highlighter + ".json")
            
        try:
            with open(highlight_file) as file:
                self.configuration = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Highlighter configuration file not found: '{highlight_file}'")
        
        general_props = self.configuration.pop("general")
        selection_props = self.configuration.pop("selection")
        syntax_props = self.configuration.pop("syntax")
        
        self.config(**general_props)
        self.tag_configure("sel", **selection_props)
        
        for key, value in syntax_props.items():
            if type(value) == str:
                self.tag_configure(key, foreground=value)
            else:
                self.tag_configure(key, **value)

        if self._highlighter:
            self.event_generate("<<HighlighterChanged>>")
            
        self._highlighter = highlighter
        self.highlight_all()
            
    def update_lexer(self, language=None):
        """Sets or changes the Pygments lexer"""
        if language:
            lang = language.lower()
        
        # I'll love the match-case statement XD
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
        elif lang == "python" or lang == "py":
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
            self.lexer = PythonLexer # Fall back to Python
            warnings.warn(f"Bad language specifier: '{lang}', falling back to Python. See 'CodeBox.languages' for a list of supported languages.")
        
        if self._language:
            self.event_generate("<<LanguageChanged>>")
        
        self._language = lang
        self.highlight_all()
    
    def __setitem__(self, key, value):
        self.configure(key=value)

    def __getitem__(self, key):
        return self.cget(key)
    
    def __str__(self):
        return self.content

    def keys(self):
        keys = tk.Text.keys(self)
        keys.extend(["highlighter", "language"])
        return sorted(keys)

    def cget(self, key):
        if key == "highlighter":
            return self._highlighter
        elif key == "language":
            return self._language
        else:
            return tk.Text.cget(self, key)

    def configure(self, *args, **kwargs):
        lang = kwargs.pop("language", None)
        highlighter = kwargs.pop("highlighter", None)
        if lang:
            self.update_lexer(lang)
        if highlighter:
            self.update_highlighter(highlighter)
        tk.Text.configure(self, *args, **kwargs)
            
    config = configure

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

