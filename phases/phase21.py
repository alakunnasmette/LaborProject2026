# corporate_culture_research.py
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
from collections import defaultdict

# ---------- Data ----------
@dataclass(frozen=True)
class Group:
    id: int
    name: str
    desc: str
    stmts: list[str]

GROUPS = [
    Group(1, "Landbouw, voeding en natuurlijke grondstoffen / Agriculture, food and natural resources",
          "Typerend voor familiebedrijven, landbouw, horeca, zorg e.d.",
          [
              "Er bestaan gemeenschappelijke waarden en doelstellingen.",
              "Onderlinge samenhang (wij-gevoel). Teamwork, het beste uit elkaar halen.",
              "Klanten worden als partners beschouwd.",
              "Regels en procedures zijn ondergeschikt aan het gevoel een team te zijn.",
          ]),
    Group(2, "Innovatieve cultuur",
          "Typerend voor softwarebedrijven, luchtvaart, ruimtevaart e.d.",
          [
              "Snel reageren op snel veranderende omstandigheden.",
              "Innovatie en vernieuwing (nieuwe diensten/producten).",
              "Creatief en flexibel zijn wordt gestimuleerd.",
              "De organisatie is flexibel en kan snel een nieuwe vorm aannemen.",
          ]),
    Group(3, "Beheersgerichte cultuur",
          "Typerend voor overheids- of onderwijsinstellingen.",
          [
              "Procedures en regels staan centraal.",
              "Leidinggevenden coördineren en organiseren.",
              "Stabiliteit, efficiëntie en voorspelbaarheid zijn belangrijk.",
              "Trage besluitvormingsprocessen.",
          ]),
    Group(4, "Resultaatgerichte cultuur",
          "Richting externe transacties; concurreren met gelijkaardige organisaties.",
          [
              "Productiviteit, resultaten, winst en taakgerichtheid.",
              "Externe positionering om concurrentie te versterken.",
              "Duidelijk doel en (soms) agressieve strategie.",
              "Leidinggevenden veeleisend; nadruk op marktleider zijn.",
          ]),
]



# Styles 
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
}

# ---------- Helpers ----------
def clear_frame(frame: tk.Widget) -> None:
    for w in frame.winfo_children():
        w.destroy()

def scrollable(parent: tk.Widget) -> tuple[tk.Frame, tk.Canvas, tk.Frame]:
    wrap = tk.Frame(parent, bg=S["bg"])
    wrap.pack(fill="both", expand=True)

    c = tk.Canvas(wrap, bg=S["bg"], highlightthickness=0)
    sb = tk.Scrollbar(wrap, orient="vertical", command=c.yview)
    c.configure(yscrollcommand=sb.set)
    c.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    inner = tk.Frame(c, bg=S["bg"])
    win = c.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda _e: c.configure(scrollregion=c.bbox("all")))
    c.bind("<Configure>", lambda e: c.itemconfig(win, width=e.width))
    c.bind_all("<MouseWheel>", lambda e: c.yview_scroll(-int(e.delta / 120), "units"))

    return wrap, c, inner

def make_likert_buttons(parent: tk.Widget, var: tk.StringVar, bg: str) -> tk.Frame:
    f = tk.Frame(parent, bg=bg)
    buttons = {}

    def refresh():
        cur = var.get()
        for v, b in buttons.items():
            if v == cur:
                b.config(relief="sunken", bg=S["btn_on"], fg="white")
            else:
                b.config(relief="raised", bg=S["btn"], fg="black")

    def choose(v: str):
        var.set(v)
        refresh()



