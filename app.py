from http import client
import tkinter as tk
from tkinter import ttk
import json
import os
import ctypes
from xmlrpc import client
import phases.phase11
from PIL import Image, ImageTk
_USE_PILLOW = True
from tkinter import simpledialog, messagebox
from ui.ui_styles import *
from phases.phase11 import build_assessments_page
from phases.phase20 import build_career_anchors_page
from phases.phase21 import build_carriereclusters_page
from phases.phase22 import build_cultuur_page
from phases.phase23 import build_job_characteristics_models_page

root = tk.Tk()
root.title("LABOR - Applicatie")
root.geometry("1000x600")
root.configure(bg="#f0f0f0")
root.state("zoomed")
phase_history = []

myappid = 'mycompany.myproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
root.iconbitmap(r"icon.ico")

# --------- Global Assessment Variables ---------
current_assessment_client = None

# --------- Phase Mapping ---------
PHASES = {
    "phase1.1": build_assessments_page,
    "phase2.0": build_career_anchors_page,
    "phase2.1": build_carriereclusters_page,
    "phase2.2": build_cultuur_page,
    "phase2.3": build_job_characteristics_models_page,
}

# --------- Colors & Styling ---------

from ui.ui_components import create_sidebar, add_logo_to_sidebar

# --------- Sidebar ---------
SIDEBAR_WIDTH = 200
sidebar = create_sidebar(root, bg=COLOR_PRIMARY, width=SIDEBAR_WIDTH)
logo_label = add_logo_to_sidebar(sidebar, logo_path=os.path.join("images", "labor-logo.png"), use_pillow=_USE_PILLOW, bg=COLOR_PRIMARY)

def go_back_phase():
    if len(phase_history) > 1:
        phase_history.pop()                 
        navigate_phase(phase_history.pop()) 

back_button = tk.Button(
    sidebar,
    text="← Terug",
    command=go_back_phase,
    bg=COLOR_PRIMARY,
    fg="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
)
back_button.pack(pady=50, padx=50, anchor="w")

# --------- Data Storage ---------
clients_file = "clients.json"

def load_clients():
    """Load clients from JSON file."""
    if os.path.exists(clients_file):
        with open(clients_file, "r") as f:
            return json.load(f)
    return []

def save_clients(clients):
    """Save clients to JSON file."""
    with open(clients_file, "w") as f:
        json.dump(clients, f, indent=2)

def search_clients(query):
    """Filter clients by name/ID."""
    clients = load_clients()
    return [c for c in clients if query.lower() in c.get("name", "").lower()]

