import tkinter as tk
from tkinter import ttk
import codebox

root = tk.Tk()

text = codebox.CodeBox(root)
text.pack(fill="both", expand=True)

combo = ttk.Combobox(root, values=text.languages)
combo.pack()
combo.set("Python")

root.mainloop()
