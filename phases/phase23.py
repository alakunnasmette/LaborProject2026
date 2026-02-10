import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.ui_components import clear_frame
from utils.write_assessments_to_excel import add_job_characteristics_to_excel

# ==================== Job Characteristics Model Data ====================
JOB_CHARACTERISTICS_MODEL = [
    (1, "Taakvaardigheid",
        "De mate waarin een baan verschillende activiteiten vereist, waarbij de werknemer een verscheidenheid aan vaardigheden en talenten moet ontwikkelen. Werknemers kunnen meer betekenis ervaren in banen die verschillende vaardigheden en capaciteiten vereisen dan wanneer de banen elementair en routinematig zijn.",
        "Hoe belangrijk vind je het dat je werk bestaat uit verschillende soorten activiteiten waarbij je diverse vaardigheden en talenten kunt inzetten en/of ontwikkelen? En wat zou voor jou een ideale verhouding zijn tussen afwisselende taken en meer routinematige werkzaamheden?"),

    (2, "Taakidentiteit",
        "De mate waarin de functie vereist dat de functiehouders een werkstuk identificeren en voltooien met een zichtbaar resultaat. Werknemers ervaren meer zingeving in een baan wanneer ze betrokken zijn bij het hele proces in plaats van alleen verantwoordelijk te zijn voor een deel van het werk.",
        "Hoe belangrijk vind je het om in je werk betrokken te zijn bij een volledig proces of werkstuk, van begin tot eind, met een duidelijk zichtbaar resultaat? En in hoeverre zou je idealiter verantwoordelijk willen zijn voor het hele werkproces versus alleen een deel ervan?"),

    (3, "Taakbetekenis",
        "De mate waarin de baan het leven van anderen beïnvloedt. De invloed kan zowel in de directe organisatie als in de externe omgeving zijn. Werknemers ervaren meer zingeving in een baan die het psychisch of fysiek welzijn van anderen aanzienlijk verbetert, dan een baan die een beperkt effect heeft op iemand anders.",
        "Hoe belangrijk vind je het dat je werk een merkbare invloed heeft op het leven of welzijn van anderen, binnen en/of buiten de organisatie? En in welke mate zou je idealiter willen dat jouw werk impact heeft op anderen?"),

    (4, "Autonomie",
        "De mate waarin de baan de werknemer aanzienlijke vrijheid, onafhankelijkheid en discretie biedt om het werk te plannen en de procedures in de baan te bepalen. Voor banen met een hoge mate van autonomie hangen de resultaten van het werk af van de eigen inspanningen, initiatieven en beslissingen van de werknemers. In plaats van in opdracht van een manager of een handleiding met werkprocedures. In dergelijke gevallen ervaren de werknemers een grotere persoonlijke verantwoordelijkheid voor hun eigen successen en mislukkingen op het werk.",
        "Hoe belangrijk vind je het om in je werk zelf te kunnen bepalen hoe en wanneer je taken uitvoert, zonder dat alles strak voorgeschreven is? En hoeveel vrijheid zou je idealiter willen hebben in het plannen en uitvoeren van je werk?"),

    (5, "Feedback",
        "De mate waarin de werknemer kennis heeft van resultaten. Dit is duidelijke, specifieke, gedetailleerde, bruikbare informatie over de effectiviteit van zijn of haar werkprestaties. Wanneer werknemers duidelijke, bruikbare informatie over hun werkprestaties ontvangen, hebben ze een betere algemene kennis van het effect van hun werkactiviteiten en welke specifieke acties ze moeten ondernemen (indien aanwezig) om hun productiviteit te verbeteren.",
        "Hoe belangrijk vind je het om duidelijke en bruikbare feedback te krijgen over hoe goed je je werk doet? En in welke mate zou je idealiter op de hoogte willen zijn van het effect van je werk en van punten waarop je jezelf kunt verbeteren?"),
]

# ==================== Styles ====================
S = {
    "bg": "#ffffff",
    "dark": "#727272",
    "odd": "#eeeeee",   
    "even": "#e0e0e0",
    "yellow": "#f1c40f",
    "btn": "#d9d9d9",
    "btn_on": "#4d4d4d",
    "f_title": ("Segoe UI", 14, "bold"),
    "f_sub": ("Segoe UI", 10),
    "f": ("Segoe UI", 10),
    "f_b": ("Segoe UI", 10, "bold"),
    "f_small": ("Segoe UI", 9),
}

