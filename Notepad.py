import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))

def clear_text():
    text_area.delete(1.0, tk.END)

def word_count():
    content = text_area.get(1.0, tk.END)
    words = content.split()
    num_words = len(words)
    messagebox.showinfo("Word Count", f"Total words: {num_words}")

def make_bold():
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")
        text_area.tag_configure("bold", font=("TkDefaultFont", text_size.get(), "bold"))

def make_italic():
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")
        text_area.tag_configure("italic", font=("TkDefaultFont", text_size.get(), "italic"))

def make_underline():
    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")
        text_area.tag_configure("underline", underline=True)

def change_text_color():
    color = colorchooser.askcolor(title="Choose Text Color")
    if color[1]:
        text_area.tag_add("color", "sel.first", "sel.last")
        text_area.tag_configure("color", foreground=color[1])

def change_highlight_color():
    color = colorchooser.askcolor(title="Choose Highlight Color")
    if color[1]:
        text_area.tag_add("highlight", "sel.first", "sel.last")
        text_area.tag_configure("highlight", background=color[1])

root = tk.Tk()
root.title("Simple Text Editor")

text_area = tk.Text(root)
text_area.pack(fill=tk.BOTH, expand=True)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Clear", command=clear_text)
edit_menu.add_command(label="Word Count", command=word_count)
edit_menu.add_separator()
edit_menu.add_command(label="Bold", command=make_bold)
edit_menu.add_command(label="Italic", command=make_italic)
edit_menu.add_command(label="Underline", command=make_underline)
edit_menu.add_separator()
edit_menu.add_command(label="Change Text Color", command=change_text_color)
edit_menu.add_command(label="Change Highlight Color", command=change_highlight_color)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

text_size = tk.IntVar()
text_size.set(12)  # Default font size
size_menu = tk.Menu(menu_bar, tearoff=0)
size_menu.add_radiobutton(label="10", variable=text_size, value=10, command=make_bold)
size_menu.add_radiobutton(label="12", variable=text_size, value=12, command=make_bold)
size_menu.add_radiobutton(label="14", variable=text_size, value=14, command=make_bold)
size_menu.add_radiobutton(label="16", variable=text_size, value=16, command=make_bold)
size_menu.add_radiobutton(label="18", variable=text_size, value=18, command=make_bold)
menu_bar.add_cascade(label="Text Size", menu=size_menu)

root.config(menu=menu_bar)

root.mainloop()
