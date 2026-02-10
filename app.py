import tkinter as tk
import os
import sys
import ctypes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from PIL import Image, ImageTk
    _USE_PILLOW = True
except Exception:
    _USE_PILLOW = False
import phases.phase11 as phase11  # phase10.py
import phases.phase20 as phase20  # phase20.py
import phases.phase21 as phase21  # phase21.py
import phases.phase22 as phase22  # phase22.py
import phases.phase23 as phase23  # phase23.py
import prognosis_model # prognosis_model.py
 
# --------- Start screen ---------
root = tk.Tk()
root.title("LABOR - Applicatie")
root.geometry("1000x600")
root.configure(bg="white")
root.state("zoomed")

myappid = 'mycompany.myproduct.version'  # Required for Windows
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
root.iconbitmap(r"icon.ico")  # Use raw string to avoid path issues

# --------- Sidebar ---------
SIDEBAR_WIDTH = 180

sidebar = tk.Frame(root, bg="black", width=SIDEBAR_WIDTH)
sidebar.pack(side="left", fill="y")

# Prevent pack from resizing the sidebar
sidebar.pack_propagate(False)



 
# --------- Sidebar logo ---------
logo_label = None
logo_path = os.path.join("images", "labor-logo.png")
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
    print("Logo error:", e)
    logo_label = tk.Label(sidebar, text="LABOR LOGO", fg="white", bg="black")
    logo_label.place(relx=0.5, rely=1.0, anchor="s", y=-20)

# ---------  Page content ---------
content = tk.Frame(root, bg="white")
content.pack(side="right", expand=True, fill="both")

BUTTON_WIDTH = 18
BUTTON_HEIGHT = 4
BUTTON_BG = "#d9d9d9"
BUTTON_FONT = ("Segoe UI", 12)
BUTTOMN_ACTIVEBG = "#c0c0c0"


# --------- Page functions ---------

# Back button
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
    """Show the back button if it is not already visible."""
    if not btn_back.winfo_ismapped():
        btn_back.pack(anchor="nw", pady=20, padx=15)

def hide_back_button():
    """Hide the back button if it is visible."""
    if btn_back.winfo_ismapped():
        btn_back.pack_forget()

def show_home():
    """Show the start screen."""
    # Hide back button on start screen
    hide_back_button()

    # Empty content
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

    btn_prognosis = tk.Button(
        button_frame,
        text="Prognosemodel",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        bg=BUTTON_BG,
        relief="flat",
        font=BUTTON_FONT,
        command=open_prognosis_model,
    )
    btn_prognosis.grid(row=0, column=1, padx=60, pady=20)

def open_career_anchors():
    """Show the Phase 2.0 – Career Anchors page within content."""
    show_back_button()
    btn_back.config(command=open_assessments)

    for w in content.winfo_children():
        w.destroy()

    phase20.build_career_anchors_page(content, navigate_to)


def open_cultuur():
    """Show the Phase 2.2 – Culture page within content."""
    show_back_button()
    # Back button from Phase 2.2 goes to Phase 2.1
    btn_back.config(command=open_career_clusters)

    # Empty content
    for w in content.winfo_children():
        w.destroy()

    phase22.build_cultuur_page(content, navigate_to)


def navigate_to(page: str):
    """Router function to navigate to different pages based on string identifier."""
    if page == "phase2.0":
        open_career_anchors()
    elif page == "phase2.1":
        open_career_clusters()
    elif page == "phase2.2":
        open_cultuur()
    elif page == "phase2.3":
        open_job_characteristics_models()
    elif page == "home":
        show_home()
    # Add other pages as needed

def open_job_characteristics_models():
    """Show the Job Characteristics Models page."""
    show_back_button()
    btn_back.config(command=open_cultuur)

    for w in content.winfo_children():
        w.destroy()

    phase23.build_job_characteristics_models_page(content, navigate_to)


def open_assessments():
    """Show the assessments page (Big Five) within content."""
    show_back_button()
    btn_back.config(command=show_home)

    for w in content.winfo_children():
        w.destroy()

    phase11.build_assessments_page(content, navigate_to)

def open_prognosis_model():
    """Show the prognosis model page."""
    show_back_button()
    btn_back.config(command=show_home)

    for w in content.winfo_children():
        w.destroy()

    prognosis_model.build_prognosis_page(content)

def open_career_clusters():
    """Show the Phase 2.1 – Career Clusters page within content."""
    show_back_button()
    # Back button from Phase 2.1 goes to Phase 2.0
    btn_back.config(command=open_career_anchors)

    # Empty content
    for w in content.winfo_children():
        w.destroy()

    # Set Excel file path for phase 2.1
    content.excel_file_path = os.path.join(os.getcwd(), "Loopbaan onderzoek 5.0 template.xlsx")

    # Try known builder names from phase21
    builder = None
    try:
        builder = getattr(phase21, "build_carriereclusters_page", None) or getattr(phase21, "build_loopbaanankers_page", None) or getattr(phase21, "create_career_clusters_frame", None)
    except Exception:
        builder = None

    if builder:
        try:
            builder(content, navigate_to)
        except TypeError:
            builder(content)
    else:
        # Fallback message
        lbl = tk.Label(content, text="Fase 2.1 is nog niet geïmplementeerd.", bg="white", fg="black")
        lbl.pack(padx=20, pady=20)


# --------- Load the start screen back ---------
show_home()

root.mainloop()