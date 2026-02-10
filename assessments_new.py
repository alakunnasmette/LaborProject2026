# assessments.py
import tkinter as tk
from tkinter import messagebox
import write_assessments_to_excel # write_assessments_to_excel.py

ROW_BG_1 = "#eeeeee"
ROW_BG_2 = "#e0e0e0"
CELL_BORDER = "#b3b3b3"

DARK_GREY = "#727272"
LIGHT_GREY = "#b3b3b3"
TEXT_FONT = ("Segoe UI", 11)

# --------- Likert-scale: 1 t/m 5 ---------
LIKERT_OPTIONS = [
    ("1", "Oneens"),
    ("2", "Deels oneens"),
    ("3", "Neutraal"),
    ("4", "Deels eens"),
    ("5", "Volledig eens"),
]

# --------- Big Five items (1 t/m 50) ---------
BIG_FIVE_ITEMS = [
    (1, "Ik ben het middelpunt van het feest."),
    (2, "Ik voel me weinig bezorgd om anderen."),
    (3, "Ik ben altijd voorbereid."),
    (4, "Ik raak niet snel gestrest."),
    (5, "Ik heb een rijk vocabulaire."),
    (6, "Ik praat niet veel."),
    (7, "Ik ben oprecht geïnteresseerd in anderen."),
    (8, "Ik vergeet met regelmaat mijn spullen."),
    (9, "Ik ben meestal ontspannen."),
    (10, "Ik heb moeite om abstracte ideeën te begrijpen."),
    (11, "Ik voel me comfortabel bij mensen."),
    (12, "Ik beledig mensen"),
    (13, "Ik besteed aandacht aan details."),
    (14, "Ik maak me niet vaak zorgen."),
    (15, "Ik heb een levendige verbeelding."),
    (16, "Ik blijf liever op de achtergrond."),
    (17, "Ik sympathiseer met de gevoelens van anderen."),
    (18, "Ik maak al snel een chaos van een situatie."),
    (19, "Ik voel me vaak droevig."),
    (20, "Ik ben niet geïnteresseerd in abstracte ideeën."),
    (21, "Ik begin gesprekken."),
    (22, "Ik ben niet geïnteresseerd in de problemen van anderen."),
    (23, "Ik krijg een klus meteen gedaan."),
    (24, "Ik raak niet snel afgeleid."),
    (25, "Ik heb uitstekende ideeën."),
    (26, "Ik heb over het algemeen weinig te zeggen."),
    (27, "Ik heb een zacht hart."),
    (28, "Ik vergeet vaak om objecten op de juiste plaats terug te zetten."),
    (29, "Ik raak niet gemakkelijk overstuur."),
    (30, "Ik heb geen goede verbeelding."),
    (31, "Ik praat met veel verschillende mensen op een feest."),
    (32, "Ik ben niet echt geïnteresseerd in anderen."),
    (33, "Ik ben gesteld op orde."),
    (34, "Mijn humeur verandert niet vaak."),
    (35, "Ik begrijp zaken snel."),
    (36, "Ik houd er niet van de aandacht op mezelf te vestigen."),
    (37, "Ik neem de tijd voor anderen."),
    (38, "Ik onttrek me van mijn plichten."),
    (39, "Ik ervaar vrijwel geen stemmingswisselingen."),
    (40, "Ik gebruik moeilijke woorden."),
    (41, "Ik heb er geen probleem mee om het centrum van de aandacht te zijn."),
    (42, "Ik voel de emoties van anderen."),
    (43, "Ik volg graag schema's."),
    (44, "Ik raak niet snel geïrriteerd."),
    (45, "Ik besteed tijd aan het reflecteren op zaken."),
    (46, "Ik ben stil rondom vreemden."),
    (47, "Ik laat mensen zich op hun gemak voelen."),
    (48, "Ik stel hoge eisen aan de kwaliteit van mijn werk."),
    (49, "Ik voel me zelden droevig."),
    (50, "Ik zit vol met ideeën."),
]


# -------------------- Helpers --------------------
def clear_frame(frame: tk.Widget) -> None:
    for w in frame.winfo_children():
        w.destroy()


def get_assessment_results(parent_frame: tk.Frame) -> dict[int, int | None]:
    """
    Retrieve all entered answers from parent_frame.assessment_vars.
    Returns a dict: {number: int(value) or None if empty}
    """
    results: dict[int, int | None] = {}
    vars_dict = getattr(parent_frame, "assessment_vars", {})

    for nummer, var in vars_dict.items():
        value = var.get().strip()
        results[nummer] = int(value) if value else None

    return results


