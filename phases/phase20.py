import tkinter as tk
from tkinter import messagebox
from ui.ui_components import clear_frame
from utils.write_assessments_to_excel import add_career_anchors_to_excel
# Try to import Phase 2.1 helpers; if the module exists use its API,
# otherwise keep safe None values and show friendly messages at runtime.
try:
    import phases.phase21 as phase21
    # phase21 may expose the builder under different names; try common variants
    phase21_build = (
        getattr(phase21, "build_carriereclusters_page", None)
        or getattr(phase21, "build_loopbaanankers_page", None)
        or getattr(phase21, "create_career_clusters_frame", None)
    )
    phase21_on_next = getattr(phase21, "on_next_page", None)
except Exception:
    phase21 = None
    phase21_build = None
    phase21_on_next = None

# ----------------------------- Phase 2.0 - Career anchors -----------------------------

# Table colors
DARK_GREY = "#4d4d4d"
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


def build_career_anchors_page(parent_frame: tk.Frame, navigate=None) -> None:
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

        # Save to Excel file if it exists
        if hasattr(parent_frame, 'excel_file_path') and parent_frame.excel_file_path:
            success = add_career_anchors_to_excel(parent_frame.excel_file_path, parent_frame.career_results)
            if success:
                messagebox.showinfo("Succes", "Loopbaanankers opgeslagen naar Excel-bestand.")
            else:
                messagebox.showwarning("Waarschuwing", "Loopbaanankers konden niet naar Excel-bestand worden geschreven.")

        # Empty right panel
        clear_frame(parent_frame)

        # Load Phase 2.1 Career Clusters in the same panel (if available)
        build_fn = phase21_build if 'phase21' in globals() else None

        if build_fn:
            try:
                frame_21 = build_fn(parent_frame, navigate)
            except TypeError:
                # Some builders don't accept navigate; call with single arg
                try:
                    frame_21 = build_fn(parent_frame)
                except Exception:
                    frame_21 = tk.Frame(parent_frame, bg="white")
                    tk.Label(frame_21, text="Fase 2.1 kon niet worden geladen.", bg="white", fg="black").pack(padx=20, pady=20)
            except Exception:
                frame_21 = tk.Frame(parent_frame, bg="white")
                tk.Label(frame_21, text="Fase 2.1 kon niet worden geladen.", bg="white", fg="black").pack(padx=20, pady=20)
        else:
            frame_21 = tk.Frame(parent_frame, bg="white")
            tk.Label(frame_21, text="Fase 2.1 is nog niet geïmplementeerd.", bg="white", fg="black").pack(padx=20, pady=20)

        frame_21.pack(fill="both", expand=True)

    btn_frame = tk.Frame(scroll_frame, bg="white")
    btn_frame.pack(fill="x", pady=(5, 20))

    def _handle_skip():
        # Prefer the passed navigate callback
        if navigate:
            try:
                navigate("phase2.1")
                return
            except Exception:
                pass

        # Next prefer phase21-specific helper
        if 'phase21' in globals() and phase21_on_next:
            try:
                phase21_on_next()
                return
            except Exception:
                pass

        messagebox.showinfo("Niet beschikbaar", "Fase 2.1 is nog niet beschikbaar.")

    btn_skip = tk.Button(
        btn_frame,
        text="Overslaan",
        bg="#b3b3b3",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=5,
        command=_handle_skip,
    )
    btn_skip.pack(side="left", padx=30)

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