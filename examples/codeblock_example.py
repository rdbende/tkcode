import tkinter as tk
from tkinter import ttk
from tkcode import CodeBlock

root = tk.Tk()
root.title("CodeBlock example")
root.config(bg="#4e5a65")

style = ttk.Style()

card_im = tk.PhotoImage(file="tkcode/code_card.png")

style.layout('Card', [
    ('Card.field', {'children': [
        ('Card.padding', {'expand': 1})
        ]})
    ])

style.element_create("Card.field", "image", card_im, border=20, padding=4, sticky="nsew")

code_frame = ttk.Frame(root, padding=15, style="Card")
code_frame.pack(fill="both", expand=True, padx=20, pady=20)

code = CodeBlock(code_frame, width=35, height=9, highlighter="más")
code.pack(expand=True, fill="both")

code.content = """import tkinter as tk
from tkcode import CodeEditor

root = tk.Tk()

text = CodeEditor(root)
text.pack(expand=True, fill="both")

root.mainloop()"""

root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.mainloop()