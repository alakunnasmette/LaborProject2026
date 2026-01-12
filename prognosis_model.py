import tkinter as tk
from tkinter import ttk, scrolledtext   
from collections import defaultdict

# --- 1. DATA EN CONFIGUREN ---
# Mock data voor 45 vragen verdeeld over 3 blokken (15 vragen per blok)
PROGNOSE_MODEL_DATA = {
    "I. PERSOON (Personalia, Gezondheid, Profilering, Competentie)": [
        {"id": "Q1", "vraag": "Q1: Wat is de huidige fysieke gezondheidstoestand?", "opties": {"Uitstekend (0 beperkingen)": 0.25, "Goed (kleine beperkingen)": 0.50, "Matig (aanzienlijke beperkingen)": 0.75, "Slecht (zeer ernstig belemmerend)": 1.00}},
        {"id": "Q2", "vraag": "Q2: Hoe is de psychische stabiliteit en veerkracht?", "opties": {"Zeer stabiel": 0.25, "Enigszins wisselvallig": 0.50, "Regelmatig spanning/stress": 0.75, "Structurele psychische drempels": 1.00}},
        {"id": "Q3", "vraag": "Q3: Welk opleidingsniveau is behaald?", "opties": {"HBO/WO of hoger": 0.25, "MBO niveau 3/4": 0.50, "VMBO/MBO niveau 1/2": 0.75, "Geen diploma's behaald": 1.00}},
        {"id": "Q4", "vraag": "Q4: Hoe recent is de meest relevante werkervaring?", "opties": {"Afgelopen jaar": 0.25, "1 tot 3 jaar geleden": 0.50, "3 tot 5 jaar geleden": 0.75, "Langer dan 5 jaar geleden": 1.00}},
        {"id": "Q5", "vraag": "Q5: Hoe wordt de competentie 'Initiatief & Zelfstandigheid' ingeschat?", "opties": {"Zeer sterk": 0.25, "Voldoende": 0.50, "Verbeterpunt": 0.75, "Grote drempel": 1.00}},
        {"id": "Q6", "vraag": "Q6: In welke mate is er sprake van financiële zorgen?", "opties": {"Geen zorgen": 0.25, "Beheersbaar": 0.50, "Regelmatig stress": 0.75, "Ernstige schuldenproblematiek": 1.00}},
        {"id": "Q7", "vraag": "Q7: Hoe is de beheersing van de Nederlandse taal?", "opties": {"Vloeiend in woord en geschrift": 0.25, "Goed, kleine fouten": 0.50, "Matig, basiscommunicatie mogelijk": 0.75, "Onvoldoende voor werk": 1.00}},
        {"id": "Q8", "vraag": "Q8: Zijn er sociale/emotionele vaardigheden voldoende ontwikkeld?", "opties": {"Zeer goed": 0.25, "Voldoende": 0.50, "Verbeterpunt": 0.75, "Grote sociale belemmering": 1.00}},
        {"id": "Q9", "vraag": "Q9: Hoe flexibel is de kandidaat in het aannemen van taken?", "opties": {"Zeer flexibel": 0.25, "Redelijk flexibel": 0.50, "Vrij strikt (beperkte functies)": 0.75, "Zeer strikt (1 type functie)": 1.00}},
        {"id": "Q10", "vraag": "Q10: Hoe is de motivatie voor re-integratie?", "opties": {"Zeer hoog, intrinsiek": 0.25, "Hoog, extern gestuurd": 0.50, "Matig, twijfels aanwezig": 0.75, "Laag/geen, weerstand": 1.00}},
        {"id": "Q11", "vraag": "Q11: Is er een duidelijk, realistisch beroepsbeeld?", "opties": {"Zeer duidelijk en realistisch": 0.25, "Duidelijk, enigszins ambitieus": 0.50, "Vaag/onrealistisch": 0.75, "Geen duidelijk beroepsbeeld": 1.00}},
        {"id": "Q12", "vraag": "Q12: Hoe is de digitale geletterdheid?", "opties": {"Expert (office, software, internet)": 0.25, "Voldoende (basis office)": 0.50, "Beperkt (alleen basis internet)": 0.75, "Geen digitale vaardigheden": 1.00}},
        {"id": "Q13", "vraag": "Q13: Hoe is de zelfkennis over sterke/zwakke punten?", "opties": {"Zeer goed": 0.25, "Voldoende": 0.50, "Oppervlakkig": 0.75, "Vrijwel afwezig": 1.00}},
        {"id": "Q14", "vraag": "Q14: Zijn er belemmeringen rond kinderopvang/mantelzorg?", "opties": {"Niet van toepassing / opgelost": 0.25, "Regelmatige uitval, goed opvangbaar": 0.50, "Frequent uitval, lastig op te lossen": 0.75, "Structureel belemmerend": 1.00}},
        {"id": "Q15", "vraag": "Q15: Hoe scoort men op punctualiteit en afspraken nakomen?", "opties": {"Altijd stipt": 0.25, "Meestal stipt": 0.50, "Regelmatig te laat": 0.75, "Zeer onbetrouwbaar": 1.00}}
    ],
    "II. OMGEVING (Leefsituatie & Mobiliteit)": [
        {"id": "Q16", "vraag": "Q16: Hoe stabiel is de woonsituatie?", "opties": {"Zeer stabiel, eigen woning": 0.25, "Stabiel, huurwoning": 0.50, "Onzeker (tijdelijke huur)": 0.75, "Geen vaste woon- of verblijfplaats": 1.00}},
        {"id": "Q17", "vraag": "Q17: Is er een sociaal netwerk dat ondersteuning biedt?", "opties": {"Sterk en actief netwerk": 0.25, "Redelijk netwerk": 0.50, "Beperkt netwerk": 0.75, "Geen of problematisch netwerk": 1.00}},
        {"id": "Q18", "vraag": "Q18: Is er een rijbewijs (B) en eigen vervoer?", "opties": {"Ja, rijbewijs en auto": 0.25, "Ja, rijbewijs, geen auto": 0.50, "Nee, alleen OV mogelijk": 0.75, "Nee, mobiliteit is grote drempel": 1.00}},
        {"id": "Q19", "vraag": "Q19: Wat is de maximale aanvaardbare reistijd (enkele reis)?", "opties": {"Tot 60+ minuten": 0.25, "Tot 45 minuten": 0.50, "Tot 30 minuten": 0.75, "Minder dan 30 minuten (zeer beperkt)": 1.00}},
        {"id": "Q20", "vraag": "Q20: Hoe is de bereidheid tot verhuizen voor werk?", "opties": {"Zeer hoog, bereid tot verhuizen": 0.25, "Redelijk, binnen regio": 0.50, "Laag, alleen korte afstand": 0.75, "Geen bereidheid tot verhuizen": 1.00}},
        {"id": "Q21", "vraag": "Q21: Hoe is de directe relatie met de buren en buurt?", "opties": {"Zeer goed/rustig": 0.25, "Normaal": 0.50, "Regelmatig spanningen": 0.75, "Ernstige overlast/problematiek": 1.00}},
        {"id": "Q22", "vraag": "Q22: Is de buurt veilig en rustig?", "opties": {"Zeer veilig": 0.25, "Voldoende": 0.50, "Onveilig gevoel (overlast)": 0.75, "Structurele onveiligheid": 1.00}},
        {"id": "Q23", "vraag": "Q23: Is de woning geschikt voor thuiswerken/studeren (indien relevant)?", "opties": {"Ja, ruime en rustige werkplek": 0.25, "Ja, maar soms storend": 0.50, "Nee, geen geschikte plek": 0.75, "Niet relevant": 0.25}},
        {"id": "Q24", "vraag": "Q24: Hoe is de beschikbaarheid van openbaar vervoer?", "opties": {"Zeer goed, directe verbindingen": 0.25, "Redelijk, met overstap": 0.50, "Matig, lange wachttijden": 0.75, "Slecht, nauwelijks beschikbaar": 1.00}},
        {"id": "Q25", "vraag": "Q25: Hoe is de flexibiliteit in werktijden (ploegendienst/avondwerk)?", "opties": {"Zeer flexibel": 0.25, "Beperkt flexibel (bijv. geen nacht)": 0.50, "Alleen dagdiensten mogelijk": 0.75, "Zeer strikte beperkingen": 1.00}},
        {"id": "Q26", "vraag": "Q26: Hoe is de fysieke toegankelijkheid van de werkplek (indien relevant)?", "opties": {"Niet van toepassing / geen beperking": 0.25, "Kleine aanpassing nodig": 0.50, "Aanzienlijke aanpassing nodig": 0.75, "Vrijwel onmogelijk": 1.00}},
        {"id": "Q27", "vraag": "Q27: Is er steun van de partner/familie voor de re-integratie?", "opties": {"Zeer veel steun": 0.25, "Voldoende steun": 0.50, "Neutraal/weinig steun": 0.75, "Tegenzwerking/conflict": 1.00}},
        {"id": "Q28", "vraag": "Q28: Is er een actieve vrijetijdsbesteding (ontspanning)?", "opties": {"Ja, actief en gezond": 0.25, "Ja, maar matig": 0.50, "Nee, weinig tot geen": 0.75, "Overmatige, ongezonde bezigheden": 1.00}},
        {"id": "Q29", "vraag": "Q29: Worden afspraken en deadlines buiten werk om nagekomen?", "opties": {"Altijd stipt en correct": 0.25, "Meestal": 0.50, "Regelmatig uitstel of vergeetachtigheid": 0.75, "Vrijwel nooit": 1.00}},
        {"id": "Q30", "vraag": "Q30: Hoe is de algemene administratieve zelfredzaamheid?", "opties": {"Volledig zelfredzaam": 0.25, "Kan basisadministratie doen": 0.50, "Hulp nodig bij complexe zaken": 0.75, "Volledig afhankelijk van hulp": 1.00}}
    ],
    "III. ARBEIDSMARKT (Vraag, Aanbod, Zoekgedrag)": [
        {"id": "Q31", "vraag": "Q31: Hoe is de huidige beschikbaarheid op de arbeidsmarkt?", "opties": {"Fulltime (40u) beschikbaar": 0.25, "Parttime (24-32u) beschikbaar": 0.50, "Beperkt beschikbaar (16-24u)": 0.75, "Zeer beperkt beschikbaar (<16u)": 1.00}},
        {"id": "Q32", "vraag": "Q32: Is er een tekort aan personeel in de gewenste sector?", "opties": {"Groot tekort": 0.25, "Matig tekort": 0.50, "In balans (geen tekort)": 0.75, "Overschot aan aanbod": 1.00}},
        {"id": "Q33", "vraag": "Q33: Hoe realistisch zijn de salarisverwachtingen?", "opties": {"Zeer realistisch (marktconform)": 0.25, "Iets boven marktconform": 0.50, "Duidelijk te hoog (drempel)": 0.75, "Onrealistisch hoog": 1.00}},
        {"id": "Q34", "vraag": "Q34: Hoe intensief is de sollicitatie-activiteit?", "opties": {"Zeer actief (3+ per week)": 0.25, "Regelmatig (1-2 per week)": 0.50, "Sporadisch (1-2 per maand)": 0.75, "Vrijwel inactief": 1.00}},
        {"id": "Q35", "vraag": "Q35: Hoe is de kwaliteit van het CV en de sollicitatiebrief?", "opties": {"Uitstekend en up-to-date": 0.25, "Voldoende, kleine aanpassingen": 0.50, "Matig, grote revisie nodig": 0.75, "Zeer slecht/ontbreekt": 1.00}},
        {"id": "Q36", "vraag": "Q36: Is er bereidheid tot omscholing/bijscholing?", "opties": {"Zeer bereid": 0.25, "Redelijk bereid (korte cursussen)": 0.50, "Enigszins terughoudend": 0.75, "Niet bereid": 1.00}},
        {"id": "Q37", "vraag": "Q37: Hoe is de beheersing van netwerken en acquisitie?", "opties": {"Zeer sterk netwerker": 0.25, "Kan netwerken (met hulp)": 0.50, "Heeft moeite met netwerken": 0.75, "Geen netwerkvaardigheden": 1.00}},
        {"id": "Q38", "vraag": "Q38: Wat is de bereidheid tot tijdelijk of uitzendwerk?", "opties": {"Zeer bereid (flexibel)": 0.25, "Redelijk bereid (onder voorbehoud)": 0.50, "Liever direct vast contract": 0.75, "Alleen vast contract, geen tijdelijk werk": 1.00}},
        {"id": "Q39", "vraag": "Q39: Hoe is de kennis van de huidige arbeidsmarkttrends?", "opties": {"Zeer goed op de hoogte": 0.25, "Voldoende kennis": 0.50, "Beperkte kennis": 0.75, "Geen kennis": 1.00}},
        {"id": "Q40", "vraag": "Q40: Hoe is het contact met potentiële werkgevers ervaren?", "opties": {"Positief en constructief": 0.25, "Neutraal": 0.50, "Regelmatig afwijzingen (geen feedback)": 0.75, "Zeer negatief (geen interviews)": 1.00}},
        {"id": "Q41", "vraag": "Q41: Is het mogelijk om te starten met een proefperiode/stage?", "opties": {"Zeer bereid (onbetaald mogelijk)": 0.25, "Bereid (betaald stage)": 0.50, "Niet bereid": 0.75, "Structurele belemmering": 1.00}},
        {"id": "Q42", "vraag": "Q42: Hoe is de omgang met afwijzingen?", "opties": {"Veerkrachtig en leergierig": 0.25, "Accepteert afwijzing": 0.50, "Wordt gedemotiveerd": 0.75, "Blokkade na afwijzing": 1.00}},
        {"id": "Q43", "vraag": "Q43: Zijn er belemmeringen door VOG- of referentievereisten?", "opties": {"Geen belemmering": 0.25, "Kleine onzekerheid": 0.50, "Aanzienlijke onzekerheid": 0.75, "Structurele belemmering (geen VOG mogelijk)": 1.00}},
        {"id": "Q44", "vraag": "Q44: Hoe is de bereidheid tot werken onder het opleidingsniveau?", "opties": {"Zeer bereid": 0.25, "Redelijk bereid": 0.50, "Alleen op niveau gewenst": 0.75, "Weigert werk onder niveau": 1.00}},
        {"id": "Q45", "vraag": "Q45: Hoe is de beschikbaarheid van (actuele) referenties?", "opties": {"Uitstekend (3+)": 0.25, "Voldoende (1-2)": 0.50, "Matig (oud of twijfelachtig)": 0.75, "Geen referenties beschikbaar": 1.00}}
    ]
}

