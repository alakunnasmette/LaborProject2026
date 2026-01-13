# assessments.py
import tkinter as tk
from tkinter import messagebox


ROW_BG_1 = "#eeeeee"
ROW_BG_2 = "#e0e0e0"
CELL_BORDER = "#b3b3b3"

DARK_GREY = "#727272"
LIGHT_GREY = "#b3b3b3"
TEXT_FONT = ("Segoe UI", 11)

# --------- Likert scale: 1–5 ---------
LIKERT_OPTIONS = [
    ("1", "Oneens"),
    ("2", "Deels oneens"),
    ("3", "Neutraal"),
    ("4", "Deels eens"),
    ("5", "Volledig eens"),
]

# --------- Big Five items: 25–50 ---------
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

# Test function save and continue
def get_assessment_results(parent_frame: tk.Frame) -> dict:
    """
    Retrieve all entered answers from parent_frame.assessment_vars.
    Returns a dict: {number: int(value) or "None" if empty}
    """
    results = {}
    vars_dict = getattr(parent_frame, "assessment_vars", {})

    for number, var in vars_dict.items():
        value = var.get().strip()
        results[number] = int(value) if value else None

    return results


def clear_frame(frame: tk.Frame) -> None:
    """Remove all widgets from a frame."""
    for w in frame.winfo_children():
        w.destroy()

def make_likert_row(parent: tk.Frame, number: int, stelling: str, var: tk.StringVar) -> None:
    """Creates a single Likert scale row with a number, statement, and 1 to 5 selection buttons."""

    row = tk.Frame(parent, bg=LIGHT_GREY)
    row.pack(fill="x", pady=1)

    # Make sure that the position of column 2 stretches, so that column 3 is always on the right
    row.grid_columnconfigure(1, weight=1)

    # --------- Number ---------
    num_label = tk.Label(
        row,
        text=str(number),
        width=4,
        bg="#f1c40f",
        fg="black",
        font=("Segoe UI", 10, "bold"),
        anchor="c",
    )
    num_label.grid(row=0, column=0, padx=(10, 10), sticky="w")

    # --------- Statement ---------
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

    # --------- Likert buttons 1..5 ---------
    likert_frame = tk.Frame(row, bg=LIGHT_GREY)
    likert_frame.grid(row=0, column=2, padx=20, pady=8, sticky="e")

    buttons = []

    def update_buttons():
        """Visually display which value has been chosen."""
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

    # Start with unselected buttons
    update_buttons()

def build_assessments_page(parent_frame: tk.Frame, on_next_page) -> None: #test#
    """Bouwt de Big Five 1.1 vragenlijst in het rechter scherm."""

    clear_frame(parent_frame)

    # ---------- Scrollable container ----------
    container = tk.Frame(parent_frame, bg="white")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(canvas, bg="white")
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

    # ---------- Title and explanation ----------
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
            "Beoordeel elke stelling in het algemeen voor uzelf.\n"
            "1 = oneens · 2 = deels oneens · 3 = neutraal · 4 = deels eens · 5 = volledig eens."
        ),
        bg="white",
        fg="black",
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    )
    subtitle.pack(fill="x", padx=20, pady=(0, 15))

    # ---------- Column headers ----------
    header = tk.Frame(scroll_frame, bg=DARK_GREY)
    header.pack(fill="x")

    tk.Label(
        header,
        text="number",
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
        bg=DARK_GREY,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        anchor="e",
        padx=40,
    ).grid(row=0, column=2, sticky="e")

    # ---------- Items ----------
    parent_frame.assessment_vars = {}

    questions_container = tk.Frame(scroll_frame, bg="white")
    questions_container.pack(fill="both", expand=True)

    for number, text in BIG_FIVE_ITEMS:
        var = tk.StringVar(value="")
        parent_frame.assessment_vars[number] = var
        make_likert_row(questions_container, number, text, var)

    # Small spacer
    tk.Frame(scroll_frame, bg="white", height=10).pack(fill="x")

    # ---------- Save and continue button ----------
    def on_submit():
        results = get_assessment_results(parent_frame)

        # Check if there are any empty answers
        missing = [nr for nr, v in results.items() if v is None]
        if missing:
            messagebox.showwarning(
                "Onvolledige vragenlijst",
                f"Er zijn nog {len(missing)} stellingen niet ingevuld."
            )
            return

        # If everything is filled in, continue to the next page
        on_next_page()


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

    # Extra space beneath
    tk.Frame(scroll_frame, bg="white", height=30).pack(fill="x")