# ==================== Build Function ====================
def build_job_characteristics_models_page(parent_frame: tk.Frame, navigate=None) -> None:
    """Build the Job Characteristics Models page with text input fields."""
    
    clear_frame(parent_frame)
    
    # =================== Scrollable container ===================
    container = tk.Frame(parent_frame, bg=S["bg"])
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=S["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(canvas, bg=S["bg"])
    window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_resize(event):
        canvas.itemconfig(window_id, width=event.width)

    scroll_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_mousewheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # =================== Headers ===================
    title = tk.Label(
        scroll_frame,
        text="Fase 2.3 – Werk karakteristieken modellen",
        bg=S["bg"],
        fg="black",
        font=S["f_title"],
        anchor="w",
    )
    title.pack(fill="x", padx=20, pady=(15, 5))

    subtitle = tk.Label(
        scroll_frame,
        text="Geef je eigen antwoord op elke vraag. Typ je gedachten, gevoelens en ervaringen in het tekstvak.",
        bg=S["bg"],
        fg="#555555",
        font=S["f_sub"],
        anchor="w",
        justify="left",
        wraplength=700,
    )
    subtitle.pack(fill="x", padx=20, pady=(0, 20))

    # =================== Dictionary to store text entries ===================
    text_entries = {}

    # =================== Build question cards ===================
    for idx, (q_num, characteristic, description, question) in enumerate(JOB_CHARACTERISTICS_MODEL):
        # Outer container for header (above) and card (below)
        outer = tk.Frame(scroll_frame, bg=S["bg"])
        outer.pack(fill="x", padx=15, pady=8)

        # Header above the box: yellow background with an outline
        header_frame = tk.Frame(outer, bg=S["yellow"], relief="solid", bd=1)
        header_frame.pack(fill="x", pady=(0, 4))

        header = tk.Label(
            header_frame,
            text=f"{q_num}. {characteristic}",
            bg=S["yellow"],
            fg="black",
            font=S["f_b"],
            anchor="w",
            wraplength=700,
            justify="left",
        )
        header.pack(fill="x", padx=12, pady=6)

        # Card background (content box)
        card = tk.Frame(outer, bg=S["odd"] if idx % 2 == 0 else S["even"], relief="solid", bd=1)
        card.pack(fill="x")

        # Description
        desc_label = tk.Label(
            card,
            text=description,
            bg=card.cget("bg"),
            fg="#000000",
            font=S["f_small"],
            anchor="w",
            wraplength=700,
            justify="left",
        )
        desc_label.pack(fill="x", padx=12, pady=(0, 10))

        # Question
        question_label = tk.Label(
            card,
            text=question,
            bg=card.cget("bg"),
            fg="black",
            font=S["f"],
            anchor="w",
            wraplength=700,
            justify="left",
        )
        question_label.pack(fill="x", padx=12, pady=(0, 8))

        # Text input box (multi-line)
        text_box = tk.Text(
            card,
            height=4,
            width=80,
            font=S["f"],
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            wrap="word",
            padx=8,
            pady=6,
        )
        text_box.pack(fill="x", padx=12, pady=(0, 12))
        
        # Store reference to text box
        text_entries[q_num] = text_box

    # =================== Submit Button ===================
    button_frame = tk.Frame(scroll_frame, bg=S["bg"])
    button_frame.pack(fill="x", padx=20, pady=20)

    def on_submit():
        """Validate and submit answers."""
        # Check if all fields are filled
        missing = []
        for q_num, text_box in text_entries.items():
            answer = text_box.get("1.0", "end-1c").strip()
            if not answer:
                missing.append(q_num)

        if missing:
            messagebox.showwarning(
                "Onvolledige vragenlijst",
                f"Vraag(en) {missing} nog niet ingevuld. Vul alle vragen in alvorens verder te gaan."
            )
            return

        # Save answers to dictionary
        answers = {q_num: text_box.get("1.0", "end-1c").strip() for q_num, text_box in text_entries.items()}
        
        # Save to Excel file if it exists
        if hasattr(parent_frame, 'excel_file_path') and parent_frame.excel_file_path:
            success = add_job_characteristics_to_excel(parent_frame.excel_file_path, answers)
            if success:
                messagebox.showinfo("Succes", "Je antwoorden zijn opgeslagen!")
            else:
                messagebox.showwarning("Waarschuwing", "Antwoorden konden niet naar Excel-bestand worden geschreven.")
        else:
            messagebox.showinfo("Succes", "Je antwoorden zijn opgeslagen!")

        # Navigate to home or next section
        if navigate:
            navigate("home")

    tk.Button(
        button_frame,
        text="Opslaan en verder",
        bg=S["btn_on"],
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=8,
        command=on_submit
    ).pack(side="right")