# career_clusters.py
import tkinter as tk
from tkinter import ttk, messagebox

# -------------------- STYLING --------------------
MAIN_BG = "#ffffff"
HEADER_BG = "#ffffff"
TABLE_HEADER_BG = "#f2f2f2"
ROW_ALT_BG = "#fafafa"
SCORE_BG = "#efefef"
BORDER = "#2b2b2b"
TEXT = "#111111"
MUTED = "#333333"

FONT_H1 = ("Segoe UI", 16, "bold")
FONT_SUB = ("Segoe UI", 10)
FONT_TH = ("Segoe UI", 10, "bold")
FONT_SEG_TITLE = ("Segoe UI", 10, "bold")
FONT_SEG_DESC = ("Segoe UI", 9)
FONT_SCORE = ("Segoe UI", 10)
FONT_TOTAL = ("Segoe UI", 10, "bold")

# -------------------- DATA (16 CLUSTERS) --------------------
CLUSTERS = [
    (1, "Landbouw, voeding en natuurlijke grondstoffen",
     "De productie, verwerking, marketing, distributie, financiering en ontwikkeling van agrarische grondstoffen en hulpbronnen waaronder voedsel, vezels, houtproducten, natuurlijke hulpbronnen, tuinbouw, en andere plantaardige en dierlijke producten cq. hulpbronnen."),
    (2, "Architectuur en constructie",
     "Carrières bij het ontwerpen, plannen, beheren, bouwen en behoud van de gebouwde omgeving."),
    (3, "Kunst, audio- visuele technologie en communicatie",
     "Ontwerpen, produceren, vertonen, uitvoeren, schrijven en publiceren van multimedia-inhoud waaronder visuele en podiumkunsten, design, journalistiek en entertainmentdiensten."),
    (4, "Business Management en administratie",
     "Business Management en administratie loopbaan omvatten het plannen, organiseren, leiden en evalueren van zakelijke functies essentieel voor efficiënte en productieve bedrijfsactiviteiten. Management en administratie carrièremogelijkheden zijn beschikbaar in elke sector van de economie."),
    (5, "Educatie en training",
     "Planning, beheer en verstrekking van onderwijs- en opleidingsdiensten en gerelateerde ondersteuningsdiensten."),
    (6, "Financiën",
     "Planning, services voor financiële en investeringsplanning, bankieren, verzekeringen en bedrijfsfinancieel beheer."),
    (7, "Overheid en publieke administratie",
     "Het uitvoeren van overheidsfuncties om governance op te nemen. Denkende aan nationale veiligheid, buitenlandse dienst, planning, inkomsten en belastingen, regulatie en beheer en administratie bij de lokale staat en federale niveaus."),
    (8, "Gezondheidswetenschappen",
     "Planning, beheer en levering van therapeutische diensten, diagnostische diensten, medische informatica, ondersteunende diensten en biotechnologie onderzoek en ontwikkeling."),
    (9, "Hospitality en toerisme",
     "Hospitality en toerisme omvat het management, marketing en activiteiten van restaurants en andere eetgelegenheden, logies, attracties en recreatie-evenementen en reisgerelateerde diensten."),
    (10, "Humanitaire dienstverlening",
     "Individuen voorbereiden op een baan in loopbaantrajecten en betrekking hebben op gezinnen en menselijke behoeften."),
    (11, "ICT",
     "Verbanden leggen in een IT-beroepskader voor instapniveau, technische en professionele loopbanen gerelateerd aan het ontwerp, ontwikkeling, ondersteuning en beheer van hardware, software, multimedia- en systeemintegratiediensten."),
    (12, "Publieke veiligheid en zekerheid",
     "Planning, beheer en verstrekking van wettelijke, openbare veiligheid, beschermende diensten en binnenlandse veiligheid inclusief professionele en technische ondersteuningsdiensten."),
    (13, "Fabricage",
     "Planning, beheer en uitvoering van de verwerking van materialen in tussentijdse of eindproducten en aanverwante professionele en technische ondersteuningsactiviteiten zoals productieplanning en controle, onderhoud en productie / procestechniek."),
    (14, "Marketing, sales en service",
     "Planning, beheer en uitvoering van marketingactiviteiten ten behoeve van het bereiken van organisatorische doelstellingen."),
    (15, "Wetenschap, technologie, engineering en mathematica",
     "Planning, beheer en bijdrage van wetenschappelijk onderzoek en professionele en technische diensten (bijv; wetenschap en techniek) inclusief laboratorium- en testdiensten en onderzoeks- en ontwikkelingsdiensten."),
    (16, "Transport, distributie en logistiek",
     "Planning, beheer en verplaatsing van mensen, materialen en goederen over de weg, pijpleiding, lucht, spoor en water en aanverwante professionele en technische ondersteuningsdiensten zoals transportinfrastructuur, planning en beheer, logistieke diensten, mobiele apparatuur en onderhoud van faciliteiten."),
]

# -------------------- HELPERS --------------------
def clear_frame(frame: tk.Widget) -> None:
    for w in frame.winfo_children():
        w.destroy()


