# fase2en2_short.py
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass

# ---------- Data ----------
@dataclass(frozen=True)
class Group:
    id: int
    name: str
    desc: str
    stmts: list[str]

GROUPS = [
    Group(1, "Mensgerichte cultuur",
          "Typerend voor zorginstellingen en servicegerichte organisaties.",
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

LIKERT = ["1", "2", "3", "4", "5"]

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

# Helpers 
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

    inner.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
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

    for i, v in enumerate(LIKERT):
        b = tk.Button(f, text=v, width=3, bd=1, font=S["f"], cursor="hand2",
                      command=lambda x=v: choose(x), bg=S["btn"])
        b.grid(row=0, column=i, padx=3)
        buttons[v] = b

    refresh()
    return f


# Page 
class App(tk.Frame):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent, bg=S["bg"])
        self.vars: dict[tuple[int, int], tk.StringVar] = {}
        self.sub_lbl: dict[int, tk.Label] = {}
        self.build()

    def subtotal(self, gid: int) -> int:
        tot = 0
        for i in range(1, 5):
            v = self.vars[(gid, i)].get().strip()
            if v.isdigit():
                tot += int(v)
        return tot

    def update_subtotal(self, gid: int):
        self.sub_lbl[gid].config(text=str(self.subtotal(gid)))

    def build(self):
        _, _, inner = scrollable(self)

        tk.Label(inner, text="Cultuur | Beoordeling van stellingen (1–5)",
                 bg=S["bg"], font=S["f_title"], anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        tk.Label(inner, text="Beoordeel elke stelling: 1=oneens … 5=volledig eens.",
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
        tk.Label(h, text="Cultuur", bg=S["dark"], fg="white", font=S["f_b"], width=8, anchor="w", padx=10)\
            .grid(row=0, column=0, sticky="w")
        tk.Label(h, text="Aspecten: stellingen", bg=S["dark"], fg="white", font=S["f_b"], anchor="w", padx=10)\
            .grid(row=0, column=1, sticky="w")
        tk.Label(h, text="Score", bg=S["dark"], fg="white", font=S["f_b"], width=22, anchor="e", padx=10)\
            .grid(row=0, column=2, sticky="e")
        tk.Label(h, text="Totaal", bg=S["dark"], fg="white", font=S["f_b"], width=8, anchor="e", padx=10)\
            .grid(row=0, column=3, sticky="e")

        body = tk.Frame(left, bg=S["bg"])
        body.pack(fill="both", expand=True)

        row_counter = 0
        for g in GROUPS:
            # group header
            grp = tk.Frame(body, bg=S["yellow"])
            grp.pack(fill="x", pady=(8, 2))
            tk.Label(grp, text=str(g.id), bg=S["yellow"], font=S["f_b"], width=8).grid(row=0, column=0)
            tk.Label(grp, text=g.name, bg=S["yellow"], font=S["f_b"], anchor="w", padx=10)\
                .grid(row=0, column=1, sticky="w")

            # 4 statements
            for i, stmt in enumerate(g.stmts, start=1):
                row_counter += 1
                bg = S["odd"] if row_counter % 2 else S["even"]
                r = tk.Frame(body, bg=bg)
                r.pack(fill="x", pady=1)

                # make text column stretch => buttons go to far right
                r.grid_columnconfigure(1, weight=1)

                tk.Label(r, text="", bg=bg, width=8).grid(row=0, column=0, sticky="w")
                tk.Label(r, text=f"{i}. {stmt}", bg=bg, font=S["f"], anchor="w",
                         justify="left", wraplength=680, padx=10)\
                    .grid(row=0, column=1, sticky="w")

                v = tk.StringVar(value="")
                self.vars[(g.id, i)] = v
                v.trace_add("write", lambda *_a, gid=g.id: self.update_subtotal(gid))

                make_likert_buttons(r, v, bg).grid(row=0, column=2, sticky="e", padx=(10, 25))
                tk.Label(r, text="", bg=bg, width=8).grid(row=0, column=3, sticky="e")

            # subtotal row
            sub = tk.Frame(body, bg=S["yellow"])
            sub.pack(fill="x", pady=(2, 6))
            sub.grid_columnconfigure(1, weight=1)

            tk.Label(sub, text="", bg=S["yellow"], width=8).grid(row=0, column=0)
            tk.Label(sub, text="Totaal score (4 stellingen)", bg=S["yellow"], font=S["f_b"],
                     anchor="w", padx=10).grid(row=0, column=1, sticky="w")
            tk.Label(sub, text="", bg=S["yellow"], width=22).grid(row=0, column=2)
            lbl = tk.Label(sub, text="0", bg=S["yellow"], font=S["f_b"], width=8, anchor="e", padx=10)
            lbl.grid(row=0, column=3, sticky="e")
            self.sub_lbl[g.id] = lbl
            self.update_subtotal(g.id)

        # right descriptions
        tk.Label(right, text="Cultuur – omschrijving", bg=S["bg"], font=S["f_b"], anchor="w")\
            .pack(fill="x", pady=(0, 8))
        for g in GROUPS:
            box = tk.Frame(right, bg="#f5f5f5", bd=1, relief="solid")
            box.pack(fill="x", pady=6)
            tk.Label(box, text=g.name, bg=S["yellow"], font=S["f_b"], pady=6).pack(fill="x")
            tk.Label(box, text=g.desc, bg="#f5f5f5", font=S["f"], wraplength=360,
                     justify="left", anchor="w", padx=8, pady=8).pack(fill="x")

        # submit
        btn_row = tk.Frame(inner, bg=S["bg"])
        btn_row.pack(fill="x", padx=20, pady=(12, 20))

        tk.Button(btn_row, text="Opslaan en verder", bg=S["btn_on"], fg="white",
                  font=("Segoe UI", 11, "bold"), padx=20, pady=6, command=self.submit)\
            .pack(side="right")

    def submit(self):
        missing = [(gid, i) for gid in range(1, 5) for i in range(1, 5) if not self.vars[(gid, i)].get().strip()]
        if missing:
            messagebox.showwarning("Onvolledige vragenlijst",
                                   f"Er zijn nog {len(missing)} stellingen niet ingevuld.")
            return
        totals = "\n".join([f"{g.id}. {g.name}: {self.subtotal(g.id)}" for g in GROUPS])
        messagebox.showinfo("Resultaat (totaal per cultuur)", totals)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cultuur – vragenlijst (kort) met subtotal per 4 stellingen")
    root.geometry("1400x750")

    App(root).pack(fill="both", expand=True)
    root.mainloop()
