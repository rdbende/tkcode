"""
Author: rdbende
License: GNU GPLv3
Copyright: 2021 rdbende
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

import pygments
from pygments.lexers import *

import json
import os
import warnings


class BaseCodeBox(tk.Text):
    languages = (
        "Ada",
        "Brainfuck",
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
        "SQL",
        "Tcl",
        "TypeScript",
    )

    def __init__(self, master, language, highlighter, autofocus, **kwargs):
        kwargs.update({"wrap": "none"})

        tab_length = kwargs.pop("tabs", "4ch")
        if tab_length[-2:] == "ch":
            tab_length = int(tab_length[: len(tab_length) - 2])
        else:
            raise ValueError(
                f"Invalid tab length '{tab_length}', please give it in characters, eg: '4ch'"
            )

        self.frame = ttk.Frame(master)
        tk.Text.__init__(self, self.frame, **kwargs)

        tk.Text.grid(self, row=0, column=0, sticky="nsew")

        self._font = tkfont.Font(font=kwargs.pop("font", ("monospace", 10)))
        tab = self._font.measure(" " * tab_length)

        self.configure(font=self._font, tabs=tab)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self._highlighter, self._language = None, None

        self.update_lexer(language)  # Order is important!
        self.update_highlighter(highlighter)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

        if autofocus:
            self.focus()

    def _proxy(self, command, *args):
        """Thanks to Bryan Oakley on StackOverflow: https://stackoverflow.com/a/40618152/"""
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        # Generate a <<ContentChanged>> event if the widget content was modified
        if command in ("insert", "replace", "delete"):
            self.event_generate("<<ContentChanged>>")

        return result  # Returns what it would actually return

    def insert(self, index, content):
        # TODO: imo this method is super hacky, there should be a better solution
        line_no = int(
            self.index(index).split(".")[0]
        )  # Important! We don't want a text index "end.end"

        if len(content.splitlines()) > 1:
            for line in content.splitlines():
                tk.Text.insert(self, f"{line_no}.end", line + "\n")
                self.mark_set("insert", f"{line_no}.end")
                self.highlight_line(line=line_no - 1)
                line_no += 1
        else:
            tk.Text.insert(self, index, content)
            self.highlight_line(line=line_no)
        self.see(f"{line_no}.0")
        return "break"

    def highlight_line(self, event: tk.Event = None, line: int = None) -> None:
        """Highlights the specified or the current line"""
        if line is None:
            line = int(self.index("insert").split(".")[0])
        line_text = self.get(f"{line}.0", f"{line}.end")
        start = f"{line}.0"

        for tag in self.tag_names(index=None):
            if tag != "sel":
                # Don't clear selection when pressing Ctrl + a
                # because this method runs on every keypress
                self.tag_remove(tag, f"{line}.0", f"{line}.end")

        for token, content in pygments.lex(line_text, self._lexer()):
            end = f"{start.split('.')[0]}.{int(start.split('.')[1]) + len(content)}"
            self.tag_add(str(token), start, end)
            start = end

    def highlight_all(self, event: tk.Event = None) -> None:
        """Loops through the entire content and highlights it"""
        for tag in self.tag_names(index=None):
            if tag != "sel":
                self.tag_remove(tag, "1.0", "end")

        for line in range(self.number_of_lines):
            self.highlight_line(line=line)

        self.event_generate("<<AllHighlighted>>")

    def load_from_file(self, file_name: str):
        with open(file_name, "r") as file:
            self.delete("1.0", "end")
            self.insert("end", file.read())
        self.event_generate("<<TextLoadedFromFile>>")

    def save_to_file(
        self, file_name: str, start: str = "1.0", end: str = "end - 1 char"
    ):
        with open(file_name, "w") as file:
            file.write(self.get(start, end))
        self.event_generate("<<TextSavedToFile>>")

    @property
    def content(self) -> str:
        return self.get("1.0", "end")

    @content.setter
    def content(self, new_content: str) -> None:
        self.delete("1.0", "end")
        self.insert(self.index("insert"), new_content)

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language) -> None:
        self.update_lexer(language)

    @property
    def lexer(self) -> pygments.lexer.Lexer:
        return self._lexer

    @lexer.setter
    def lexer(self, lexer: str) -> None:
        self._lexer = lexer
        self.update_lexer("unknown")

    @property
    def font_family(self) -> str:
        return self._font.actual("family")

    @font_family.setter
    def font_family(self, family: str) -> None:
        self._font.config(family=family)

    @property
    def font_size(self) -> int:
        return self._font.actual("size")

    @font_size.setter
    def font_size(self, size: int) -> None:
        self._font.config(size=size)

    @property
    def font(self) -> tuple:
        return self._font.actual()

    @property
    def number_of_lines(self) -> int:
        return int(self.index("end - 1 char").split(".")[0])

    @property
    def is_empty(self) -> bool:
        return True if self.get("1.0", "end") == "\n" else False

    def update_highlighter(self, highlighter: str) -> None:
        """Sets or changes the highlighter configuration"""
        highlight_file = highlighter
        package_path = os.path.dirname(os.path.realpath(__file__))

        if highlighter in {"azure", "mariana", "monokai"}:  # There will be more
            highlight_file = os.path.join(
                package_path, "schemes", highlighter + ".json"
            )
        try:
            with open(highlight_file) as file:
                self.configuration = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Style configuration file not found: '{highlight_file}'"
            )

        general_props = self.configuration.pop("general")
        selection_props = self.configuration.pop("selection")
        syntax_props = self.configuration.pop("syntax")

        self.config(**general_props)
        self.tag_configure("sel", **selection_props)

        for key, value in syntax_props.items():
            if type(value) == str:
                self.tag_configure(key, foreground=value)
            else:  # TODO: Implement font properties
                self.tag_configure(key, **value)

        if self._highlighter:  # Don't generate event on init
            self.event_generate("<<HighlighterChanged>>")

        self._highlighter = highlighter
        self.highlight_all()

    def update_lexer(self, language: str = None) -> None:
        """Sets or changes the Pygments lexer"""
        if language:
            lang = language.lower()

        # I'll love the match-case statement XD
        if lang == "ada":
            self._lexer = AdaLexer
        elif lang == "brainfuck" or lang == "bf":
            self._lexer = BrainfuckLexer
        elif lang == "c":
            self._lexer = CLexer
        elif lang == "css":
            self._lexer = CssLexer
        elif lang == "c sharp" or lang == "cs" or lang == "c#":
            self._lexer = CSharpLexer
        elif lang == "c plus plus" or lang == "cpp" or lang == "c++":
            self._lexer = CppLexer
        elif lang == "dart":
            self._lexer = DartLexer
        elif lang == "delphi":
            self._lexer = DelphiLexer
        elif lang == "haskell":
            self._lexer = HaskellLexer
        elif lang == "html":
            self._lexer = HtmlLexer
        elif lang == "go" or lang == "golang":
            self._lexer = GoLexer
        elif lang == "java":
            self._lexer = JavaLexer
        elif lang == "javascript" or lang == "js":
            self._lexer = JavascriptLexer
        elif lang == "kotlin":
            self._lexer = KotlinLexer
        elif lang == "lisp":
            self._lexer = CommonLispLexer
        elif lang == "lua":
            self._lexer = LuaLexer
        elif lang == "matlab":
            self._lexer = MatlabLexer
        elif lang == "objective-c" or lang == "objectivec":
            self._lexer = ObjectiveCLexer
        elif lang == "perl":
            self._lexer = PerlLexer
        elif lang == "php":
            self._lexer = PhpLexer
        elif lang == "r" or lang == "erlang":
            self._lexer = ErlangLexer
        elif lang == "python" or lang == "py":
            self._lexer = PythonLexer
        elif lang == "ruby":
            self._lexer = RubyLexer
        elif lang == "swift":
            self._lexer = SwiftLexer
        elif lang == "sql":
            self._lexer = SqlLexer
        elif lang == "tcl":
            self._lexer = TclLexer
        elif lang == "typescript" or lang == "ts":
            self._lexer = TypeScriptLexer
        else:
            warnings.warn(
                f"""The lexer '{self._lexer.__name__}', is not supported.
Although you can use it, there may be problems with syntax highlighting.
You can open an issue or PR in the original repository to implement
it: https://github.com/rdbende/tkcode""".replace(
                    "\n", " "
                ),
                stacklevel=3,
            )

        if self._language:  # Don't generate event on init
            self.event_generate("<<LanguageChanged>>")

        self._language = language
        self.highlight_all()

    def __setitem__(self, key, value):
        self.configure(key=value)

    def __getitem__(self, key: str):
        return self.cget(key)

    def __str__(self) -> str:
        return self.content

    def keys(self) -> list:
        keys = tk.Text.keys(self)
        keys.extend(["autofocus", "highlighter", "language"])
        return sorted(keys)

    def cget(self, key: str):
        if key == "highlighter":
            return self._highlighter
        elif key == "language":
            return self._language
        else:
            return tk.Text.cget(self, key)

    def configure(
        self, *args, **kwargs
    ) -> None:  # The autofocus arg doesn't makes sense here
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