def make_likert_row(parent: tk.Frame, nummer: int, stelling: str, var: tk.StringVar) -> None:
    """One row: number + position + 1..5 buttons (right-aligned)."""

    row = tk.Frame(parent, bg=LIGHT_GREY)
    row.pack(fill="x", pady=1)

    # make sure that column 2 (position) stretches, so that column 3 is always on the right
    row.grid_columnconfigure(1, weight=1)

    # Nummer (geel)
    num_label = tk.Label(
        row,
        text=str(nummer),
        width=4,
        bg="#f1c40f",
        fg="black",
        font=("Segoe UI", 10, "bold"),
        anchor="c",
    )
    num_label.grid(row=0, column=0, padx=(10, 10), sticky="w")

    # Stat
    stmt_label = tk.Label(
        row,
        text=stelling,
        bg=LIGHT_GREY,
        fg="white",
        font=TEXT_FONT,
        anchor="w",
        justify="left",
        wraplength=650,
    )
    stmt_label.grid(row=0, column=1, sticky="w", padx=10, pady=8)

    # Likert buttons (right)
    likert_frame = tk.Frame(row, bg=LIGHT_GREY)
    likert_frame.grid(row=0, column=2, padx=20, pady=8, sticky="e")

    buttons: list[tuple[str, tk.Label]] = []

    def update_buttons():
        current = var.get()
        for value, widget in buttons:
            if current == value:
                widget.config(relief="sunken", bg="#4d4d4d", fg="white")
            else:
                widget.config(relief="raised", bg="#d9d9d9", fg="black")

    for col, (value, _label_text) in enumerate(LIKERT_OPTIONS):
        btn = tk.Label(
            likert_frame,
            text=value,
            width=3,
            bd=1,
            relief="raised",
            bg="#d9d9d9",
            fg="black",
            font=("Segoe UI", 10),
        )
        btn.grid(row=0, column=col, padx=4)

        def on_click(event, v=value):
            var.set(v)
            update_buttons()

        btn.bind("<Button-1>", on_click)
        buttons.append((value, btn))

    update_buttons()


# -------------------- Page builder --------------------
def build_assessments_page(parent_frame: tk.Frame, navigate) -> None:
    """
    Builds the Big Five 1.1 questionnaire in the right screen.
    Navigate is the router from app.py, so you can use: navigate("phase2.0") etc.
    """
    clear_frame(parent_frame)

    # ---------- scrollbar container ----------
    container = tk.Frame(parent_frame, bg="white")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(canvas, bg="white")
    window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(_event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_resize(event):
        canvas.itemconfig(window_id, width=event.width)

    scroll_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_resize)

    # Mousewheel (Windows)
    def on_mousewheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ---------- title and explanation ----------
    title = tk.Label(
        scroll_frame,
        text="Fase 1.1 – Big Five persoonlijkheidsdimensies",
        bg="white",
        fg="black",
        font=("Segoe UI", 14, "bold"),
        anchor="w",
    )
    title.pack(fill="x", padx=20, pady=(15, 5))

    subtitle = tk.Label(
        scroll_frame,
        text=(
            "Beoordeel elke stelling in het algemeen voor jezelf.\n"
            "1 = oneens · 2 = deels oneens · 3 = neutraal · 4 = deels eens · 5 = volledig eens."
        ),
        bg="white",
        fg="black",
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    )
    subtitle.pack(fill="x", padx=20, pady=(0, 15))

    # ---------- column headings ----------
    header = tk.Frame(scroll_frame, bg=DARK_GREY)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Nummer",
        bg=DARK_GREY,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=8,
        anchor="w",
        padx=10,
    ).grid(row=0, column=0, sticky="w")

    tk.Label(
        header,
        text="Stelling",
        bg=DARK_GREY,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        anchor="w",
        padx=10,
    ).grid(row=0, column=1, sticky="w")

    tk.Label(
        header,
        text="",
        bg=DARK_GREY,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        anchor="e",
        padx=40,
    ).grid(row=0, column=2, sticky="e")

    # ---------- all items ----------
    parent_frame.assessment_vars = {}

    questions_container = tk.Frame(scroll_frame, bg="white")
    questions_container.pack(fill="both", expand=True)

    for nummer, tekst in BIG_FIVE_ITEMS:
        var = tk.StringVar(value="")
        parent_frame.assessment_vars[nummer] = var
        make_likert_row(questions_container, nummer, tekst, var)

    # spacer
    tk.Frame(scroll_frame, bg="white", height=10).pack(fill="x")

    # ---------- Save and continue button ----------
    def on_submit():
        results = get_assessment_results(parent_frame)

        missing = [nr for nr, v in results.items() if v is None]
        if missing:
            messagebox.showwarning(
                "Onvolledige vragenlijst",
                f"Er zijn nog {len(missing)} stellingen niet ingevuld."
            )
            return

        # (optional) save results for later use/export
        parent_frame.assessment_results = results

        # -> go to Phase 2.0
        navigate("phase2.0")

    btn_frame = tk.Frame(scroll_frame, bg="white")
    btn_frame.pack(fill="x", pady=(5, 20))

    btn_submit = tk.Button(
        btn_frame,
        text="Opslaan en verder",
        bg="#4d4d4d",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=5,
        command=on_submit,
    )
    btn_submit.pack(side="right", padx=30)

    # extra space at the bottom
    tk.Frame(scroll_frame, bg="white", height=30).pack(fill="x")