# ----------------------------- Phase 2.0 - Career anchors -----------------------------

# Table colors
ROW_BG_1 = "#eeeeee"
ROW_BG_2 = "#e0e0e0"

# --------- Fase 2.0 – Career anchors: fetch data from Excel ---------
# Each entry: (question number, anchor letter, statement text)
# Anchors: V = Moving upward, W = Feeling safe, X = Being free, Y = Finding balance, Z = Seeking challenge.

CAREER_STATEMENTS = [
    (1, "V", "Graag wil ik het voor mezelf en voor anderen dusdanig regelen dat succes verzekerd is."),
    (1, "X", "Ik houd me binnen een werksituatie het liefst bezig met mijn eigen zaken."),
    (2, "Y", "Binnen het werk moet er tijd zijn voor zaken die jezelf belangrijk vindt en moet er gelegenheid zijn om zinvolle relaties te cultiveren."),
    (2, "V", "Vooruitkomen is voor mij belangrijker dan persoonlijke behoeften."),
    (3, "W", "Ik werk graag in een omgeving waar hard werken, loyaliteit en toewijding gewaardeerd wordt."),
    (3, "X", "Ik houd van een werksituatie waar ik mijn eigen doelen kan stellen en ze kan bereiken op mijn eigen manier en op mijn eigen tempo."),
    (4, "V", "Ik ben strijdlustig, kan goed analyseren en met mensen omgaan."),
    (4, "Y", "Ik kan goed mijn evenwicht bewaren tussen de eisen van mijn werk en die van mijn privé-leven."),
    (5, "X", "Ik wil onafhankelijk werken."),
    (5, "W", "Ik houd ervan me een vertegenwoordiger te voelen van een groter geheel."),
    (6, "Z", "Ik houd ervan als consultant of probleemoplosser te werken en me dusdanig te profileren door middel van een opwindend project."),
    (6, "V", "Ik houd ervan in een situatie te werken waarin ik de leiding heb en verantwoordelijk ben voor het bereiken van bepaalde doelen."),
    (7, "Y", "Mijn echtgenoot/partner is net zo belangrijk voor mij als mijn loopbaan."),
    (7, "Z", "Mijn echtgenoot/partner verdwijnt naar de achtergrond als ik midden in een zeer opwindend project zit."),
    (8, "X", "Het allerbelangrijkst voor mij is vrijheid."),
    (8, "Y", "Het allerbelangrijkst voor mij is een doel in mijn leven."),
    (9, "W", "Ik ben bekwaam, loyaal, betrouwbaar en ik werk hard."),
    (9, "Z", "Ik ben sociaal en in de omgang, een goede leider en een goede organisator."),
    (10, "X", "Ik ben onafhankelijk."),
    (10, "Y", "Ik ben evenwichtig."),
    (11, "Z", "Ik ben iemand die in actie komt door opwindende projecten."),
    (11, "Y", "Ik ben iemand die graag met anderen werkt."),
    (12, "X", "Ik ben ambitieus en iemand die graag met anderen wedijvert."),
    (12, "W", "Ik ben iemand die een medewerker zijn met wie men kan rekenen."),
    (13, "Z", "Ik voel zelfvertrouwen en ben in staat mezelf te redden."),
    (13, "V", "Ik heb veel fantasie en enthousiasme."),
    (14, "W", "Ik ben stabiel en vasthoudend."),
    (14, "X", "Ik ben onafhankelijk en in staat een eigen koers te bepalen."),
    (15, "Y", "Ik ben iemand die goed kan plannen en coördineren."),
    (15, "Z", "Ik ben iemand die situaties analyseert en creatieve, nieuwe oplossingen ontwikkelt."),
    (16, "V", "Ik ben een expert op mijn terrein."),
    (16, "W", "Ik ben een betrouwbare en degelijk persoon."),
    (17, "Y", "Ik ben iemand die wil werken volgens vaststaande procedures."),
    (17, "X", "Ik ben iemand die probeert de doelen in het werk in overeenstemming te brengen met het persoonlijk nastreven."),
    (18, "Z", "Een persoonlijk doel is om mijn eigen lot te bepalen."),
    (18, "Y", "Een persoonlijk doel is om mijn werk te verweven met mijn privé-leven."),
    (19, "W", "Ik vind het belangrijk een veilige baan te hebben en het gevoel te hebben erbij te horen."),
    (19, "X", "Ik vind het belangrijk om tijd te kunnen besteden aan mijn privé-leven en hobby’s."),
    (20, "V", "Ik geef de voorkeur aan een carrière waarin veel promotiekansen voorhanden zijn."),
    (20, "Z", "Ik geef de voorkeur aan om in staat gesteld te worden uitdagende problemen en taken aan te pakken."),
    (21, "Y", "Ik ben graag in een werksituatie waar invloed uitgeoefend kan worden."),
    (21, "W", "Ik waardeer een baan waar je langere tijd kunt blijven werken en waar je gewaardeerd en geaccepteerd wordt."),
    (22, "V", "Ik denk dat de juiste mensen en goede vrienden maken belangrijk is om vooruit te komen."),
    (22, "Z", "Ik denk dat het essentieel is om interessesgebieden te ontwikkelen."),
    (23, "Y", "Voor mij geldt als basis het scheppen van een evenwicht tussen mijn privé-leven en mijn werk."),
    (23, "W", "Voor mij geldt als basis stabiliteit, waardering en een veilige plaats binnen mijn werksituatie."),
    (24, "X", "Ik denk dat ik graag een positie zou willen hebben met een maximum aan zelfstandigheid."),
    (24, "V", "Ik denk dat ik graag tot \"de kring van ingewijden\" zou willen behoren."),
    (25, "W", "Voor mij geldt als basis stabiliteit, waardering en een veilige plaats op het werk."),
    (25, "V", "Als basis geldt voor mij dat ik vooruit wil komen in de werkomgeving."),
    (26, "V", "Ik denk dat geld, macht en aanzien een belangrijke maatstaf zijn van een succesvolle loopbaan."),
    (26, "Y", "Ik denk dat een loopbaan succesvol is als je evenveel tijd hebt voor het werk, het gezin en je eigen ontwikkeling."),
    (27, "Z", "Ik wil liever uitblinken op mijn gebied."),
    (27, "W", "Ik wil liever beschouwd worden als betrouwbaar en loyaal."),
    (28, "W", "Ik geef de voorkeur aan het werken met een team op lange termijn en een hechte basis."),
    (28, "Z", "Ik geef de voorkeur aan het werken met een taakgerichte of projectgroep op korte termijn basis en in een hoog tempo."),
    (29, "Z", "Ik geef de voorkeur aan professionele ontwikkeling en permanente training."),
    (29, "X", "Ik geef de voorkeur aan professionele ontwikkeling om een expert te worden en om meer flexibiliteit en onafhankelijkheid te verkrijgen."),
    (30, "Y", "Ik geef de voorkeur aan een werksituatie die een evenwicht garandeert tussen mijn privé-leven en mijn werk."),
    (30, "Z", "Ik geef de voorkeur aan een werksituatie die opwindend is en mij stimuleert."),
]

