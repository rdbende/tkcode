import tkinter as tk
from tkinter import ttk
from tkcode import CodeEditor

root = tk.Tk()
root.title("CodeEditor example")
root.option_add("*tearOff", 0)

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save as")
file_menu.add_separator()
file_menu.add_command(label="Exit")

help_menu = tk.Menu(menubar)
help_menu.add_command(label="Help")
help_menu.add_command(label="About")

menubar.add_cascade(menu=file_menu, label="File")
menubar.add_cascade(menu=help_menu, label="Help")

root.config(menu=menubar)

notebook = ttk.Notebook(root)
tab_1 = ttk.Frame(notebook)
notebook.add(tab_1, text="hello.cpp")
notebook.pack(fill="both", expand=True)

code_editor = CodeEditor(tab_1, width=40, height=10, language="c++",
                         autofocus=True, blockcursor=True, insertofftime=0)

code_editor.pack(fill="both", expand=True)

code_editor.content = """#include <iostream>
using namespace std;

int main() {
\tcout << "Hello World!" << endl;
\treturn 0;
}"""

root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.mainloop()

