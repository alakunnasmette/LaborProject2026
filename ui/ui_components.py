"""
Reusable Tkinter UI components for constructing pages, tables, and form elements.
"""

import tkinter as tk
from tkinter import ttk
import ui_styles as stylesheet # stylesheet

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

# --- Primary action button ---
def create_start_screen_button(parent, text, command=None):
    start_screen_button = tk.Button(
        parent,
        text=text,
        font=stylesheet.BUTTON_FONT,
        bg=stylesheet.CONTROL_PRIMARY_BACKGROUND_COLOR,
        activebackground=stylesheet.CONTROL_PRIMARY_BACKGROUND_ACTIVE_COLOR,
        fg=stylesheet.TEXT_PRIMARY_COLOR,
        command=command
    )
    return start_screen_button

# --- Page title ---
def create_page_title(parent, title_text, subtitle_text):
    title = tk.Label(
        parent,
        text=title_text,
        bg=stylesheet.PAGE_BACKGROUND_COLOR,
        fg=stylesheet.TEXT_PRIMARY_COLOR,
        font=stylesheet.TITLE_FONT,
        anchor="w"
    )
    title.pack(fill="x", padx=stylesheet.TITLE_PADX, pady=(stylesheet.TITLE_PADY_TOP, stylesheet.TITLE_PADY_BOTTOM))

    subtitle = tk.Label(
        parent,
        text=subtitle_text,
        bg=stylesheet.PAGE_BACKGROUND_COLOR,
        fg=stylesheet.TEXT_PRIMARY_COLOR,
        font=stylesheet.SUBTITLE_FONT,
        anchor="w",
        justify="left"
    )
    subtitle.pack(fill="x", padx=stylesheet.SUBTITLE_PADX, pady=(stylesheet.SUBTITLE_PADY_TOP, stylesheet.SUBTITLE_PADY_BOTTOM))

# --- Table number label ---
def create_table_number_label(parent, number):
    number_label = tk.Label(
        parent,
        text=str(number),
        width=stylesheet.NUMBER_WIDTH,
        bg=stylesheet.ACCENT_PRIMARY_COLOR,
        fg=stylesheet.TEXT_PRIMARY_COLOR,
    )
    return number_label

# --- Table row separator ---
def create_table_row_separator(parent):
    row_separator = tk.Frame(
        parent,
        height=stylesheet.SEPARATOR_HEIGHT,
        bg=stylesheet.SEPARATOR_COLOR
    )
    row_separator.pack(fill="x")
    return row_separator


# --- Table column headers ---
def create_table_column_header(parent, labels):
    header = tk.Frame(parent)
    header.pack(fill="x")

    for col, text in enumerate(labels):
        tk.Label(
            header,
            text=text,
            bg=stylesheet.TABLE_HEADER_BACKGROUND_COLOR,
            fg=stylesheet.TEXT_SECONDARY_COLOR,
            font=stylesheet.TABLE_HEADER_FONT,
            anchor="w" if col < 2 else "e",
            padx=stylesheet.TABLE_HEADER_PADX if col < 2 else 40,
            width=8 if col == 0 else None # Add this width value in ui_styles.py
        ).grid(row=0, column=col, sticky="w" if col < 2 else "e")
    
    return header

# --- Table scope headers ---
def create_table_scope_header(parent, text):
    header = tk.Frame(
        parent,
        bg=stylesheet.TABLE_HEADER_BACKGROUND_COLOR
    )
    header.pack(fill="x", pady=(10, 0)) # Add these values to ui_styles.py

    label = tk.Label(
        header,
        text=text,
        bg=stylesheet.TABLE_HEADER_BACKGROUND_COLOR,
        fg=stylesheet.TEXT_SECONDARY_COLOR,
        anchor="w",
        padx=stylesheet.TABLE_HEADER_PADX,
        pady=stylesheet.TABLE_HEADER_PADY
    )
    label.pack(fill="x")

    return header