# Descriptions of the 5 career anchors
CAREER_ANCHOR_DESCRIPTIONS = {
    "Omhoog komen": "Deze op opwaartse mobiliteit gerichte loopbaanoriëntatie wordt gewoonlijk geassocieerd met het vooruitkomen in een hiërarchische en/of statusgevoelige organisatie. Het verwerven van steeds meer invloed speelt in deze kaders een grote rol. Prestige en beloning nemen bij iedere opwaartse beweging toe.",
    "Veilig voelen": "Sommige personen hebben behoefte aan een veilige baan in een duidelijke organisatie die vooral gekenmerkt wordt door orde en rust. Zij geven de voorkeur aan een lang en vast dienstverband, erkenning en appreciatie door de werkgever. In ruil daarvoor bieden ze een loyale en toegewijde instelling en zijn ze niet bang om hard te werken. Onderling respect, wederkerigheid en loyaliteit karakteriseren de werkhouding.",
    "Vrij zijn": "Personen met deze loopbaanoriëntatie zijn er op uit hun grenzen te verkennen. De nadruk ligt bij hen meer op het verwerven van persoonlijke autonomie, ruimte en verantwoordelijkheid voor het bereiken van resultaten dan op gebondenheid, zekerheid en vaste regels. Men is bereid zeer hard te werken als daar gunstige voorwaarden tegenover staan in de sfeer van onafhankelijkheid en zelfcontrole. Interessant werk is belangrijk maar individuele vrijheid is het uiteindelijke doel.",
    "Balans vinden": "De meeste mensen streven naar evenwicht maar zelden vormt dit het basis uitgangspunt voor hun loopbaanbeslissingen. Sommige mensen zoeken echter een optimaal evenwicht tussen werk, privé-leven en zelfontwikkeling. Het werk vormt voor hen slechts één dimensie van hun totale levensvervulling. De aandacht voor werk en privé-leven kan verschillen afhankelijk van de situatie waarin personen met deze loopbaanoriëntatie zich bevinden. Individuen die de kwaliteit van het leven hoog in het vaandel dragen, vallen dikwijls in deze categorie.",
    "Uitdaging zoeken": "Deze loopbaanoriëntatie wordt gekenmerkt door de behoefte aan opwinding en uitdaging en een sterke betrokkenheid bij het werk. Men is er op gericht dichtbij het centrum van actie, avontuur en creativiteit te zijn en heeft er zeer veel moeite mee zich aan het werk los te maken. Een bureaucratische organisatie wordt als bijzonder remmend ervaren. Autonomie is belangrijk maar het belangrijkste is opwindend en uitdagend werk.",
}