# --- 2. CONSTANTEN VOOR BEREKENING ---
# Bereken het totale scorebereik op basis van de PROGNOSE_MODEL_DATA
MAX_SCORE_COUNT = sum(len(questions) for questions in PROGNOSE_MODEL_DATA.values()) # 45
MIN_SCORE = MAX_SCORE_COUNT * 0.25 # 11.25
MAX_SCORE = MAX_SCORE_COUNT * 1.00 # 45.00
MAX_RANGE = MAX_SCORE - MIN_SCORE # 33.75

# --- 3. LOGICA FUNCTIES ---

def get_risk_level(total_score):
    """Berekent het risiconiveau en het percentage op basis van de totale gewogen score."""
    
    # Percentage berekening: (score - min_score) / max_range * 100
    risk_percentage = ((total_score - MIN_SCORE) / MAX_RANGE) * 100
    risk_percentage = max(0, min(100, risk_percentage)) # Clamp tussen 0 en 100
    
    # Bepaal het risiconiveau en de kleur (deze blijven kleur houden voor urgentie)
    if risk_percentage <= 20:
        level = "LAAG RISICO"
        description = "De re-integratiekansen zijn zeer gunstig. Dit profiel wijst op weinig belemmeringen en een snelle plaatsing is realistisch. Focus ligt op het matchen met de best passende functie."
        color = "#228B22"  # Forest Green
    elif risk_percentage <= 45:
        level = "GEMIDDELD RISICO"
        color = "#FFBF00"  # Amber / Goud
        description = "De kansen zijn goed, maar er zijn enkele factoren die de doorstroom vertragen. Gericht advies en versterking op deze specifieke drempels is nodig."
    elif risk_percentage <= 75:
        level = "HOOG RISICO"
        description = "Er zijn aanzienlijke structurele drempels aanwezig. Er is intensieve en gerichte begeleiding nodig, mogelijk in de vorm van scholing, training, of het wegnemen van primaire belemmeringen (zoals mobiliteit of gezondheid)."
        color = "#FFA500"  # Orange
    else:
        level = "ZEER HOOG RISICO"
        description = "Ernstige, structurele drempels. Een fundamentele ommezwaai of een drastisch omscholingstraject is vereist om de kansen op duurzame arbeid te vergroten."
        color = "#DC143C"  # Crimson Red
        
    return level, description, color, risk_percentage

