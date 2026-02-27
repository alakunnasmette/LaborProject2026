# --- Helper to show incomplete warning ---
def show_incomplete_warning(missing_count, item_name="vragen"):
    from tkinter import messagebox
    messagebox.showwarning(
        "Onvolledige vragenlijst",
        f"Er zijn nog {missing_count} {item_name} niet ingevuld."
    )
# --- Helper to add navigation buttons (back/submit) ---
def add_nav_buttons(parent, submit_command, skip_command=None, skip_text="Overslaan", submit_text="Opslaan en verder", skip_side="left", submit_side="right", padx=30):
    """
    Adds navigation buttons (back/skip and submit) to the given parent frame.
    Only adds skip button if skip_command is provided.
    """
    if skip_command:
        btn_skip = create_back_button(parent, text=skip_text, command=skip_command)
        btn_skip.pack(side=skip_side, padx=padx)
    btn_submit = create_submit_button(parent, text=submit_text, command=submit_command)
    btn_submit.pack(side=submit_side, padx=padx)
"""
Reusable Tkinter UI components for constructing pages, tables, and form elements.
"""

import tkinter as tk
from tkinter import ttk
from . import ui_styles as stylesheet # stylesheet

# --- Clear frame ---
def clear_frame(frame: tk.Widget) -> None:
    for w in frame.winfo_children():
        w.destroy()

# --- Reusable Back Button ---
def create_back_button(parent, text, command=None):
    btn = tk.Button(
        parent,
        text=text,
        bg=stylesheet.SECONDARY_BG if hasattr(stylesheet, 'SECONDARY_BG') else stylesheet.CONTROL_PRIMARY_BACKGROUND_COLOR,
        fg="white",
        font=getattr(stylesheet, 'BUTTON_FONT', ("Segoe UI", 11, "bold")),
        padx=getattr(stylesheet, 'BUTTON_PADX', 20),
        pady=getattr(stylesheet, 'BUTTON_PADY', 6),
        command=command
    )
    return btn

# --- Reusable Submit Button ---
def create_submit_button(parent, text, command=None):
    btn = tk.Button(
        parent,
        text=text,
        bg=stylesheet.PRIMARY_BG if hasattr(stylesheet, 'PRIMARY_BG') else stylesheet.CONTROL_PRIMARY_BACKGROUND_COLOR,
        fg="white",
        font=getattr(stylesheet, 'BUTTON_FONT', ("Segoe UI", 11, "bold")),
        padx=getattr(stylesheet, 'BUTTON_PADX', 20),
        pady=getattr(stylesheet, 'BUTTON_PADY', 8),
        command=command
    )
    return btn

# --- Reusable Warning Label ---
def create_warning_label(parent, text):
    label = tk.Label(
        parent,
        text=text,
        fg="#b22222",  # firebrick red
        bg=stylesheet.PAGE_BACKGROUND_COLOR if hasattr(stylesheet, 'PAGE_BACKGROUND_COLOR') else "#fff8e1",
        font=getattr(stylesheet, 'SUBTITLE_FONT', ("Segoe UI", 10, "bold")),
        wraplength=500,
        justify="left"
    )
    return label

# --- Reusable Sidebar ---
def create_sidebar(root, bg=None, width=200):
    bg = bg or getattr(stylesheet, 'COLOR_PRIMARY', stylesheet.SIDEBAR_BACKGROUND_COLOR)
    sidebar = tk.Frame(root, bg=bg, width=width)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    return sidebar

# --- Reusable Logo ---
def add_logo_to_sidebar(sidebar, logo_path="images/labor-logo.png", use_pillow=True, bg=None):
    import os
    try:
        from PIL import Image, ImageTk
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((140, 140), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_img)
    except Exception:
        try:
            logo = tk.PhotoImage(file=logo_path)
            w = logo.width()
            h = logo.height()
            if w > 140 or h > 140:
                sx = max(1, int(round(w / 140)))
                sy = max(1, int(round(h / 140)))
                logo = logo.subsample(sx, sy)
        except Exception:
            logo = None
    if logo:
        logo_label = tk.Label(sidebar, image=logo, bg=bg or getattr(stylesheet, 'COLOR_PRIMARY', stylesheet.SIDEBAR_BACKGROUND_COLOR))
        logo_label.image = logo
        logo_label.pack(side="bottom", pady=20)
    else:
        logo_label = tk.Label(sidebar, text="LABOR", fg="white", bg=bg or getattr(stylesheet, 'COLOR_PRIMARY', stylesheet.SIDEBAR_BACKGROUND_COLOR), font=("Arial", 16, "bold"))
        logo_label.pack(side="bottom", pady=20)
    return logo_label