def build_career_anchors_page(parent_frame: tk.Frame) -> None:
    """Show Phase 2.0 – Career Anchors in content."""

    clear_frame(parent_frame)

    # =================== Scrollable container ===================
    container = tk.Frame(parent_frame, bg="white")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(canvas, bg="white")
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
        text="Fase 2.0 | Wat wil de cliënt? | Identificatie van de loopbaanwaarden",
        bg="white",
        fg="black",
        font=("Segoe UI", 14, "bold"),
        anchor="w",
    )
    title.pack(fill="x", padx=20, pady=(20, 2))

    subtitle = tk.Label(
        scroll_frame,
        text=(
            "Beoordeling van stelling a.h.v. onderstaande criteria:\n"
            "Met welke stelling kan cliënt zich het sterkst identificeren?"
        ),
        bg="white",
        fg="black",
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    )
    subtitle.pack(fill="x", padx=20, pady=(0, 15))

    # =================== Table headers and rows ===================
    table = tk.Frame(scroll_frame, bg="white")
    table.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    # Table columns
    for c in range(7):
        table.grid_columnconfigure(c, weight=0)
    table.grid_columnconfigure(1, weight=1)  # Statement column stretches

    # Header row
    header_bg = DARK_GREY
    headers = [
        ("Nummer", 0),
        ("Stelling", 1),
        ("Omhoog | V", 2),
        ("Veilig | W", 3),
        ("Vrij | X", 4),
        ("Balans | Y", 5),
        ("Uitdaging | Z", 6),
    ]

    for text, col in headers:
        lbl = tk.Label(
            table,
            text=text,
            bg=header_bg,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            anchor="w" if col <= 1 else "center",
        )
        lbl.grid(row=0, column=col, sticky="nsew")

    ANCHORS = ["V", "W", "X", "Y", "Z"]

    # One StringVar per row (statement)
    question_vars: dict[int, tk.StringVar] = {}
    question_buttons: dict[int, list[tuple[str, tk.Radiobutton]]] = {}

    def update_row(row_id: int) -> None:
        """Show an 'X' only in the selected box of this row."""
        current = question_vars[row_id].get()
        for code, btn in question_buttons[row_id]:
            if code == current:
                btn.config(text="1", font=("Segoe UI", 11, "bold"))
            else:
                btn.config(text="", font=("Segoe UI", 11))

    # Amount of lines corresponding to each question number
    question_counts: dict[int, int] = {}
    for number, _anchor, _text in CAREER_STATEMENTS:
        question_counts[number] = question_counts.get(number, 0) + 1

    shown_numbers: set[int] = set()

    # Build all rows
    for row_index, (number, _anchor, text) in enumerate(CAREER_STATEMENTS, start=1):
        row_id = row_index

        question_vars[row_id] = tk.StringVar(value="")
        question_buttons[row_id] = []
        row_bg = ROW_BG_1 if row_index % 2 == 1 else ROW_BG_2

        table.grid_rowconfigure(row_index, weight=0)

        # One yellow block per question number
        if number not in shown_numbers:
            rowspan = question_counts.get(number, 1)
            num_label = tk.Label(
                table,
                text=str(number),
                width=4,
                bg="#f1c40f",
                fg="black",
                font=("Segoe UI", 10, "bold"),
                anchor="c",
            )
            num_label.grid(
                row=row_index,
                column=0,
                rowspan=rowspan,
                padx=(10, 10),
                pady=(2, 2),
                sticky="nsw",
            )
            shown_numbers.add(number)

        # Statement text
        stmt_label = tk.Label(
            table,
            text=text,
            bg=row_bg,
            fg="black",
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
            wraplength=700,
            padx=12,
            pady=6,
        )
        stmt_label.grid(
            row=row_index,
            column=1,
            sticky="nsew",
            padx=(0, 10),
            pady=(2, 2),
        )

        # Five boxes in columns 2..6
        var = question_vars[row_id]
        for offset, code in enumerate(ANCHORS):
            col = 2 + offset

            cell = tk.Frame(
                table,
                bg=row_bg,
                bd=1,
                relief="solid",
                highlightthickness=0,
            )
            cell.grid(
                row=row_index,
                column=col,
                padx=3,
                pady=(2, 2),
                sticky="nsew",
            )

            rb = tk.Radiobutton(
                cell,
                variable=var,
                value=code,
                indicatoron=False,
                text="",  # Becomes an "X" when chosen
                width=2,
                font=("Segoe UI", 11),
                bg=row_bg,
                fg="black",
                activebackground=row_bg,
                activeforeground="black",
                selectcolor=row_bg,
                relief="flat",
                borderwidth=0,
                command=lambda q=row_id: update_row(q),
                cursor="hand2",
            )
            rb.pack(expand=True, fill="both")
            question_buttons[row_id].append((code, rb))

    # Empty content
    for rid in question_vars.keys():
        update_row(rid)

    # Save all choices for later score calculation
    parent_frame.career_vars = question_vars

    # =================== Total score row (placeholders) ===================
    total_frame = tk.Frame(scroll_frame, bg="white")
    total_frame.pack(fill="x", padx=20, pady=(15, 5))

    total_header = tk.Frame(total_frame, bg="black")
    total_header.pack(fill="x")

    tk.Label(
        total_header,
        text="Totaal score",
        bg="black",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        anchor="center",
    ).grid(row=0, column=0, sticky="nsew", padx=(0, 1))

    for i, col_name in enumerate(["Omhoog | V", "Veilig | W", "Vrij | X", "Balans | Y", "Uitdaging | Z"], start=1):
        tk.Label(
            total_header,
            text=col_name,
            bg="black",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="center",
        ).grid(row=0, column=i, sticky="nsew", padx=(1 if i > 1 else 0, 0))

    total_row = tk.Frame(total_frame, bg="#f1c40f")
    total_row.pack(fill="x")

    tk.Label(
        total_row,
        text="",
        bg="#f1c40f",
        fg="black",
        width=15,
    ).grid(row=0, column=0, sticky="nsew")

    parent_frame.total_labels = {}
    for i, key in enumerate(["V", "W", "X", "Y", "Z"], start=1):
        lbl = tk.Label(
            total_row,
            text="0",
            bg="#f1c40f",
            fg="black",
            font=("Segoe UI", 10, "bold"),
            anchor="center",
            width=8,
        )
        lbl.grid(row=0, column=i, sticky="nsew", padx=1)
        parent_frame.total_labels[key] = lbl

    # =================== Score interpretation ===================
    score_box = tk.Frame(scroll_frame, bg="white")
    score_box.pack(fill="x", padx=20, pady=(20, 10))

    tk.Label(
        score_box,
        text="Score-interpretatie (per loopbaananker)",
        bg="white",
        fg="black",
        font=("Segoe UI", 11, "bold"),
        anchor="w",
    ).pack(fill="x", pady=(0, 5))

    tk.Label(
        score_box,
        text="12–10: Sterk   ·   9–7: Neutraal   ·   6–0: Matig",
        bg="white",
        fg="black",
        font=("Segoe UI", 10),
        anchor="w",
    ).pack(fill="x")

    # =================== Career anchor descriptions ===================
    desc_frame = tk.Frame(scroll_frame, bg="white")
    desc_frame.pack(fill="x", padx=20, pady=(20, 20))

    tk.Label(
        desc_frame,
        text="Loopbaanankers – omschrijving",
        bg="white",
        fg="black",
        font=("Segoe UI", 11, "bold"),
        anchor="w",
    ).pack(fill="x", pady=(0, 5))

    for naam, text in CAREER_ANCHOR_DESCRIPTIONS.items():
        box = tk.Frame(desc_frame, bg="#f5f5f5", bd=1, relief="solid")
        box.pack(fill="x", pady=4)

        tk.Label(
            box,
            text=naam,
            bg="#f1c40f",
            fg="black",
            font=("Segoe UI", 10, "bold"),
            width=16,
            anchor="center",
            padx=4,
            pady=4,
        ).pack(side="left", fill="y")

        tk.Label(
            box,
            text=text,
            bg="#f5f5f5",
            fg="black",
            font=("Segoe UI", 10),
            justify="left",
            wraplength=650,
            anchor="w",
            padx=8,
            pady=6,
        ).pack(side="left", fill="both", expand=True)


    # =================== Save and continue button ===================
    def on_submit_loopbaan():
        # Check if each row has a choice
        missing = [row_id for row_id, v in parent_frame.career_vars.items() if not v.get()]
        if missing:
            messagebox.showwarning(
                "Onvolledige vragenlijst",
                f"Er zijn nog {len(missing)} stellingen zonder keuze."
            )
            return

        # Save results to the parent_frame
        parent_frame.career_results = {
            row_id: v.get() for row_id, v in parent_frame.career_vars.items()
        }

        # Empty right panel
        clear_frame(parent_frame)

        # Load Phase 2.1 Career Clusters in the same panel
        frame_21 = create_career_clusters_frame(parent_frame)
        frame_21.pack(fill="both", expand=True)

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
        command=on_submit_loopbaan,
    )
    btn_submit.pack(side="right", padx=30)



