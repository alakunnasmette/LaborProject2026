import tkinter as tk
from tkinter import ttk
import ui.ui_styles

def build_client_page(parent):
    parent.configure(bg="white")

    for w in parent.winfo_children():
        w.destroy()

    page = tk.Frame(parent, bg="white")
    page.pack(fill="both", expand=True)