# --- Likert question row ---
def create_likert_row(parent, row_index, number, statement, var, options):
    likert_row_bg = (
        stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR
        if row_index % 2 == 0
        else stylesheet.TABLE_ROW_SECONDARY_BACKGROUND_COLOR
    )

    likert_row = tk.Frame(parent, bg=likert_row_bg)
    likert_row.pack(fill="x", pady=stylesheet.ROW_PADY)
    likert_row.grid_columnconfigure(1, weight=1)

    # -- Number label --
    number_label = create_table_number_label(likert_row, number)
    number_label.grid(row=0, column=0, sticky="w", padx=stylesheet.ROW_INNER_PADX)
    
    # -- Statement label --
    statement_label = tk.Label(
        likert_row,
        text=statement,
        bg=likert_row_bg,
        fg=stylesheet.TEXT_PRIMARY_COLOR,
        font=stylesheet.TEXT_FONT,
        anchor="w",
        justify="left",
        wraplength=stylesheet.STATEMENT_WRAP
    )
    statement_label.grid(row=0, column=1, sticky="w", padx=stylesheet.STATEMENT_PADX, pady=stylesheet.STATEMENT_PADY)

    likert_frame = tk.Frame(likert_row, bg=likert_row_bg)
    likert_frame.grid(row=0, column=2, padx=20, pady=8, sticky="e") # Add padx and pady values to ui_styles.py

    # -- Likert buttons --
    likert_buttons = []

    def update_buttons():
        current = var.get()
        for value, widget in likert_buttons:
            widget.config(
                relief="sunken" if current == value else "raised",
                bg=stylesheet.CONTROL_SECONDARY_BACKGROUND_ACTIVE_COLOR if current == value else stylesheet.CONTROL_SECONDARY_BACKGROUND_COLOR,
                fg=stylesheet.TEXT_SECONDARY_COLOR if current == value else stylesheet.TEXT_PRIMARY_COLOR
            )
    
    for col, value in enumerate(options):
        likert_button = tk.Label(
            likert_frame,
            text=value,
            width=stylesheet.LIKERT_BUTTON_WIDTH,
            bd=1, # Add this value to ui_styles.py
            relief="raised",
            bg=stylesheet.CONTROL_PRIMARY_BACKGROUND_COLOR,
            fg=stylesheet.TEXT_PRIMARY_COLOR,
            font=stylesheet.BUTTON_FONT
        )
        likert_button.grid(row=0, column=col, padx=stylesheet.LIKERT_BUTTON_PADX)

        likert_button.bind("<Button-1>", lambda e, v=value: (var.set(v), update_buttons()))
        likert_buttons.append((value, likert_button))

# --- Radio question block ---
def create_radio_question(parent, number, question_text, options, variable):
    container = tk.Frame(
        parent,
        bg=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR
    )
    container.pack(fill="x")

    # -- Question row --
    question_row = tk.Frame(
        container,
        bg=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR
    )
    question_row.pack(fill="x", padx=stylesheet.ROW_INNER_PADX, pady=stylesheet.ROW_INNER_PADY)
    
    # -- Number label --
    number_label = create_table_number_label(question_row, number)
    number_label.grid(row=0, column=0, sticky="w", padx=stylesheet.ROW_INNER_PADX)

    # -- Question text --
    question_label = tk.Label(
        question_row,
        text=question_text,
        bg=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR,
        fg=stylesheet.TEXT_PRIMARY_COLOR,
        font=stylesheet.TEXT_FONT,
        anchor="w",
        justify="left",
        wraplength=stylesheet.STATEMENT_WRAP
    )
    question_label.pack(side="left", padx=stylesheet.STATEMENT_PADX, fill="x", expand=True)

    # -- Options --
    options_frame = tk.Frame(
        container,
        bg=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR
    )
    options_frame.pack(fill="x", padx=(stylesheet.NUMBER_WIDTH * 8, 0), pady=(0, 8)) # Add these number values to ui_styles.py

    for option in options:
        rb = tk.Radiobutton(
            options_frame,
            text=option,
            variable=variable,
            value=option,
            bg=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR,
            fg=stylesheet.TEXT_PRIMARY_COLOR,
            font=stylesheet.TEXT_FONT,
            activebackground=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR,
            selectcolor=stylesheet.TABLE_ROW_PRIMARY_BACKGROUND_COLOR,
            anchor="w"
        )
        rb.pack(anchor="w")

    # -- Separator --
    row_separator = create_table_row_separator(container)


    return container

sdfdsfsfsdfdsfds