# ----------------------------- Phase 2.1 - Career Clusters  -----------------------------


# Data for the 16 career clusters
CAREER_CLUSTERS = [
    {
        "id": 1,
        "segment": "Landbouw, voeding en natuurlijke grondstoffen",
        "description": (
            "Productie, verwerking en ontwikkeling van agrarische grondstoffen, "
            "voedsel en natuurlijke hulpbronnen."
        ),
    },
    {
        "id": 2,
        "segment": "Architectuur en constructie",
        "description": (
            "Ontwerpen, plannen, bouwen en onderhouden van de gebouwde omgeving."
        ),
    },
    {
        "id": 3,
        "segment": "Kunst, audio-visuele technologie en communicatie",
        "description": (
            "Ontwerpen, produceren en presenteren van multimedia, podiumkunsten "
            "en andere creatieve content."
        ),
    },
    {
        "id": 4,
        "segment": "Business Management en administratie",
        "description": (
            "Plannen, organiseren en aansturen van zakelijke processen en "
            "administratieve activiteiten."
        ),
    },
    {
        "id": 5,
        "segment": "Educatie en training",
        "description": (
            "Plannen, verzorgen en ondersteunen van onderwijs- en "
            "opleidingsactiviteiten."
        ),
    },
    {
        "id": 6,
        "segment": "Financiën",
        "description": (
            "Financiële planning, investeringen, bankwezen, verzekeringen en "
            "bedrijfseconomische dienstverlening."
        ),
    },
    {
        "id": 7,
        "segment": "Overheid en publieke administratie",
        "description": (
            "Uitvoering van overheidstaken zoals beleid, regelgeving, belastingen "
            "en publieke administratie."
        ),
    },
    {
        "id": 8,
        "segment": "Gezondheidswetenschappen",
        "description": (
            "Therapeutische, diagnostische en ondersteunende zorg, inclusief "
            "biotechnologisch onderzoek."
        ),
    },
    {
        "id": 9,
        "segment": "Hospitality en toerisme",
        "description": (
            "Management en uitvoering in horeca, logies, recreatie en toeristische "
            "diensten."
        ),
    },
    {
        "id": 10,
        "segment": "Humanitaire dienstverlening",
        "description": (
            "Ondersteunen van mensen en gezinnen via sociale, maatschappelijke en "
            "vrijwilligersdiensten."
        ),
    },
    {
        "id": 11,
        "segment": "ICT",
        "description": (
            "Ontwikkeling, beheer en ondersteuning van hardware, software, "
            "netwerken en digitale media."
        ),
    },
    {
        "id": 12,
        "segment": "Publieke veiligheid en zekerheid",
        "description": (
            "Handhaving, crisisbeheersing en bescherming van publieke orde en "
            "veiligheid."
        ),
    },
    {
        "id": 13,
        "segment": "Fabricage",
        "description": (
            "Verwerking van materialen tot producten, inclusief onderhoud en "
            "procesbeheersing."
        ),
    },
    {
        "id": 14,
        "segment": "Marketing, sales en service",
        "description": (
            "Marketingactiviteiten, verkoop en dienstverlening om "
            "organisatorische doelen te bereiken."
        ),
    },
    {
        "id": 15,
        "segment": "Wetenschap, technologie, engineering en mathematica",
        "description": (
            "Onderzoek, experimenten en technische ontwikkeling in natuur- en "
            "technische wetenschappen."
        ),
    },
    {
        "id": 16,
        "segment": "Transport, distributie en logistiek",
        "description": (
            "Planning en uitvoering van vervoer en distributie van mensen en goederen."
        ),
    },
]