# -------------------- PAGE --------------------
class CareerClusters21Page(tk.Frame):
    def __init__(self, parent: tk.Widget, navigate):
        super().__init__(parent, bg=MAIN_BG)
        self.navigate = navigate

        self.scores = {cid: {"act": 0, "comp": 0, "edu": 0} for cid, *_ in CLUSTERS}
        self.score_labels = {}  # cid -> (act_lbl, comp_lbl, edu_lbl, total_lbl)

        self._build()

    # -------- UI builders --------
    def _build(self):
        # Titleblock
        header = tk.Frame(self, bg=HEADER_BG)
        header.pack(fill="x", padx=22, pady=(18, 10))

        tk.Label(header, text="FASE 2.1 – Carrièreclusters", bg=HEADER_BG, fg=TEXT, font=FONT_H1)\
            .pack(anchor="w")

        tk.Label(
            header,
            text="Per cluster: klik op 'Invullen' en selecteer de stellingen die passen. De scores worden automatisch berekend.",
            bg=HEADER_BG, fg=MUTED, font=FONT_SUB
        ).pack(anchor="w", pady=(6, 0))

        # Wrapper for table
        table_wrap = tk.Frame(self, bg=MAIN_BG)
        table_wrap.pack(fill="both", expand=True, padx=22, pady=(0, 10))  # iets minder onderruimte, want we hebben knop

        # Column widths
        self.col_w = {
            "cluster": 70,
            "segment": 560,
            "act": 120,
            "comp": 120,
            "edu": 120,
            "total": 80,
            "btn": 170
        }

        # Header row (fixed)
        hdr = tk.Frame(table_wrap, bg=MAIN_BG)
        hdr.pack(fill="x")

        self._th(hdr, "Cluster", self.col_w["cluster"])
        self._th(hdr, "Segment", self.col_w["segment"])
        self._th(hdr, "Activiteiten\n(max. 7)", self.col_w["act"])
        self._th(hdr, "Competenties\n(max. 5)", self.col_w["comp"])
        self._th(hdr, "Educatief\n(max. 5)", self.col_w["edu"])
        self._th(hdr, "Totaal", self.col_w["total"])
        self._th(hdr, "", self.col_w["btn"])

        # Scrollbar body
        body = tk.Frame(table_wrap, bg=MAIN_BG)
        body.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(body, bg=MAIN_BG, highlightthickness=0)
        self.vsb = ttk.Scrollbar(body, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")

        self.inner = tk.Frame(self.canvas, bg=MAIN_BG)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        for idx, (cid, segment, oms) in enumerate(CLUSTERS, start=1):
            self._row(self.inner, idx, cid, segment, oms)

        # ----- SAVE AND CONTINUE -----
        footer = tk.Frame(self, bg=MAIN_BG)
        footer.pack(fill="x", padx=22, pady=(0, 18))

        def on_submit_next():
            # at least 1 cluster filled in (total > 0)
            any_filled = any(
                (v["act"] + v["comp"] + v["edu"]) > 0
                for v in self.scores.values()
            )
            if not any_filled:
                messagebox.showwarning(
                    "Nog niets ingevuld",
                    "Vul minimaal één cluster in voordat je verder gaat."
                )
                return

        # Next, move on to your next page:
        # Adjust this to the next Phase Page
            self.navigate("phase2.2")  # bijv. "phase3.0"

        btn = tk.Button(
            footer,
            text="Opslaan en verder",
            bg="#4d4d4d",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=6,
            relief="flat",
            command=on_submit_next
        )
        btn.pack(side="right")

    def _th(self, parent, text, width):
        f = tk.Frame(parent, bg=TABLE_HEADER_BG, highlightbackground=BORDER, highlightthickness=1)
        f.pack(side="left", fill="y")
        f.configure(width=width, height=48)
        f.pack_propagate(False)

        tk.Label(f, text=text, bg=TABLE_HEADER_BG, fg=TEXT, font=FONT_TH, justify="center")\
            .pack(expand=True, fill="both")

    def _cell(self, parent, width, height, bg):
        f = tk.Frame(parent, bg=bg, highlightbackground=BORDER, highlightthickness=1)
        f.configure(width=width, height=height)
        f.pack_propagate(False)
        f.pack(side="left", fill="y")
        return f

    def _row(self, parent, idx, cid, segment, oms):
        row_h = 110
        row_bg = ROW_ALT_BG if idx % 2 == 0 else MAIN_BG

        r = tk.Frame(parent, bg=MAIN_BG)
        r.pack(fill="x")

        # Cluster
        c1 = self._cell(r, self.col_w["cluster"], row_h, row_bg)
        tk.Label(c1, text=str(cid), bg=row_bg, fg=TEXT, font=("Segoe UI", 10, "bold"))\
            .pack(expand=True)

        # Segment
        c2 = self._cell(r, self.col_w["segment"], row_h, row_bg)
        pad = tk.Frame(c2, bg=row_bg)
        pad.pack(fill="both", expand=True, padx=12, pady=10)

        tk.Label(pad, text=segment, bg=row_bg, fg=TEXT, font=FONT_SEG_TITLE, anchor="w")\
            .pack(anchor="w")
        tk.Label(
            pad,
            text=oms,
            bg=row_bg,
            fg=TEXT,
            font=FONT_SEG_DESC,
            justify="left",
            wraplength=self.col_w["segment"] - 28
        ).pack(anchor="w", pady=(6, 0))

        # Scores
        act = self._cell(r, self.col_w["act"], row_h, SCORE_BG)
        comp = self._cell(r, self.col_w["comp"], row_h, SCORE_BG)
        edu = self._cell(r, self.col_w["edu"], row_h, SCORE_BG)
        total = self._cell(r, self.col_w["total"], row_h, SCORE_BG)

        act_lbl = tk.Label(act, text="0", bg=SCORE_BG, fg=TEXT, font=FONT_SCORE)
        comp_lbl = tk.Label(comp, text="0", bg=SCORE_BG, fg=TEXT, font=FONT_SCORE)
        edu_lbl = tk.Label(edu, text="0", bg=SCORE_BG, fg=TEXT, font=FONT_SCORE)
        tot_lbl = tk.Label(total, text="0", bg=SCORE_BG, fg=TEXT, font=FONT_TOTAL)

        act_lbl.pack(expand=True)
        comp_lbl.pack(expand=True)
        edu_lbl.pack(expand=True)
        tot_lbl.pack(expand=True)

        self.score_labels[cid] = (act_lbl, comp_lbl, edu_lbl, tot_lbl)

        # Button
        cbtn = self._cell(r, self.col_w["btn"], row_h, row_bg)
        btn = tk.Button(
            cbtn,
            text="Invullen",
            font=("Segoe UI", 10, "bold"),
            relief="solid",
            bd=1,
            padx=16,
            pady=8,
            cursor="hand2",
            command=lambda x=cid: self.open_invullen(x)
        )
        btn.pack(fill="both", expand=True, padx=10, pady=18)

    # -------- scrolling --------
    def _on_inner_configure(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        sb = max(16, self.vsb.winfo_reqwidth())
        w = max(300, event.width - sb)
        self.canvas.itemconfig(self.inner_id, width=w)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # -------- popup --------
    def open_invullen(self, cid):
        root = self.winfo_toplevel()
        win = tk.Toplevel(root)
        win.title(f"Invullen – Cluster {cid}")
        win.geometry("520x340")
        win.configure(bg=MAIN_BG)

        tk.Label(win, text=f"Cluster {cid} – Invullen", bg=MAIN_BG, fg=TEXT, font=("Segoe UI", 14, "bold"))\
            .pack(anchor="w", padx=18, pady=(16, 8))

        tk.Label(
            win,
            text="Koppel hier later de echte stellingen (activiteiten/competenties/educatief).\n"
                 "Voor nu: klik op 'Opslaan' om dummy-scores te testen.",
            bg=MAIN_BG, fg=MUTED, font=("Segoe UI", 10), justify="left"
        ).pack(anchor="w", padx=18)

        box = tk.Frame(win, bg=MAIN_BG)
        box.pack(fill="x", padx=18, pady=16)

        act_var = tk.IntVar(value=self.scores[cid]["act"])
        comp_var = tk.IntVar(value=self.scores[cid]["comp"])
        edu_var = tk.IntVar(value=self.scores[cid]["edu"])

        for label, var, mx in [
            ("Activiteiten (max 7)", act_var, 7),
            ("Competenties (max 5)", comp_var, 5),
            ("Educatief (max 5)", edu_var, 5),
        ]:
            row = tk.Frame(box, bg=MAIN_BG)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label, bg=MAIN_BG, fg=TEXT, font=("Segoe UI", 10)).pack(side="left")
            sp = tk.Spinbox(row, from_=0, to=mx, width=6, textvariable=var)
            sp.pack(side="right")

        btns = tk.Frame(win, bg=MAIN_BG)
        btns.pack(fill="x", padx=18, pady=14)

        def save():
            self.scores[cid]["act"] = int(act_var.get())
            self.scores[cid]["comp"] = int(comp_var.get())
            self.scores[cid]["edu"] = int(edu_var.get())
            self.refresh_scores(cid)
            win.destroy()

        tk.Button(btns, text="Annuleren", command=win.destroy, relief="groove", bd=1, padx=14)\
            .pack(side="right")
        tk.Button(btns, text="Opslaan", command=save, relief="groove", bd=1, padx=18)\
            .pack(side="right", padx=(0, 10))

    def refresh_scores(self, cid):
        act = self.scores[cid]["act"]
        comp = self.scores[cid]["comp"]
        edu = self.scores[cid]["edu"]
        total = act + comp + edu

        act_lbl, comp_lbl, edu_lbl, tot_lbl = self.score_labels[cid]
        act_lbl.config(text=str(act))
        comp_lbl.config(text=str(comp))
        edu_lbl.config(text=str(edu))
        tot_lbl.config(text=str(total))


# -------------------- BUILDER FUNCTION --------------------
def build_carriereclusters_page(parent_frame: tk.Frame, navigate) -> None:
    clear_frame(parent_frame)
    page = CareerClusters21Page(parent_frame, navigate)
    page.pack(fill="both", expand=True)