# ---------- Page ----------
class Culture22Page(tk.Frame):
    def __init__(self, parent: tk.Widget, navigate):
        super().__init__(parent, bg=S["bg"])
        self.navigate = navigate
        self.vars: dict[tuple[int, int], tuple[tk.IntVar, tk.IntVar, tk.IntVar]] = {}
        self.sub_lbl: dict[int, tk.Label] = {}
        self.build()

    def subtotal(self, gid: int) -> int:
        tot = 0
        # Iterate over all (gid, idx) in self.vars for this gid
        for (cluster_id, idx), triple in self.vars.items():
            if cluster_id != gid:
                continue
            main_var, skill_var, interest_var = triple
            try:
                tot += int(main_var.get())
            except Exception:
                pass
            try:
                tot += int(skill_var.get())
            except Exception:
                pass
            try:
                tot += int(interest_var.get())
            except Exception:
                pass
        return tot

    def update_subtotal(self, gid: int):
        self.sub_lbl[gid].config(text=str(self.subtotal(gid)))

    def build(self):
        _, _, inner = scrollable(self)


        tk.Label(inner, text="Fase 2.1 – Carrierrèclusters",
                 bg=S["bg"], font=S["f_title"], anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        tk.Label(inner, text="Lees de stellingen uit het Excel-bestand en geef aan met een vinkje als je vaardigheid of interesse hebt.",
                 bg=S["bg"], font=S["f_sub"], anchor="w").pack(fill="x", padx=20, pady=(0, 12))

        outer = tk.Frame(inner, bg=S["bg"])
        outer.pack(fill="both", expand=True, padx=20)

        left = tk.Frame(outer, bg=S["bg"])
        right = tk.Frame(outer, bg=S["bg"])
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="y", padx=(15, 0))

        # header
        h = tk.Frame(left, bg=S["dark"])
        h.pack(fill="x")
        tk.Label(h, text="Cluster", bg=S["dark"], fg="white", font=S["f_b"], width=8, anchor="w", padx=10)\
            .grid(row=0, column=0, sticky="w")
        tk.Label(h, text="Activiteiten die beschrijven wat de cliënt leuk vind om te doen", bg=S["dark"], fg="white", font=S["f_b"], anchor="center", padx=10)\
            .grid(row=0, column=2, sticky="w")
        tk.Label(h, text="Competenties", bg=S["dark"], fg="white", font=S["f_b"], anchor="center", padx=10)\
            .grid(row=0, column=3, sticky="w")
        tk.Label(h, text="Educatieve onderwerpen", bg=S["dark"], fg="white", font=S["f_b"], anchor="center", padx=10)\
            .grid(row=0, column=4, sticky="w")

        body = tk.Frame(left, bg=S["bg"])
        body.pack(fill="both", expand=True)

        # Hardcoded questions for each cluster
        # Example structure: {cluster_id: [ {main_statement, skill_statement, interest_statement}, ... ] }
        # Fill in your questions for each cluster below:
        CLUSTER_QUESTIONS = {
            1: [
                {
                    "main_statement": "Leren hoe flora en fauna groeit en in leven blijft",
                    "skill_statement": "Zelfredzaam",
                    "interest_statement": "Wiskunde"
                },
                {
                    "main_statement": "Het zo optimaal mogelijk gebruik maken van de grondstoffen van de aarde",
                    "skill_statement": "Natuurliefhebber",
                    "interest_statement": "Beheer van natuurlijke grondstoffen"
                },
                {
                    "main_statement": "Jagen en/of vissen",
                    "skill_statement": "Fysiek actief",
                    "interest_statement": "Aardrijkskunde"
                },
                {
                    "main_statement": "Het beschermen van het milieu",
                    "skill_statement": "Planner",
                    "interest_statement": "Scheikunde"
                },
                {
                    "main_statement": "Buiten zijn in allerlei weersomstandigheden",
                    "skill_statement": "Creatieve probleemoplosser",
                    "interest_statement": "Landbouw"
                },
                {
                    "main_statement": "Plannen,budgetteren en registraties bijhouden",
                },
                {
                    "main_statement": "Het bedienen van machines en deze in goede conditie houden",   
                },
            ],
            2: [
                {
                    "main_statement": "Het lezen en volgen van blauwdrukken en/of instructies",
                    "skill_statement": "Nieuwsgierig",
                    "interest_statement": "Calculeren"
                },
                {
                    "main_statement": "Inbeelden hoe een afgewerkt producteruit zal zien",
                    "skill_statement": "Het verstrekken van duidelijke instructies",
                    "interest_statement": "Technisch tekenen"
                },
                {
                    "main_statement": "Werken met de handen",
                    "skill_statement": "Aandacht besteden aan details",
                    "interest_statement": "Exacte wetenschappen"
                },
                {
                    "main_statement": "Het uitvoeren van werkzaamheden die nauwkeurige resultaten vereisen",
                    "skill_statement": "Goed in het visualiseren van mogelijkheden",
                    "interest_statement": "Architectuur"
                },
                {
                    "main_statement": "Het oplossen van technische problemen",
                    "skill_statement": "Geduldig en persistent",
                    "interest_statement": "elektrische warmtebronnen, airconditioning en koeltechniek"
                },
                {
                    "main_statement": "Het bezoeken en onderzoeken van mooie, historische en/of interessante gebouwen",
                },
                {
                    "main_statement": "Het opvolgen van logische en stapsgewijze procedures",   
                },
            ],
            3: [
                {
                    "main_statement": "Het gebruik van verbeeldingskracht om informatie naar anderen te communiceren",
                    "skill_statement": "Creatief en fantasierijk",
                    "interest_statement": "Kunst en grafisch ontwerp"
                },
                {
                    "main_statement": "Klaar staan voor anderen",
                    "skill_statement": "Goede communicator",
                    "interest_statement": "Muziek"
                },
                {
                    "main_statement": "Lezen en schrijven",
                    "skill_statement": "Benieuwd naar nieuwe technologie",
                    "interest_statement": "Spraak en drama"
                },
                {
                    "main_statement": "Het bespelen van een muziekinstrument",
                    "skill_statement": "Symphatisch en empathisch",
                    "interest_statement": "Journalistiek en literatuur"
                },
                {
                    "main_statement": "Het uitvoeren van creatieve en/of artistieke activiteiten",
                    "skill_statement": "Bepalend en vasthoudend",
                    "interest_statement": "Audiovisuele technologie"
                },
                {
                    "main_statement": "Het gebruik van video- en opnametechnologie",
                },
                {
                    "main_statement": "Het ontwerpen van posters en brochures",   
                },
            ],
            4: [
                {
                    "main_statement": "Het uitvoeren van routine en/of georganiseerde activiteiten maar ook flexibel kunnen zijn",
                    "skill_statement": "Georganiseerd",
                    "interest_statement": "ICT"
                },
                {
                    "main_statement": "Werken met getallen en gedetailleerde informatie",
                    "skill_statement": "Praktisch en logisch",
                    "interest_statement": "Boekhouding"
                },
                {
                    "main_statement": "Een leider zijn in een groep",
                    "skill_statement": "Geduldig",
                    "interest_statement": "Kostprijs berekeningen"
                },
                {
                    "main_statement": "Zakelijk contact maken met mensen",
                    "skill_statement": "Tactvol",
                    "interest_statement": "Engels"
                },
                {
                    "main_statement": "Werken met computerprogramma's",
                    "skill_statement": "Verantwoordelijk",
                    "interest_statement": "Economie"
                },
                {
                    "main_statement": "Het maken van rapporten en het communiceren van ideeën",
                },
                {
                    "main_statement": "Het plannen van werk en het volgen van instructies",   
                },
            ],
            5: [
                {
                    "main_statement": "Communiceren met verschillende soorten mensen",
                    "skill_statement": "Vriendelijk",
                    "interest_statement": "Taalvaardigheid"
                },
                {
                    "main_statement": "Anderen helpen met hun huiswerk of met het leren beheersen van nieuwe onderwerpen",
                    "skill_statement": "Beslisser",
                    "interest_statement": "Sociale studies"
                },
                {
                    "main_statement": "Naar school gaan",
                    "skill_statement": "Nuttig",
                    "interest_statement": "Pedagogiek"
                },
                {
                    "main_statement": "Het leiden en plannen van activiteiten voor anderen",
                    "skill_statement": "Innovatief en nieuwsgierig",
                    "interest_statement": "Wetenschap"
                },
                {
                    "main_statement": "Het uitdragen van meerdere verantwoordelijkheden tegelijk",
                    "skill_statement": "Goede luisteraar",
                    "interest_statement": "Psychologie"
                },
                {
                    "main_statement": "Het verkrijgen van nieuwe informatie",
                },
                {
                    "main_statement": "Mensen helpen om hun uitdagingen te overwinnen",   
                },
            ],
            6: [
                {
                    "main_statement": "Werken met cijfers",
                    "skill_statement": "Betrouwbaar",
                    "interest_statement": "Belastingen"
                },
                {
                    "main_statement": "Werken om een deadline te halen",
                    "skill_statement": "Orderlijk",
                    "interest_statement": "Wiskunde"
                },
                {
                    "main_statement": "Het maken van voorspellingen op basis van bestaande feiten",
                    "skill_statement": "Zelfverzekerd",
                    "interest_statement": "Economie"
                },
                {
                    "main_statement": "Zorgen voor een kader van regels en procedures",
                    "skill_statement": "Logisch",
                    "interest_statement": "Financiële administratie"
                },
                {
                    "main_statement": "Het analyseren en interpreteren van financiële informatie voor anderen",
                    "skill_statement": "Methodisch en efficiënt",
                    "interest_statement": "Ondernemersrecht"
                },
                {
                    "main_statement": "Het met nauwkeurigheid en betrouwbaarheid behandelen van financiën",
                },
                {
                    "main_statement": "Trots zijn op de manier waarop je je kleedt en presenteert",
                },
            ],
            7: [
                {
                    "main_statement": "Betrokken zijn in de politiek",
                    "skill_statement": "Goede communicator",
                    "interest_statement": "Politiek"
                },
                {
                    "main_statement": "Het onderhandelen, verdedigen en/of bespreken van ideeën en onderwerpen",
                    "skill_statement": "Concurrerend",
                    "interest_statement": "Taalvaardigheid"
                },
                {
                    "main_statement": "Het plannen van activiteiten en samenwerken met anderen",
                    "skill_statement": "Service georiënteerd",
                    "interest_statement": "Nederlandse geschiedenis"
                },
                {
                    "main_statement": "Werken met details",
                    "skill_statement": "Goed georganiseerd",
                    "interest_statement": "Calculeren"
                },
                {
                    "main_statement": "Het uitvoeren van taken die vaak kunnen veranderen",
                    "skill_statement": "Probleem oplosser",
                    "interest_statement": "Vreemde talen"
                },
                {
                    "main_statement": "Het analyseren en interpreteren van informatie voor anderen",
                },
                {
                    "main_statement": "Reizen en nieuwe dingen ontdekken",   
                },
            ],
            8: [
                {
                    "main_statement": "Werken onder druk",
                    "skill_statement": "Emphatisch en zorgzaam",
                    "interest_statement": "Biologische wetenschappen"
                },
                {
                    "main_statement": "Het helpen van zieke mensen en/of dieren",
                    "skill_statement": "Het verstrekken van duidelijke informatie",
                    "interest_statement": "Chemie"
                },
                {
                    "main_statement": "Beslissingen nemen op basis van logica en informatie",
                    "skill_statement": "Zorgvuldig en voorzichtig",
                    "interest_statement": "Biometrie"
                },
                {
                    "main_statement": "Deelnemen aan gezondheid- en wetenschapslessen",
                    "skill_statement": "Geduldig",
                    "interest_statement": "Gezondheid op werk"
                },
                {
                    "main_statement": "Snel reageren en rustig blijven in noodsituaties",
                    "skill_statement": "Goede luisteraar",
                    "interest_statement": "Spelling en grammatica"
                },
                {
                    "main_statement": "Werken als lid van een team",
                },
                {
                    "main_statement": "Het nauwkeurig volgen van richtlijnen en het voldoen aan strikte normen voor nauwkeurigheid",   
                },
            ],
            9: [
                {
                    "main_statement": "Onderzoek doen naar nieuwe plaatsen en activiteiten",
                    "skill_statement": "Tactvol",
                    "interest_statement": "Nederlands"
                },
                {
                    "main_statement": "Werken met alle leeftijden en alle soorten mensen",
                    "skill_statement": "Zelfgemotiveerd",
                    "interest_statement": "Vreemde talen"
                },
                {
                    "main_statement": "Het organiseren van activiteiten waarbij andere mensen zich amuseren",
                    "skill_statement": "Samenwerkend",
                    "interest_statement": "Sociale wetenschappen"
                },
                {
                    "main_statement": "Het hanteren van een flexibel schema",
                    "skill_statement": "Ondernemend",
                    "interest_statement": "Marketing"
                },
                {
                    "main_statement": "Mensen helpen om besluiten te nemen",
                    "skill_statement": "Tolerant",
                    "interest_statement": "Voedsel"
                },
                {
                    "main_statement": "Eenvoudig, tactvol en hoffelijk communiceren",
                },
                {
                    "main_statement": "Informatie verzamelen over verschillende culturen",   
                },
            ],
            10: [
                {
                    "main_statement": "Zorgen voor mensen, hun behoeften en problemen",
                    "skill_statement": "Goede communicator",
                    "interest_statement": "Taalvaardigheid"
                },
                {
                    "main_statement": "Deelnemen aan gemeenschapsdiensten en/of vrijwilligerswerk",
                    "skill_statement": "Zorgzaam",
                    "interest_statement": "Psychologie en sociologie"
                },
                {
                    "main_statement": "Luisteren naar de perspectieven van anderen",
                    "skill_statement": "Non-materialistisch",
                    "interest_statement": "Familie- en consumentenwetenschap"
                },
                {
                    "main_statement": "Mensen helpen op hun best te zijn",
                    "skill_statement": "Gebruik van intuïtie en logica",
                    "interest_statement": "Financiën"
                },
                {
                    "main_statement": "Werken met mensen van jong en oud",
                    "skill_statement": "Niet-oordelend",
                    "interest_statement": "Vreemde talen"
                },
                {
                    "main_statement": "Denken aan nieuwe manieren om dingen te doen",
                },
                {
                    "main_statement": "Vrienden maken met verschillende soorten mensen",   
                },
            ],
            11: [
                {
                    "main_statement": "Werken met computers",
                    "skill_statement": "Logische en analytische denker",
                    "interest_statement": "Wiskunde"
                },
                {
                    "main_statement": "Logisch redeneren om complexe problemen op te lossen",
                    "skill_statement": "Helicopter view",
                    "interest_statement": "Wetenschap"
                },
                {
                    "main_statement": "Het gebruiken van machines, technieken en processen",
                    "skill_statement": "Peristent",
                    "interest_statement": "Computertechnologie"
                },
                {
                    "main_statement": "Het lezen van technische handleidingen en diagrammen en het oplossen van technische problemen",
                    "skill_statement": "Goede concentratievaardigheden",
                    "interest_statement": "Communicatievaardigheden"
                },
                {
                    "main_statement": "Aanpassen aan veranderingen",
                    "skill_statement": "Nauwkeurig",
                    "interest_statement": "Grafisch ontwerp"
                },
                {
                    "main_statement": "Het spelen van videogames en uitzoeken hoe deze werken",
                },
                {
                    "main_statement": "Gedurende lange perioden concentreren zonder te zijn afgeleid",   
                },
            ],
            12: [
                {
                    "main_statement": "Werken onder druk of in de aanwezigheid van gevaar",
                    "skill_statement": "Avontuurlijk",
                    "interest_statement": "Taalvaardigheid"
                },
                {
                    "main_statement": "Beslissingen maken op basis van observaties",
                    "skill_statement": "Betrouwbaar",
                    "interest_statement": "Psychologie en sociologie"
                },
                {
                    "main_statement": "Communiceren met anderer mensen",
                    "skill_statement": "Gemeenschapsgericht",
                    "interest_statement": "Overheid en geschiedenis"
                },
                {
                    "main_statement": "Een positie van authoriteit hebben",
                    "skill_statement": "Doorslaggevend",
                    "interest_statement": "Rechshandhaving"
                },
                {
                    "main_statement": "Het respecteren van regels en voorschriften",
                    "skill_statement": "Optimistisch",
                    "interest_statement": "EHBO"
                },
                {
                    "main_statement": "Debbateren en het winnen van argumenten",
                },
                {
                    "main_statement": "Het oberserveren en analyseren van het gedrag van mensen",   
                },
            ],
            13: [
                {
                    "main_statement": "Werken met de handen en op de manier leren",
                    "skill_statement": "Praktisch",
                    "interest_statement": "Wiskunde en geometrie"
                },
                {
                    "main_statement": "Concepten samenvoegen",
                    "skill_statement": "Observerend",
                    "interest_statement": "Chemie"
                },
                {
                    "main_statement": "Het uitvoeren van routinematig, georganiseerd en nauwkeurig werk",
                    "skill_statement": "Fysiek actief",
                    "interest_statement": "Handel en industrie"
                },
                {
                    "main_statement": "Het uitvoeren van activiteiten die tastbare producten opleveren",
                    "skill_statement": "Stapsgewijze denker",
                    "interest_statement": "Natuurkunde"
                },
                {
                    "main_statement": "Wiskunde toepassen om oplossingen uit te werken",
                    "skill_statement": "Gecoördineerd",
                    "interest_statement": "Taalvaardigheid"
                },
                {
                    "main_statement": "Het gebruiken van hand- en elektrisch gereedschap, werkuitrusting en machines",
                },
                {
                    "main_statement": "Het visualiseren van objecten in drie dimensies vanuit een vlakke tekening",   
                },
            ],
            14: [
                {
                    "main_statement": "Winkelen en naar het winkelcentrum gaan",
                    "skill_statement": "Enthousiast",
                    "interest_statement": "Taalvaardigheid"
                },
                {
                    "main_statement": "De baas zijn",
                    "skill_statement": "Concurrerend",
                    "interest_statement": "Marketing"
                },
                {
                    "main_statement": "Het maken van reclameschermen en het promoten van ideeën",
                    "skill_statement": "Creatief",
                    "interest_statement": "Bedrijfseconomie"
                },
                {
                    "main_statement": "Het geven van presentaties en het toespreken van publiek",
                    "skill_statement": "Zelfgemotiveerd",
                    "interest_statement": "Order to cash"
                },
                {
                    "main_statement": "Mensen overtuigen om producten te kopen of om deel te nemen aan promotie activiteiten",
                    "skill_statement": "Overtuigend",
                    "interest_statement": "Communicatietechnologie"
                },
                {
                    "main_statement": "Het communiceren van ideeën naar andere mensen",
                },
                {
                    "main_statement": "Het gebruik maken van de mogelijkheden om extra geld te verdienen",   
                },
            ],
            15: [
                {
                    "main_statement": "Formules interpreteren",
                    "skill_statement": "Detailgericht",
                    "interest_statement": "Wiskunde"
                },
                {
                    "main_statement": "Zoeken naar antwoorden op vragen",
                    "skill_statement": "Nieuwsgierig",
                    "interest_statement": "Wetenschap"
                },
                {
                    "main_statement": "Werken in een laboratorium",
                    "skill_statement": "Doelgericht",
                    "interest_statement": "Computer aided drawing"
                },
                {
                    "main_statement": "Uitzoeken hoe zaken werken en het onderzoeken van nieuwe zaken",
                    "skill_statement": "Methodisch",
                    "interest_statement": "Elektronica en computernetwerken"
                },
                {
                    "main_statement": "Het ontdekken van nieuwe technologie",
                    "skill_statement": "Statisch",
                    "interest_statement": "Technologie"
                },
                {
                    "main_statement": "Experimenteren om de beste manier te vinden om dingen te doen",
                },
                {
                    "main_statement": "Het besteden van aandacht aan details en nauwkeurig werken",   
                },
            ],
            16: [
                {
                    "main_statement": "Reizen",
                    "skill_statement": "Ondernemend",
                    "interest_statement": "Logistiek en distributie"
                },
                {
                    "main_statement": "Goed zien en het bezitten van snelle reflexen",
                    "skill_statement": "Mechanisch",
                    "interest_statement": "Handel en industrie"
                },
                {
                    "main_statement": "Het oplossen van mechanische problemen",
                    "skill_statement": "Gecoördineerd",
                    "interest_statement": "Exacte wetenschappen"
                },
                {
                    "main_statement": "Het ontwerpen van efficiënte processen",
                    "skill_statement": "Observerend",
                    "interest_statement": "Economie"
                },
                {
                    "main_statement": "Het anticiperen op behoeften en het voorbereiden van ontmoetingen",
                    "skill_statement": "Planner",
                    "interest_statement": "Vreemde talen"
                },
                {
                    "main_statement": "Auto rijden",
                },
                {
                    "main_statement": "Het verplaatsen van dingen van de ene lokatie naar de andere lokatie",   
                },
            ],
    }

        rows_by_cluster = defaultdict(list)
        for cluster_id, questions in CLUSTER_QUESTIONS.items():
            for idx, q in enumerate(questions, start=1):
                rows_by_cluster[cluster_id].append((idx, q))

        for cluster_id, rows in rows_by_cluster.items():
            # Cluster header
            grp = tk.Frame(body, bg=S["yellow"])
            grp.pack(fill="x", pady=(8, 2))
            tk.Label(grp, text=str(cluster_id), bg=S["yellow"], font=S["f_b"], width=8).grid(row=0, column=0)
            tk.Label(grp, text=f"Cluster {cluster_id}", bg=S["yellow"], font=S["f_b"], anchor="w", padx=10).grid(row=0, column=1, sticky="w")

            for idx, row in rows:  # Show all questions per cluster
                bg = S["odd"] if idx % 2 else S["even"]
                r = tk.Frame(body, bg=bg)
                r.pack(fill="x", pady=1)
                r.grid_columnconfigure(1, weight=1)

                tk.Label(r, text=str(row.get("cluster_id", cluster_id)), bg=bg, width=8).grid(row=0, column=0, sticky="w")
                main_var = tk.IntVar(value=0)
                skill_var = tk.IntVar(value=0)
                interest_var = tk.IntVar(value=0)
                self.vars[(row.get("cluster_id", cluster_id), idx)] = (main_var, skill_var, interest_var)
                main_var.trace_add("write", lambda *_a, gid=row.get("cluster_id", cluster_id): self.update_subtotal(gid))
                skill_var.trace_add("write", lambda *_a, gid=row.get("cluster_id", cluster_id): self.update_subtotal(gid))
                interest_var.trace_add("write", lambda *_a, gid=row.get("cluster_id", cluster_id): self.update_subtotal(gid))

                # Main statement checkbox replaces the number label
                cb_main = tk.Checkbutton(r, text="", variable=main_var, onvalue=1, offvalue=0, bg=bg)
                cb_main.grid(row=0, column=0, sticky="w", padx=(10, 6))
                tk.Label(
                    r,
                    text=f"{idx}. {row.get('main_statement', '')}",
                    bg=bg,
                    font=S["f"],
                    anchor="w",
                    justify="left",
                    wraplength=680,
                    padx=10
                ).grid(row=0, column=1, sticky="w")
                cb_skill = tk.Checkbutton(r, text=row.get('skill_statement', "(geen tekst)"), variable=skill_var, onvalue=1, offvalue=0, bg=bg)
                cb_skill.grid(row=0, column=2, sticky="e", padx=(0, 6))
                cb_interest = tk.Checkbutton(r, text=row.get('interest_statement', "(geen tekst)"), variable=interest_var, onvalue=1, offvalue=0, bg=bg)
                cb_interest.grid(row=0, column=3, sticky="e", padx=(0, 10))

            # subtotal row
            sub = tk.Frame(body, bg=S["yellow"])
            sub.pack(fill="x", pady=(2, 6))
            sub.grid_columnconfigure(1, weight=1)

            tk.Label(sub, text="", bg=S["yellow"], width=8).grid(row=0, column=0)
            tk.Label(sub, text=f"Totaal score ({len(rows)} stellingen)", bg=S["yellow"], font=S["f_b"], anchor="w", padx=10).grid(row=0, column=1, sticky="w")
            tk.Label(sub, text="", bg=S["yellow"], width=22).grid(row=0, column=2)

            lbl = tk.Label(sub, text="0", bg=S["yellow"], font=S["f_b"], width=8, anchor="e", padx=10)
            lbl.grid(row=0, column=3, sticky="e")
            self.sub_lbl[cluster_id] = lbl
            self.update_subtotal(cluster_id)

        # right descriptions
        tk.Label(right, text="Cultuur – omschrijving", bg=S["bg"], font=S["f_b"], anchor="w")\
            .pack(fill="x", pady=(0, 8))
        for g in GROUPS:
            box = tk.Frame(right, bg="#f5f5f5", bd=1, relief="solid")
            box.pack(fill="x", pady=6)
            tk.Label(box, text=g.name, bg=S["yellow"], font=S["f_b"], pady=6).pack(fill="x")
            tk.Label(
                box,
                text=g.desc,
                bg="#f5f5f5",
                font=S["f"],
                wraplength=360,
                justify="left",
                anchor="w",
                padx=8,
                pady=8
            ).pack(fill="x")

        # submit
        btn_row = tk.Frame(inner, bg=S["bg"])
        btn_row.pack(fill="x", padx=20, pady=(12, 20))

        tk.Button(
            btn_row,
            text="Opslaan en verder",
            bg=S["btn_on"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=6,
            command=self.submit
        ).pack(side="right")

    def submit(self):
        # Save checkbox results (0/1) and totals per group
        self.cultuur_results = {}
        for k, v in self.vars.items():
            # v may be a tuple (skill_var, interest_var)
            if isinstance(v, tuple) and len(v) == 2:
                skill_var, interest_var = v
                try:
                    sval = int(skill_var.get())
                except Exception:
                    sval = 0
                try:
                    ival = int(interest_var.get())
                except Exception:
                    ival = 0
                self.cultuur_results[k] = {"skill": sval, "interest": ival}
            else:
                # fallback for single var
                try:
                    self.cultuur_results[k] = int(v.get())
                except Exception:
                    self.cultuur_results[k] = v

        self.cultuur_totals = {g.id: self.subtotal(g.id) for g in GROUPS}

        # Proceed to next page
        self.navigate("phase2.2")



# -------------------- BUILDER FUNCTION --------------------
def build_carriereclusters_page(parent_frame: tk.Frame, navigate=None) -> None:
    clear_frame(parent_frame)
    page = Culture22Page(parent_frame, navigate)
    page.pack(fill="both", expand=True)