def calculate_and_display(tk_vars, result_label, description_label, analysis_text):
    """Berekent de totale gewogen score, update de UI en genereert de analyse (placeholder)."""
    
    total_score = 0
    missing_count = 0

    # Kaart om de ID's te koppelen aan de volledige vraagteksten en opties
    question_map = {}
    for block_title, questions in PROGNOSE_MODEL_DATA.items():
        for q_data in questions:
            question_map[q_data["id"]] = q_data

    # Bereken de score en controleer op ontbrekende antwoorden
    for q_id, var in tk_vars.items():
        selected_option = var.get()
        if not selected_option:
            missing_count += 1
            continue
        
        try:
            # Zoek het gewicht op van de geselecteerde optie
            gewicht = question_map[q_id]["opties"][selected_option]
            total_score += gewicht
        except KeyError:
            print(f"Fout: Kan gewicht niet vinden voor {q_id} met optie {selected_option}")
            
    if missing_count > 0:
        result_label.config(text=f"Fout: {missing_count} vragen zijn nog niet beantwoord!", fg="#DC143C") # Crimson Red
        description_label.config(text="Vul alle vragen in om een complete prognose te berekenen.", fg="black")
        
        analysis_text.delete(1.0, tk.END)
        analysis_text.insert(tk.END, "Incomplete data. Vul alle vragen in om de gedetailleerde analyse te zien.")
        return

    # Toon de resultaten
    level, description, color, risk_percentage = get_risk_level(total_score)
    
    # De risico score zelf behoudt de kleur voor urgentie
    result_label.config(text=f"Totaal Risico: {risk_percentage:.1f}% ({level})", fg=color)
    description_label.config(text=description, fg="black")

    # Update de analyse-placeholder (de gedetailleerde analyse is inactief gemaakt zoals gevraagd)
    analysis_text.delete(1.0, tk.END)
    analysis_text.insert(tk.END, 
        f"De gedetailleerde Zelfreflectie & Analyse is inactief gemaakt zoals gevraagd.\n\n"
        f"Het risiconiveau is: {level} ({risk_percentage:.1f}%)\n"
        f"Totale gewogen score: {total_score:.2f} punten.")