def show_create_client_form():
    """Display form to create a new client with all fields."""
    clear_content_frame()

    button_frame = tk.Frame(content_frame, bg=COLOR_BG)
    button_frame.pack(fill="x", padx=20, pady=(0, 20))
    text: str = "← Terug naar Klantenlijst"
    tk.Button(
        button_frame,
        text=text,
        command=show_client_list,
        bg=COLOR_TEXT_LIGHT,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=5
    ).pack(side="left")

    form_frame = tk.Frame(content_frame, bg=COLOR_BG)
    form_frame.pack(padx=40, pady=30, fill="x")

    tk.Label(
        form_frame,
        text="Nieuwe Klant Toevoegen",
        font=("Segoe UI", 20, "bold"),
        bg=COLOR_BG,
        fg=COLOR_PRIMARY
    ).pack(anchor="w", pady=(0, 20))

    # Dictionary to store entry widgets
    entries = {}

    fields = [
        "Naam",
        "Geboortedatum",
        "Email",
        "Telefoonnummer",
        "Adres",
        "Opleidingen",
        "Land van herkomst"
    ]

    for field in fields:
        row = tk.Frame(form_frame, bg=COLOR_BG)
        row.pack(fill="x", pady=5)

        tk.Label(
            row,
            text=field,
            width=20,
            anchor="w",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(side="left")

        entry = tk.Entry(row, font=("Segoe UI", 11))
        entry.pack(side="left", fill="x", expand=True)

        entries[field] = entry

    # Save button
    def save_client():
        name = entries["Naam"].get().strip()

        if not name:
            messagebox.showerror("Fout", "Naam is verplicht.")
            return

        clients = load_clients()
        client_id = max([c["id"] for c in clients], default=0) + 1

        new_client = {
            "id": client_id,
            "name": name,
            "Date of Birth": entries["Geboortedatum"].get(),
            "email": entries["Email"].get(),
            "phone number": entries["Telefoonnummer"].get(),
            "address": entries["Adres"].get(),
            "Qualifications": entries["Opleidingen"].get(),
            "Country of origin": entries["Land van herkomst"].get(),
            "assessments": [],
            "prognosis": []
        }

        clients.append(new_client)
        save_clients(clients)

        # Create client folder and info.json
        import os, json
        safe_name = "_".join(name.split())
        folder_name = f"{client_id}_{safe_name}"
        client_dir = os.path.join("clients", folder_name)
        os.makedirs(client_dir, exist_ok=True)
        client_json_path = os.path.join(client_dir, "info.json")
        with open(client_json_path, "w", encoding="utf-8") as f:
            json.dump(new_client, f, indent=2, ensure_ascii=False)

        messagebox.showinfo("Succes", f"Client '{name}' aangemaakt!")
        show_client_list()

    tk.Button(
        form_frame,
        text="Opslaan",
        command=save_client,
        bg=COLOR_SUCCESS,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=20,
        pady=10
    ).pack(pady=20)

def clear_content_frame():
    """Clear the content area."""
    for widget in content_frame.winfo_children():
        widget.destroy()

def refresh_client_list(query=""):
    """Refresh the client list display."""
    clear_content_frame()
    
    # Client list container
    list_container = tk.Frame(content_frame, bg=COLOR_BG)
    list_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # Populate list
    clients = search_clients(query) if query else load_clients()
    
    # Create listbox
    client_listbox = tk.Listbox(
        list_container,
        font=("Segoe UI", 15),
        bg="white",
        fg=COLOR_TEXT,
        relief="flat",
        bd=15,
        highlightthickness=0,
        activestyle="none",
        selectmode="single"
    )
    client_listbox.pack(fill="both", expand=True, side="left")
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=client_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    client_listbox.config(yscrollcommand=scrollbar.set)
    
    # Add clients to listbox
    for i, client in enumerate(clients):
        client_listbox.insert(tk.END, f"{client['name']}")
    
    # Bind click to open dashboard
    def on_select(event):
        sel = client_listbox.curselection()
        if sel:
            open_client_dashboard(clients[sel[0]])
    
    client_listbox.bind("<Double-Button-1>", on_select)

def open_phase11_assessment(client):
    """Start the assessment questionnaire for a client."""
    global current_assessment_client
    current_assessment_client = client
    navigate_phase("phase1.1")

def navigate_phase(phase_name):
    """Navigate to a specific phase."""
    
    if phase_name == "phase1.1":
        top_frame.pack_forget()

    if phase_name not in PHASES:
        messagebox.showerror("Error", f"Unknown phase: {phase_name}")
        return
    
    phase_history.append(phase_name)
    build_func = PHASES[phase_name]
    # Pass current_assessment_client to phase1.1 via parent_frame
    if phase_name == "phase1.1":
        content_frame.current_assessment_client = current_assessment_client
    build_func(content_frame, navigate_phase)

def show_client_list(query=""):
    """Display the client list view."""
    top_frame.pack(fill="x", padx=20, pady=15)
    search_entry.delete(0, tk.END)
    refresh_client_list(query)

def run_assessment(client):
    """Launch assessment questionnaire for the client."""
    open_phase11_assessment(client)

def run_prognosis(client):
    """Launch prognosis questionnaire for the client."""
    # TODO: Launch prognosis questionnaire

def view_client_results(client):
    """View results for this client."""
    # TODO: Show results

def open_client_dashboard(client):
    """Open the dashboard for this client with assessment and prognosis buttons."""
    clear_content_frame()
    info_frame = tk.Frame(content_frame, bg=COLOR_BG)
    info_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Client info header
    header_frame = tk.Frame(content_frame, bg=COLOR_PRIMARY)
    header_frame.pack(fill="x", padx=20, pady=(10, 30))

        # Back button
    back_btn = tk.Button(
        content_frame,
        text="← Terug naar Klantenlijst",
        command=show_client_list,
        bg=COLOR_TEXT_LIGHT,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=5,
        relief="flat",
        cursor="hand2"
    )
    back_btn.pack(anchor="w", padx=20, pady=10)
    
    tk.Label(
        header_frame,
        text=client["name"],
        font=("Segoe UI", 24, "bold"),
        bg=COLOR_PRIMARY,
        fg="white"
    ).pack(anchor="w")

    info_fields = [
        ("Geboortedatum", client.get("Date of Birth", "")),
        ("Email", client.get("email", "")),
        ("Telefoon", client.get("phone number", "")),
        ("Adres", client.get("address", "")),
        ("Opleidingen", client.get("Qualifications", "")),
        ("Land", client.get("Country of origin", "")),
]

    for label, value in info_fields:
        tk.Label(
        info_frame,
        text=f"{label}: {value}",
        font=("Segoe UI", 11),
        bg=COLOR_BG,
        fg=COLOR_TEXT
    ).pack(anchor="w")
    
    tk.Label(
        header_frame,
        font=("Segoe UI", 11),
        bg=COLOR_PRIMARY,
        fg=COLOR_LIGHT
    ).pack(anchor="w")
    
    # Action buttons frame
    buttons_container = tk.Frame(content_frame, bg=COLOR_BG)
    buttons_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    buttons_frame = tk.Frame(buttons_container, bg=COLOR_BG)
    buttons_frame.pack(fill="x", expand=False)
    
    # Assessment Button
    tk.Button(
        buttons_frame,
        text="📋 Assessment Vragenlijst",
        command=lambda: run_assessment(client),
        bg=COLOR_SECONDARY,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=30,
        pady=20,
        relief="flat",
        cursor="hand2",
        activebackground="#2980b9"
    ).pack(pady=10, fill="x")
    
    # Prognosis Button
    tk.Button(
        buttons_frame,
        text="🔮 Prognosis Vragenlijst",
        command=lambda: run_prognosis(client),
        bg=COLOR_ACCENT,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=30,
        pady=20,
        relief="flat",
        cursor="hand2",
        activebackground="#c0392b"
    ).pack(pady=10, fill="x")
    
    # View Results Button
    tk.Button(
        buttons_frame,
        text="📊 Bekijk Resultaten",
        command=lambda: view_client_results(client),
        bg=COLOR_SUCCESS,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=30,
        pady=20,
        relief="flat",
        cursor="hand2",
        activebackground="#229954"
    ).pack(pady=10, fill="x")

# --------- UI Layout ---------
main_frame = tk.Frame(root, bg=COLOR_BG)
main_frame.pack(fill="both", expand=True)

# Top bar with search and new client button
top_frame = tk.Frame(main_frame, bg=YELLOW_ACCENT, height=80)
top_frame.pack(fill="x", padx=20, pady=15)
top_frame.pack_propagate(False)
if navigate_phase == "phase1.1":
    visible = False

tk.Label(
    top_frame,
    text="Klantenbeheer",
    font=("Segoe UI", 22, "bold"),
    bg=YELLOW_ACCENT,
    fg=COLOR_PRIMARY
).pack(side="left", padx=10, pady=10)

# Search frame
search_frame = tk.Frame(top_frame, bg=YELLOW_ACCENT)
search_frame.pack(side="left", padx=(30, 10), anchor="w")

tk.Label(
    search_frame,
    text="Zoeken:",
    font=("Segoe UI", 10),
    bg=YELLOW_ACCENT,
    fg=COLOR_TEXT
).pack(side="left", padx=(0, 8))

search_entry = tk.Entry(
    search_frame,
    width=25,
    font=("Segoe UI", 10),
    relief="flat",
    bd=2
)
search_entry.pack(side="left")

tk.Button(
    search_frame,
    text="Zoeken",
    command=lambda: refresh_client_list(search_entry.get()),
    bg=COLOR_TEXT_LIGHT,
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=8)

# New client button
tk.Button(
    top_frame,
    text="+ Nieuwe Klant",
    command=show_create_client_form,
    bg=COLOR_TEXT_LIGHT,
    fg="white",
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2",
    activebackground=COLOR_TEXT_LIGHT
).pack(side="right", padx=15)

# Content frame - this swaps between list view and dashboard
content_frame = tk.Frame(main_frame, bg=COLOR_BG)
content_frame.pack(fill="both", expand=True)

# Initialize the client list display
show_client_list()

root.mainloop()

# Add to imports at the top of app.py:
from phases.phase11 import build_assessments_page
from phases.phase20 import build_career_anchors_page
from phases.phase21 import build_carriereclusters_page
from phases.phase22 import build_cultuur_page
from phases.phase23 import build_job_characteristics_models_page

# Global to track current client during questionnaire
current_assessment_client = None

# Phase mapping
PHASES = {
    "phase1.1": build_assessments_page,
    "phase2.0": build_career_anchors_page,
    "phase2.1": build_carriereclusters_page,
    "phase2.2": build_cultuur_page,
    "phase2.3": build_job_characteristics_models_page,
}

def navigate_phase(phase_name):
    """Navigate to a specific phase."""
    if phase_name not in PHASES:
        messagebox.showerror("Error", f"Unknown phase: {phase_name}")
        return
    
    build_func = PHASES[phase_name]
    build_func(content_frame, navigate_phase)

def open_phase11_assessment(client):
    """Start the assessment questionnaire for a client."""
    global current_assessment_client
    current_assessment_client = client
    navigate_phase("phase1.1")

try:
    root.mainloop()
except KeyboardInterrupt:
    pass