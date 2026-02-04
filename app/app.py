import tkinter as tk
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from PIL import Image, ImageTk
    _USE_PILLOW = True
except Exception:
    _USE_PILLOW = False
import phases.assessments_new as assessments_new  # assessments_new.py
import phases.phase20 as phase20  # phase20.py
import prognosis_model # prognosis_model.py
 
# --------- Start screen ---------
root = tk.Tk()
root.title("LABOR - Applicatie")
root.geometry("1000x600")
root.configure(bg="white")

# --------- Sidebar ---------
SIDEBAR_WIDTH = 180

sidebar = tk.Frame(root, bg="black", width=SIDEBAR_WIDTH)
sidebar.pack(side="left", fill="y")

# Prevent pack from resizing the sidebar
sidebar.pack_propagate(False)

# Test if Pillow is available

logo_label = None
if _USE_PILLOW: 
    print("Pillow is available for image processing.")
else:
    print("Pillow is not availbable. Use Tkinter's PhotoImage.")
 
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

    phase20.build_career_anchors_page(content)


def navigate_to(page: str):
    """Router function to navigate to different pages based on string identifier."""
    if page == "phase2.0":
        open_career_anchors()
    elif page == "assessments":
        open_assessments()
    elif page == "home":
        show_home()
    # Add other pages as needed


def open_assessments():
    """Show the assessments page (Big Five) within content."""
    show_back_button()
    btn_back.config(command=show_home)

    for w in content.winfo_children():
        w.destroy()

    assessments_new.build_assessments_page(content, navigate_to)

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

    # TODO: Add phase21 implementation when available
    # frame_21 = phase21.create_career_clusters_frame(content)
    # frame_21.pack(fill="both", expand=True)


# --------- Load the start screen back ---------
show_home()

root.mainloop()