# --- 4. TKINTER UI FUNCTIE ---

def build_prognose_page(root):
    """Bouwt de gebruikersinterface voor het Prognosemodel in zwart-wit met verbeterde scroll.
    
    Args:
        root (tk.Frame/tk.Tk): Het Tkinter-object (meestal een Frame) waarin de pagina wordt geladen.
    """
    
    # Configureer basisstijlen
    BG_COLOR = "white"
    FG_COLOR = "black"
    ACCENT_BG = "#f0f0f0" # Lichtgrijs voor blokken
    BUTTON_BG = "#333333" # Donkergrijs/Zwart voor knop
    BUTTON_FG = "white"
    
    # root.title("Prognosemodel Re-integratiekansen") <-- VERWIJDERD, dit veroorzaakt de AttributeError, want 'root' is hier een Frame, geen Tk-instantie.
    root.config(bg=BG_COLOR)
    
    # Clear bestaande widgets als de root een Frame is (wat we aannemen van app.py)
    for widget in root.winfo_children():
        widget.destroy()
    
    # Map om de geselecteerde waarden op te slaan
    tk_vars = {}
    
    # Hoofdframe met twee kolommen
    main_frame = tk.Frame(root, bg=BG_COLOR)
    # Gebruik pack met fill/expand om de volledige 'root' ruimte op te vullen (nodig als root een Frame is)
    main_frame.pack(padx=20, pady=20, fill='both', expand=True) 

    # Linker Frame: Vragenlijst
    left_frame = tk.Frame(main_frame, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    # --- VERBETERDE SCROLL FUNCTIE ---
    
    # 1. Scrollable Canvas
    canvas = tk.Canvas(left_frame, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    
    # 2. Scrollbar
    scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 3. Frame binnen de Canvas
    questionnaire_frame = tk.Frame(canvas, bg=BG_COLOR)
    
    # Creëer de 'window' in de canvas. Dit is het scrollbare gebied.
    canvas_window = canvas.create_window((0, 0), window=questionnaire_frame, anchor="nw")

    # Functie om de scrollregio bij te werken en de breedte aan te passen bij wijziging van het venster
    def _on_frame_configure(event):
        # Update de scrollregio van de canvas om de volledige framegrootte te omvatten
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Zorgt ervoor dat de canvas window breedte gelijk is aan het canvas/linkerframe breedte
        canvas.itemconfig(canvas_window, width=event.width)

    # Functie om te scrollen met het muiswiel
    def _on_mousewheel(event):
        # Controleert of het event het Windows/macOS delta of Linux-specifieke knopnummer is
        scroll_amount = 0
        if event.delta: # Windows/macOS
            # Gebruik event.delta (meestal 120 of -120) en normaliseer tot 'units'
            scroll_amount = -int(event.delta / 120)
        elif event.num == 5: # Linux (scroll down)
            scroll_amount = 1
        elif event.num == 4: # Linux (scroll up)
            scroll_amount = -1
            
        if scroll_amount != 0:
            canvas.yview_scroll(scroll_amount, "unit")

    # Bind events
    questionnaire_frame.bind("<Configure>", _on_frame_configure)
    # Bind muiswiel-scrollen aan de canvas en aan het frame BINNNEN de canvas voor betrouwbaarheid
    canvas.bind("<MouseWheel>", _on_mousewheel) 
    questionnaire_frame.bind("<MouseWheel>", _on_mousewheel)
    # Extra binds voor Linux/X11
    canvas.bind("<Button-4>", _on_mousewheel) 
    canvas.bind("<Button-5>", _on_mousewheel)
    questionnaire_frame.bind("<Button-4>", _on_mousewheel) 
    questionnaire_frame.bind("<Button-5>", _on_mousewheel)
    
    # --- EINDE VERBETERDE SCROLL FUNCTIE ---
    
    # Rechter Frame: Resultaten en Analyse
    right_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10, pady=10)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    # Zet gewichten voor kolommen om de linkerzijde meer ruimte te geven
    main_frame.grid_columnconfigure(0, weight=4) # Vragenlijst krijgt 4x zoveel ruimte
    main_frame.grid_columnconfigure(1, weight=1) # Resultaten krijgt 1x zoveel ruimte

    # --- Titel ---
    tk.Label(questionnaire_frame, text="Prognosemodel Re-integratiekansen (45 Vragen)", 
             font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR, pady=10).pack(fill='x')

    # --- Vragenlijst Sectie ---
    for block_title, questions in PROGNOSE_MODEL_DATA.items():
        # Blok Titel
        block_label = tk.Label(questionnaire_frame, text=block_title, 
                               font=("Helvetica", 12, "bold"), bg=ACCENT_BG, fg=FG_COLOR, 
                               anchor='w', padx=5, pady=5)
        block_label.pack(fill='x', pady=(10, 5))
        
        # Voeg vragen toe
        for q_data in questions:
            q_id = q_data["id"]
            question_text = q_data["vraag"]
            options = q_data["opties"]
            
            # Frame voor de individuele vraag
            q_frame = tk.Frame(questionnaire_frame, bg=BG_COLOR, padx=10, pady=5, bd=1, relief=tk.RIDGE)
            q_frame.pack(fill='x', pady=2)
            
            # Vraagtekst
            # Wraplength is belangrijk om ervoor te zorgen dat lange vragen goed omspringen.
            tk.Label(q_frame, text=question_text, font=("Helvetica", 10, "bold"), bg=BG_COLOR, fg=FG_COLOR, anchor='w', wraplength=450).pack(fill='x', pady=(0, 5))
            
            # StringVar om de geselecteerde optie op te slaan
            var = tk.StringVar(q_frame)
            tk_vars[q_id] = var
            
            # Radiobuttons voor opties
            for option_text, weight in options.items():
                display_text = f"{option_text} ({weight:.2f})"
                rb = tk.Radiobutton(q_frame, text=display_text, variable=var, value=option_text, 
                                    bg=BG_COLOR, fg=FG_COLOR, activebackground=ACCENT_BG, 
                                    selectcolor=ACCENT_BG, anchor='w')
                rb.pack(fill='x', padx=10)

    # --- Resultaat Sectie ---
    
    # 1. Bereken Knop
    calculate_button = tk.Button(right_frame, text="Bereken Risicoscore", 
                                 command=lambda: calculate_and_display(tk_vars, result_label, description_label, analysis_text),
                                 bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 12, "bold"), 
                                 activebackground=FG_COLOR, activeforeground=BUTTON_BG,
                                 width=30)
    calculate_button.pack(fill='x', pady=(0, 20))

    # 2. Resultaat Label
    result_title = tk.Label(right_frame, text="Totaal Risicopercentage", font=("Helvetica", 10), bg=ACCENT_BG, fg=FG_COLOR, anchor='w', padx=5, pady=2)
    result_title.pack(fill='x')
    
    result_label = tk.Label(right_frame, text="-", font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR, pady=5, anchor='w')
    result_label.pack(fill='x', pady=(0, 10))

    # 3. Beschrijving Label
    desc_title = tk.Label(right_frame, text="Classificatie & Advies", font=("Helvetica", 10), bg=ACCENT_BG, fg=FG_COLOR, anchor='w', padx=5, pady=2)
    desc_title.pack(fill='x')
    
    description_label = tk.Label(right_frame, text="Beantwoord alle 45 vragen om de prognose te berekenen.", font=("Helvetica", 10, "italic"), bg=BG_COLOR, fg=FG_COLOR, justify=tk.LEFT, wraplength=300, anchor='nw')
    description_label.pack(fill='x', pady=(0, 10))

    # 4. Analyse Tekst (Placeholder)
    analysis_title = tk.Label(right_frame, text="Zelfreflectie & Analyse (Inactief)", font=("Helvetica", 12, "bold"), bg=BG_COLOR, fg=FG_COLOR, anchor='w', pady=10)
    analysis_title.pack(fill='x')
    
    analysis_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=15, font=("Helvetica", 10), bd=1, relief=tk.SUNKEN)
    analysis_text.insert(tk.END, "Incomplete data. Vul alle vragen in om de gedetailleerde analyse te zien.")
    analysis_text.config(state=tk.NORMAL) # Maak schrijfbaar voor de berekeningsfunctie
    analysis_text.pack(fill='both', expand=True)

if __name__ == '__main__':
    # Dit deel is alleen voor standalone testen en roept de Tkinter root aan
    root = tk.Tk()
    root.title("Prognosemodel Re-integratiekansen") 
    build_prognose_page(root)
    root.mainloop()