# Store IntVars to read and access them later.
career_cluster_vars = []  # Will be filled in create_career_clusters_frame()


def _create_total_score_callback(var_act, var_comp, var_edu, var_tot):
    """Internal helper: ensures that the total score is updated automatically."""
    def _update(*_):
        try:
            totaal = var_act.get() + var_comp.get() + var_edu.get()
        except tk.TclError:
            totaal = 0
        var_tot.set(totaal)

    return _update


def create_career_clusters_frame(parent):
    """
    Creates the form for Phase 2.1 – Career Clusters.

    For example, use the following in app.py:
    frame_fase21 = assessments.create_career_clusters_frame(main_container)
    """
    global career_cluster_vars
    career_cluster_vars = []

    frame = tk.Frame(parent, bg="#ffffff")

    title = tk.Label(
        frame,
        text="FASE 2.1 – Carrièreclusters",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff",
        fg="#000000",
    )
    title.pack(anchor="w", padx=20, pady=(15, 5))

    subtitle = tk.Label(
        frame,
        text=(
            "Scoor per cluster hoeveel de cliënt zich herkent in de activiteiten, "
            "competenties en educatieve onderwerpen. "
            "(0 = niet passend, hoger = meer passend)"
        ),
        font=("Segoe UI", 9),
        bg="#ffffff",
        fg="#333333",
        wraplength=900,
        justify="left",
    )
    subtitle.pack(anchor="w", padx=20, pady=(0, 10))

    table = tk.Frame(frame, bg="#ffffff")
    table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Column titles
    headers = [
        "Cluster",
        "Segment",
        "Score activiteiten\n(max. 7)",
        "Score competenties\n(max. 5)",
        "Score educatieve onderwerpen\n(max. 5)",
        "Totaalscore",
    ]

    for col, text in enumerate(headers):
        lbl = tk.Label(
            table,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg="#f3f4f6",
            fg="#111827",
            bd=1,
            relief="solid",
            padx=5,
            pady=5,
            justify="center",
        )
        lbl.grid(row=0, column=col, sticky="nsew")

    # Make sure all columns resize
    for col in range(len(headers)):
        table.grid_columnconfigure(col, weight=1)

    # Columns for the 16 clusters
    for r, cluster in enumerate(CAREER_CLUSTERS, start=1):
        # Label: cluster number
        lbl_id = tk.Label(
            table,
            text=str(cluster["id"]),
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#000000",
            bd=1,
            relief="solid",
            padx=5,
            pady=3,
        )
        lbl_id.grid(row=r, column=0, sticky="nsew")

        # Label: segment and brief description
        seg_text = f"{cluster['segment']}\n\n{cluster['description']}"
        lbl_seg = tk.Label(
            table,
            text=seg_text,
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#111827",
            bd=1,
            relief="solid",
            padx=5,
            pady=3,
            wraplength=350,
            justify="left",
        )
        lbl_seg.grid(row=r, column=1, sticky="nsew")

        # IntVars for scores
        var_act = tk.IntVar(value=0)
        var_comp = tk.IntVar(value=0)
        var_edu = tk.IntVar(value=0)
        var_tot = tk.IntVar(value=0)

        # Spinboxes for input
        spn_act = tk.Spinbox(
            table,
            from_=0,
            to=7,
            width=5,
            textvariable=var_act,
            font=("Segoe UI", 9),
            justify="center",
        )
        spn_act.grid(row=r, column=2, sticky="nsew")

        spn_comp = tk.Spinbox(
            table,
            from_=0,
            to=5,
            width=5,
            textvariable=var_comp,
            font=("Segoe UI", 9),
            justify="center",
        )
        spn_comp.grid(row=r, column=3, sticky="nsew")

        spn_edu = tk.Spinbox(
            table,
            from_=0,
            to=5,
            width=5,
            textvariable=var_edu,
            font=("Segoe UI", 9),
            justify="center",
        )
        spn_edu.grid(row=r, column=4, sticky="nsew")

        # Total score (read only)
        ent_tot = tk.Entry(
            table,
            textvariable=var_tot,
            font=("Segoe UI", 9, "bold"),
            justify="center",
            state="readonly",
        )
        ent_tot.grid(row=r, column=5, sticky="nsew")

        # Link callbacks so that the total score is recalculated each time
        cb = _create_total_score_callback(var_act, var_comp, var_edu, var_tot)
        var_act.trace_add("write", cb)
        var_comp.trace_add("write", cb)
        var_edu.trace_add("write", cb)

        # Save data
        career_cluster_vars.append(
            {
                "id": cluster["id"],
                "segment": cluster["segment"],
                "var_activities": var_act,
                "var_competences": var_comp,
                "var_educative": var_edu,
                "var_total": var_tot,
            }
        )

    return frame


def get_career_clusters_scores():
    """
    Returns the entered scores as a list of dicts.
    You can call this, for example, in your on_submit_career or a separate
    on_submit_phase21 function to write everything to Excel/JSON.
    """
    results = []
    for item in career_cluster_vars:
        results.append(
            {
                "cluster": item["id"],
                "segment": item["segment"],
                "score_activities": item["var_activities"].get(),
                "score_competences": item["var_competences"].get(),
                "score_educative_subjects": item["var_educative"].get(),
                "total_score": item["var_total"].get(),
            }
        )
    return results