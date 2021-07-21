"""
Author: rdbende
License: GNU GPLv3
Copyright: 2021 rdbende
"""

import json
import os
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Union

import pygments
from pygments.lexers import *


class BaseCodeBox(tk.Text):
    languages = (
        "Ada",
        "Bash",
        "Batch",
        "Brainfuck",
        "C",
        "CMake",
        "CoffeeScript",
        "CSS",
        "C#",
        "C++",
        "Dart",
        "Delphi",
        "Dockerfile",
        "Fortran",
        "Go",
        "Groovy",
        "Haskell",
        "HTML",
        "Java",
        "JavaScript",
        "JSON",
        "Kotlin",
        "Lisp",
        "Lua",
        "Matlab",
        "Makefile",
        "Nasm",  # probably the most common
        "Objective-C",
        "Perl",
        "PHP",
        "PowerShell",
        "Python",
        "R",
        "Ruby",
        "Swift",
        "SQL",
        "Tcl",
        "TypeScript",
        "Vim",
        "YAML",
    )

    def __init__(
        self,
        master: tk.Misc,
        language: str,
        highlighter: str,
        autofocus: bool,
        **kwargs,
    ) -> None:
        kwargs.update({"wrap": "none"})

        tab_length = kwargs.pop("tabs", "4ch")
        if tab_length[-2:] == "ch":
            tab_length = int(tab_length[:-2])
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

        if command in {"insert", "replace", "delete"}:
            self.event_generate("<<ContentChanged>>")

        return result  # Returns what it would actually return

    def insert(self, index: str, content: str):
        # FIXME: imo this method is super hacky, there should be a better solution
        line_no = int(
            self.index(index).split(".")[
                0
            ]  # Important! We don't want a text index "end.end"
        )

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

    def highlight_all(self, *_) -> None:
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
        # FIXME: if index is `end` than both the code_editor
        # and the code_block's last line gets highlighted, but if it's 1.0,
        # than just the code_block, and code_editor's last line stays white
        self.insert("end", new_content)

    @property
    def language(self) -> Union[str, None]:
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
        return self.get("1.0", "end") == "\n"

    def _generate_font_list(self, input_dict: dict) -> list:
        font_dict = {"-family": self.font_family, "-size": self.font_size}

        for style_key, style_value in input_dict.items():
            if style_key == "family":
                font_dict["-family"] = style_value
            elif style_key == "size":
                font_dict["-size"] = style_value
            elif style_key == "bold":
                font_dict["-weight"] = "bold" if style_value else "normal"
            elif style_key == "italic":
                font_dict["-slant"] = "italic" if style_value else "roman"
            elif style_key == "underline":
                font_dict["-underline"] = style_value
            elif style_key == "strikethrough":
                font_dict["-overstrike"] = style_value

        font_list = []
        for x, y in zip(font_dict.keys(), font_dict.values()):
            font_list.extend([x, y])

        return font_list

    def update_highlighter(self, highlighter: str) -> None:
        """Sets or changes the highlighter configuration"""
        highlight_file = highlighter
        package_path = os.path.dirname(os.path.realpath(__file__))

        if highlighter in [
            x.split(".")[0] for x in os.listdir(os.path.join(package_path, "schemes"))
        ]:
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
            if isinstance(value, str):
                self.tag_configure(key, foreground=value)
            else:
                if "font" in value:
                    value["font"] = self._generate_font_list(value["font"])
                self.tag_configure(key, **value)

        if self._highlighter:  # Don't generate event on init
            self.event_generate("<<HighlighterChanged>>")

        self._highlighter = highlighter
        self.highlight_all()

    def update_lexer(self, language: Union[str, None] = None) -> None:
        """Sets or changes the Pygments lexer"""
        if not language:
            return

        self._set_lexer(language.lower())

        if self._language:  # Don't generate event on init
            self.event_generate("<<LanguageChanged>>")

        self._language = language
        self.highlight_all()

    def _set_lexer(self, lang):
        if lang == "ada":
            self._lexer = AdaLexer
        elif lang == "bash":
            self._lexer = BashLexer
        elif lang == "batch":
            self._lexer = BatchLexer
        elif lang in ["brainfuck", "bf"]:
            self._lexer = BrainfuckLexer
        elif lang == "c":
            self._lexer = CLexer
        elif lang == "cmake":
            self._lexer = CMakeLexer
        elif lang in ["coffeescript", "coffee"]:
            self._lexer = CoffeeScriptLexer
        elif lang == "css":
            self._lexer = CssLexer
        elif lang in ["c sharp", "cs", "c#"]:
            self._lexer = CSharpLexer
        elif lang in ["c plus plus", "cpp", "c++"]:
            self._lexer = CppLexer
        elif lang == "dart":
            self._lexer = DartLexer
        elif lang == "delphi":
            self._lexer = DelphiLexer
        elif lang in ["dockerfile", "docker"]:
            self._lexer = DockerLexer
        elif lang == "fortran":
            self._lexer = FortranLexer
        elif lang in ["go", "golang"]:
            self._lexer = GoLexer
        elif lang == "groovy":
            self._lexer = GroovyLexer
        elif lang == "haskell":
            self._lexer = HaskellLexer
        elif lang == "html":
            self._lexer = HtmlLexer
        elif lang == "java":
            self._lexer = JavaLexer
        elif lang in ["javascript", "js"]:
            self._lexer = JavascriptLexer
        elif lang == "json":
            self._lexer = JsonLexer
        elif lang == "kotlin":
            self._lexer = KotlinLexer
        elif lang == "lisp":
            self._lexer = CommonLispLexer
        elif lang == "lua":
            self._lexer = LuaLexer
        elif lang == "makefile":
            self._lexer = MakefileLexer
        elif lang == "matlab":
            self._lexer = MatlabLexer
        elif lang == "nasm":
            self._lexer = NasmLexer
        elif lang in ["objective-c", "objectivec"]:
            self._lexer = ObjectiveCLexer
        elif lang == "perl":
            self._lexer = PerlLexer
        elif lang == "php":
            self._lexer = PhpLexer
        elif lang == "powershell":
            self._lexer = PowerShellLexer
        elif lang in ["python", "py"]:
            self._lexer = PythonLexer
        elif lang in ["r", "erlang"]:
            self._lexer = ErlangLexer
        elif lang == "ruby":
            self._lexer = RubyLexer
        elif lang == "swift":
            self._lexer = SwiftLexer
        elif lang == "sql":
            self._lexer = SqlLexer
        elif lang == "tcl":
            self._lexer = TclLexer
        elif lang in ["typescript", "ts"]:
            self._lexer = TypeScriptLexer
        elif lang == "vim":
            self._lexer = VimLexer
        elif lang == "yaml":
            self._lexer = YamlLexer

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, key: str):
        return self.cget(key)

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        result = f"{type(self).__module__}.{type(self).__name__} widget"

        if not self.winfo_exists():
            return f"<destroyed {result}>"

        return f"<{result}, color scheme: {self._highlighter!r}, lexer: {self._lexer.__name__}>"

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

    def configure(self, **kwargs) -> None:
        lang = kwargs.pop("language", None)
        highlighter = kwargs.pop("highlighter", None)
        if lang:
            self.update_lexer(lang)
        if highlighter:
            self.update_highlighter(highlighter)
        tk.Text.configure(self, **kwargs)

    config = configure

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

    def destroy(self):
        """Destroys this widget"""
        # Explicit tcl calls are needed to avoid recursion error
        for i in self.frame.children.values():
            self.tk.call("destroy", i._w)
        self.tk.call("destroy", self.frame._w)
