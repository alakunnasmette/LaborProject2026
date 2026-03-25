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
navigation_history = []  # Stack of (page_type, page_data) tuples

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

def push_history(page_type, page_data):
    """Push a page to the navigation history."""
    navigation_history.append((page_type, page_data))
    print(f"[DEBUG] Pushed to history: {page_type}, Stack size: {len(navigation_history)}")

def go_back():
    """Go back to the previous page. If no history, return to home (client list)."""
    global current_assessment_client
    
    if len(navigation_history) == 0:
        # Empty history, go to home
        push_history("client_list", {})
        show_client_list(push_to_history=False)
        return
    
    if len(navigation_history) == 1:
        # Only one page in history, just reload it
        page_type, page_data = navigation_history[0]
        if page_type == "client_list":
            show_client_list(push_to_history=False)
        else:
            # Go to home as default
            show_client_list(push_to_history=False)
        return
    
    # Pop current page
    navigation_history.pop()
    print(f"[DEBUG] Popped from history, Stack size: {len(navigation_history)}")
    
    # Load previous page from history
    page_type, page_data = navigation_history[-1]
    
    if page_type == "client_list":
        top_frame.pack(side="top", fill="x", padx=20, pady=15, before=content_frame)
        clear_content_frame()
        refresh_client_list()
    elif page_type == "client_dashboard":
        top_frame.pack(side="top", fill="x", padx=20, pady=15, before=content_frame)
        open_client_dashboard(page_data.get("client"), push_to_history=False)
    elif page_type == "phase":
        phase_name = page_data.get("phase_name")
        navigate_phase(phase_name, push_to_history=False)
    elif page_type == "create_client":
        top_frame.pack(side="top", fill="x", padx=20, pady=15, before=content_frame)
        show_create_client_form(push_to_history=False)
    else:
        show_client_list(push_to_history=False)

back_button = tk.Button(
    sidebar,
    text="← Terug",
    command=go_back,
    bg=COLOR_PRIMARY,
    fg="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
)
back_button.pack(pady=50, padx=50, anchor="w")

# --------- Data Storage ---------

# --- New client loading: scan clients/ directory ---
def load_clients():
    """Load clients by scanning the clients/ directory and reading info.json files."""
    clients_dir = "clients"
    clients = []
    if os.path.exists(clients_dir):
        for folder in os.listdir(clients_dir):
            info_path = os.path.join(clients_dir, folder, "info.json")
            if os.path.isfile(info_path):
                try:
                    with open(info_path, "r", encoding="utf-8") as f:
                        client = json.load(f)
                        clients.append(client)
                except Exception as e:
                    print(f"Error reading {info_path}: {e}")
    return clients

def search_clients(query):
    """Filter clients by name/ID."""
    clients = load_clients()
    return [c for c in clients if query.lower() in c.get("name", "").lower()]

def show_create_client_form(push_to_history=True):
    """Display form to create a new client with all fields."""
    if push_to_history:
        push_history("create_client", {})
    clear_content_frame()

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
        "Land van herkomst",
        "Leef situatie",
        "Toelichting (optioneel)"
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
            "Living situation": entries.get("Leef situatie", tk.Entry()).get(),
            "Empty text field": entries.get("Toelichting (optioneel)", tk.Entry()).get(),
            "assessments": [],
            "prognosis": []
        }



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

def show_client_list(query="", push_to_history=True):
    """Display the client list view."""
    if push_to_history:
        push_history("client_list", {})
    top_frame.pack(side="top", fill="x", padx=20, pady=15, before=content_frame)
    search_entry.delete(0, tk.END)
    refresh_client_list(query)

def run_assessment(client):
    """Launch assessment questionnaire for the client."""
    global current_assessment_client
    current_assessment_client = client
    # Also set on content_frame if available
    try:
        content_frame.current_assessment_client = client
    except Exception:
        pass
    open_phase11_assessment(client)

def run_prognosis(client):
    """Launch prognosis questionnaire for the client."""
    # TODO: Launch prognosis questionnaire

def view_client_results(client):
    """View results for this client."""
    # TODO: Show results

