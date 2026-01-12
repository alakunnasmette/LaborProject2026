import tkinter as tk
import os
try:
    from PIL import Image, ImageTk
    _USE_PILLOW = True
except Exception:
    _USE_PILLOW = False
import assessments  # assessments.py
import prognosemodel # prognosemodel.py
 
# --------- 1. HOOFDVENSTER ---------
root = tk.Tk()
root.title("LABOR - Applicatie")
root.geometry("1000x600")
root.configure(bg="white")

# --------- 2. LINKER ZWARTE SIDEBAR ---------
SIDEBAR_WIDTH = 180

sidebar = tk.Frame(root, bg="black", width=SIDEBAR_WIDTH)
sidebar.pack(side="left", fill="y")

# voorkom dat pack de grootte van de sidebar aanpast
sidebar.pack_propagate(False)

#test

logo_label = None
if _USE_PILLOW: 
    print("Pillow is beschikbaar voor afbeeldingsverwerking.")
else:
    print("Pillow is NIET beschikbaar. Gebruik Tkinter's PhotoImage (beperkte formaten).")
    aiter
 
# --------- 3. LOGO ONDERIN ---------
logo_label = None
logo_path = os.path.join("images", "Labor-logo.png")
try:
    if _USE_PILLOW:
        # Use Pillow for reliable loading and high-quality resizing
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((140, 140), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_img)
    else:
        # Fallback to Tk's PhotoImage (supports PNG/GIF on modern Tk)
        logo = tk.PhotoImage(file=logo_path)
        # If image is larger than desired, try integer subsample scaling
        try:
            w = logo.width()
            h = logo.height()
            if w > 140 or h > 140:
                sx = max(1, int(round(w / 140)))
                sy = max(1, int(round(h / 140)))
                logo = logo.subsample(sx, sy)
        except Exception:
            pass

    logo_label = tk.Label(sidebar, image=logo, bg="black")
    # Keep a reference to avoid garbage collection
    logo_label.image = logo
    logo_label.place(relx=0.5, rely=1.0, anchor="s", y=-20)
except Exception as e:
    print("Logo fout:", e)
    logo_label = tk.Label(sidebar, text="LABOR LOGO", fg="white", bg="black")
    logo_label.place(relx=0.5, rely=1.0, anchor="s", y=-20)

# ---------  4. HOOFDCONTENT RECHTS ---------
content = tk.Frame(root, bg="white")
content.pack(side="right", expand=True, fill="both")

BUTTON_WIDTH = 18
BUTTON_HEIGHT = 4
BUTTON_BG = "#d9d9d9"
BUTTON_FONT = ("Segoe UI", 12)
BUTTOMN_ACTIVEBG = "#c0c0c0"


# --------- 5. PAGINA-FUNCTIES ---------

# Terug-knop: eerst maken, maar NOG NIET tonen en nog geen command
btn_back = tk.Button(
    sidebar,
    text="← Terug",
    bg="black",
    fg="white",
    relief="flat",
    bd=0,
    font=("Segoe UI", 11, "bold"),
    activebackground="black",
    activeforeground="white",
)

def show_back_button():
    """Laat de Terug-knop zien (alleen als hij nog niet zichtbaar is)."""
    if not btn_back.winfo_ismapped():
        btn_back.pack(anchor="nw", pady=20, padx=15)

def hide_back_button():
    """Verberg de Terug-knop als hij zichtbaar is."""
    if btn_back.winfo_ismapped():
        btn_back.pack_forget()

def show_home():
    """Toon de startpagina met 2 knoppen in de rechterkant."""
    # Terug-knop hoort NIET op de homepagina
    hide_back_button()

    # rechterkant leegmaken
    for w in content.winfo_children():
        w.destroy()

    button_frame = tk.Frame(content, bg="white")
    button_frame.pack(expand=True)

    btn_assessments = tk.Button(
        button_frame,
        text="Assessments",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        bg=BUTTON_BG,
        relief="flat",
        font=BUTTON_FONT,
        command=open_assessments,
    )
    btn_assessments.grid(row=0, column=0, padx=60, pady=20)

    btn_prognose = tk.Button(
        button_frame,
        text="Prognosemodel",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        bg=BUTTON_BG,
        relief="flat",
        font=BUTTON_FONT,
        command=open_prognose_model,
    )
    btn_prognose.grid(row=0, column=1, padx=60, pady=20)

def open_loopbaanankers():
    """Toon de pagina Fase 2.0 – Loopbaanankers in de rechterkant."""
    show_back_button()
    btn_back.config(command=open_assessments)

    for w in content.winfo_children():
        w.destroy()

    assessments.build_loopbaanankers_page(content)


def open_assessments():
    """Toon de assessmentspagina (Big Five) in dezelfde rechterkant."""
    show_back_button()
    btn_back.config(command=show_home)

    for w in content.winfo_children():
        w.destroy()

    assessments.build_assessments_page(content, open_loopbaanankers)

def open_prognose_model():
    """Toon de prognosemodel-pagina."""
    show_back_button()
    btn_back.config(command=show_home)

    for w in content.winfo_children():
        w.destroy()

    prognosemodel.build_prognose_page(content)

def open_carriereclusters():
    """Toon de pagina Fase 2.1 – Carrièreclusters in de rechterkant."""
    show_back_button()
    # Terug vanuit 2.1 moet naar 2.0
    btn_back.config(command=open_loopbaanankers)

    # rechterkant leegmaken
    for w in content.winfo_children():
        w.destroy()

    frame_21 = assessments.create_carriere_clusters_frame(content)
    frame_21.pack(fill="both", expand=True)


# --------- 6. START: HOME LADEN ---------
show_home()

root.mainloop()