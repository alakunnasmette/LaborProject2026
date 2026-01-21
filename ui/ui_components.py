# ui_components.py
import tkinter as tk
from tkinter import ttk

import ui_styles as ui_styles

# --- Scrollable container ---
def create_scrollable_container(parent, bg=None):
    container = tk.Frame(parent, bg=bg)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    content = tk.Frame(canvas, bg=bg)
    window_id = canvas.create_window((0, 0), window=content, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_resize(event):
        canvas.itemconfig(window_id, width=event.width)

    content.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_mousewheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    return container, canvas, content

# --- Title and subtitle ---
def create_page_title(parent, title_text, subtitle_text):
    # -- Title label --
    title = tk.Label(
        parent,
        text=title_text,
        bg=ui_styles.PAGE_BACKGROUND_COLOR,
        fg=ui_styles.TEXT_PRIMARY_COLOR,
        font=ui_styles.TITLE_FONT,
        anchor="w"
    )
    title.pack(fill="x", padx=ui_styles.TITLE_PADX, pady=(ui_styles.TITLE_PADY_TOP, ui_styles.TITLE_PADY_BOTTOM))

    # -- Subtitle label --
    subtitle = tk.Label(
        parent,
        text=subtitle_text,
        bg=ui_styles.PAGE_BACKGROUND_COLOR,
        fg=ui_styles.TEXT_PRIMARY_COLOR,
        font=ui_styles.SUBTITLE_FONT,
        anchor="w",
        justify="left"
    )
    subtitle.pack(fill="x", padx=ui_styles.SUBTITLE_PADX, pady=(ui_styles.SUBTITLE_PADY_TOP, ui_styles.SUBTITLE_PADY_BOTTOM))

    return title, subtitle

# --- Column headers ---
def create_column_headers(parent, labels):
    header = tk.Frame(parent)
    header.pack(fill="x")
    for col, text in enumerate(labels):
        tk.Label(
            header,
            text=text,
            bg=ui_styles.TABLE_HEADER_BACKGROUND_COLOR,
            fg=ui_styles.TEXT_SECONDARY_COLOR,
            font=ui_styles.TABLE_HEADER_FONT,
            anchor="w" if col < 2 else "e",
            padx=ui_styles.TABLE_HEADER_PADX if col < 2 else 40,
            width=8 if col == 0 else None
        ).grid(row=0, column=col, sticky="w" if col < 2 else "e")
    
    return header

# --- Column row ---
def create_likert_row(parent, row_index, number, statement, var, options):
    if row_index % 2 == 0:
        row_bg = ui_styles.TABLE_ROW_PRIMARY_BACKGROUND_COLOR
    else:
        row_bg = ui_styles.TABLE_ROW_SECONDARY_BACKGROUND_COLOR

    row = tk.Frame(parent, bg=row_bg)
    row.pack(fill="x", pady=ui_styles.ROW_PADY)
    row.grid_columnconfigure(1, weight=1)

    # -- Number label --
    num_label = tk.Label(
        row,
        text=str(number),
        width=ui_styles.NUMBER_WIDTH,
        bg=ui_styles.ACCENT_PRIMARY_COLOR,
        fg=ui_styles.TEXT_PRIMARY_COLOR,
        font=ui_styles.NUMBER_FONT,
        anchor="c"
    )
    num_label.grid(
        row=0, column=0, 
        padx=(
            ui_styles.ROW_INNER_PADX, 
            ui_styles.ROW_INNER_PADX), 
            sticky="w"
        )

    # -- Statement label --
    stmt_label = tk.Label(
        row,
        text=statement,
        bg=row_bg,
        fg=ui_styles.TEXT_PRIMARY_COLOR,
        font=ui_styles.TEXT_FONT,
        anchor="w",
        justify="left",
        wraplength=ui_styles.STATEMENT_WRAP
    )
    stmt_label.grid(
        row=0, column=1, 
        sticky="w", 
        padx=ui_styles.STATEMENT_PADX, 
        pady=ui_styles.STATEMENT_PADY
    )

    likert_frame = tk.Frame(row, bg=row_bg)
    likert_frame.grid(
        row=0, 
        column=2, 
        padx=20, 
        pady=8, 
        sticky="e"
    )

    buttons = []

    def update_buttons():
        current = var.get()
        for value, widget in buttons:
            if current == value:
                widget.config(relief="sunken", bg=ui_styles.CONTROL_SECONDARY_BACKGROUND_ACTIVE_COLOR, fg=ui_styles.TEXT_SECONDARY_COLOR)
            else:
                widget.config(relief="raised", bg=ui_styles.CONTROL_PRIMARY_BACKGROUND_COLOR, fg=ui_styles.TEXT_PRIMARY_COLOR)
    
    for col, value in enumerate(options):
        btn = tk.Label(
            likert_frame,
            text=value,
            width=ui_styles.LIKERT_BUTTON_WIDTH,
            bd=1,
            relief="raised",
            bg=ui_styles.CONTROL_PRIMARY_BACKGROUND_COLOR,
            fg=ui_styles.TEXT_PRIMARY_COLOR,
            font=ui_styles.BUTTON_FONT
        )
        btn.grid(row=0, column=col, padx=ui_styles.LIKERT_BUTTON_PADX)

        def on_click(event, v=value):
            var.set(v)
            update_buttons()

        btn.bind("<Button-1>", on_click)
        buttons.append((value, btn))
    
    return row