def open_client_dashboard(client, push_to_history=True):
    """Open the dashboard for this client with assessment and prognosis buttons."""
    global current_assessment_client
    current_assessment_client = client
    if push_to_history:
        push_history("client_dashboard", {"client": client})
    print(f"[DEBUG] Active client set: {client.get('name', 'UNKNOWN')} (ID: {client.get('id', 'UNKNOWN')})")
    clear_content_frame()
    info_frame = tk.Frame(content_frame, bg=COLOR_BG)
    info_frame.pack(fill="x", padx=20, pady=(0, 20))

    # Client info header
    header_frame = tk.Frame(content_frame, bg=COLOR_PRIMARY)
    header_frame.pack(fill="x", padx=20, pady=(10, 30))

    # --- Name and Edit Button Row ---
    name_edit_frame = tk.Frame(header_frame, bg=COLOR_PRIMARY)
    name_edit_frame.pack(anchor="w", fill="x")

    tk.Label(
        name_edit_frame,
        text=client["name"],
        font=("Segoe UI", 24, "bold"),
        bg=COLOR_PRIMARY,
        fg="white"
    ).pack(side="left", padx=(0, 10))

    def open_edit_client_info():
        clear_content_frame()

        form_frame = tk.Frame(content_frame, bg=COLOR_BG)
        form_frame.pack(padx=40, pady=30, fill="x")

        tk.Label(
            form_frame,
            text="Klantinformatie Bewerken",
            font=("Segoe UI", 20, "bold"),
            bg=COLOR_BG,
            fg=COLOR_PRIMARY
        ).pack(anchor="w", pady=(0, 20))

        entries = {}
        fields = [
            ("Naam", "name"),
            ("Geboortedatum", "Date of Birth"),
            ("Email", "email"),
            ("Telefoonnummer", "phone number"),
            ("Adres", "address"),
            ("Opleidingen", "Qualifications"),
            ("Land van herkomst", "Country of origin"),
            ("Leef situatie", "Living situation"),
            ("Toelichting (optioneel)", "Empty text field")
        ]
        for label, key in fields:
            row = tk.Frame(form_frame, bg=COLOR_BG)
            row.pack(fill="x", pady=5)
            tk.Label(
                row,
                text=label,
                width=20,
                anchor="w",
                bg=COLOR_BG,
                fg=COLOR_TEXT
            ).pack(side="left")
            entry = tk.Entry(row, font=("Segoe UI", 11))
            entry.insert(0, client.get(key, ""))
            entry.pack(side="left", fill="x", expand=True)
            entries[key] = entry

        def save_edited_client():
            updated = False
            old_name = client.get("name", "")
            old_safe_name = "_".join(old_name.split())
            old_folder_name = f"{client['id']}_{old_safe_name}"
            old_client_dir = os.path.join("clients", old_folder_name)
            for label, key in fields:
                value = entries[key].get().strip()
                if value != client.get(key, ""):
                    client[key] = value
                    updated = True
            if updated:
                # Rename folder if name changed
                new_safe_name = "_".join(client["name"].split())
                new_folder_name = f"{client['id']}_{new_safe_name}"
                new_client_dir = os.path.join("clients", new_folder_name)
                if old_client_dir != new_client_dir and os.path.exists(old_client_dir):
                    try:
                        os.rename(old_client_dir, new_client_dir)
                    except Exception as e:
                        messagebox.showwarning("Waarschuwing", f"Kon map niet hernoemen: {e}")
                else:
                    os.makedirs(new_client_dir, exist_ok=True)
                # Save to info.json
                client_json_path = os.path.join(new_client_dir, "info.json")
                with open(client_json_path, "w", encoding="utf-8") as f:
                    json.dump(client, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Succes", "Klantinformatie bijgewerkt!")
            open_client_dashboard(client)

        tk.Button(
            form_frame,
            text="Opslaan",
            command=save_edited_client,
            bg=COLOR_SUCCESS,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=20)

    edit_btn = tk.Button(
        name_edit_frame,
        text="✏️",
        command=open_edit_client_info,
        bg=COLOR_PRIMARY,
        fg="white",
        font=("Segoe UI", 12),
        relief="flat",
        cursor="hand2",
        width=2,
        height=1
    )
    edit_btn.pack(side="left", padx=(0, 5))

    info_fields = [
        ("Geboortedatum", client.get("Date of Birth", "")),
        ("Email", client.get("email", "")),
        ("Telefoon", client.get("phone number", "")),
        ("Adres", client.get("address", "")),
        ("Opleidingen", client.get("Qualifications", "")),
        ("Land", client.get("Country of origin", "")),
        ("Leef situatie", client.get("Living situation", "")),
        ("Toelichting", client.get("Empty text field", ""))
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
top_frame.pack(side="top", fill="x", padx=20, pady=15)
top_frame.pack_propagate(False)

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
content_frame.pack(side="top", fill="both", expand=True)

# DEBUG: show children of main_frame
print("Children of main_frame:")
for widget in main_frame.winfo_children():
    print(widget)

# Initialize the client list display
show_client_list()

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

def navigate_phase(phase_name, push_to_history=True):
    """Navigate to a specific phase or handle special navigation."""
    global current_assessment_client
    
    # Handle special navigation
    if phase_name == "go_back":
        go_back()
        return
    
    if phase_name not in PHASES:
        messagebox.showerror("Error", f"Unknown phase: {phase_name}")
        return
    
    # Push to history
    if push_to_history:
        push_history("phase", {"phase_name": phase_name})
    
    # Hide header when entering a phase
    top_frame.pack_forget()
    
    build_func = PHASES[phase_name]
    
    # Set up phase context (excel path, etc.)
    if phase_name == "phase1.1":
        content_frame.current_assessment_client = current_assessment_client
        if current_assessment_client:
            print(f"[DEBUG] Passing client to phase1.1: {current_assessment_client.get('name', 'UNKNOWN')} (ID: {current_assessment_client.get('id', 'UNKNOWN')})")
        else:
            print("[DEBUG] No active client to pass to phase1.1!")
    
    # Set results_excel_path for phase2.x if client context is available
    if phase_name in ("phase2.0", "phase2.1", "phase2.2", "phase2.3") and hasattr(content_frame, "current_assessment_client"):
        client = content_frame.current_assessment_client
        safe_name = "_".join(client["name"].split())
        folder_name = f"{client['id']}_{safe_name}"
        client_dir = os.path.join("clients", folder_name)
        excel_path = None
        if os.path.exists(client_dir):
            for fname in os.listdir(client_dir):
                if fname.endswith(".xlsx"):
                    excel_path = os.path.join(client_dir, fname)
                    break
        if not excel_path:
            excel_path = "Loopbaan onderzoek 5.0 template.xlsx"
        content_frame.results_excel_path = excel_path
    
    build_func(content_frame, navigate_phase)

def open_phase11_assessment(client):
    """Start the assessment questionnaire for a client."""
    global current_assessment_client
    current_assessment_client = client
    # Always set on content_frame as well
    try:
        content_frame.current_assessment_client = client
    except Exception:
        pass
    navigate_phase("phase1.1")

root.mainloop()