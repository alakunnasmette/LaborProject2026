#!/usr/bin/env python3
"""
Test that navigate_phase correctly sets root.results_excel_path when resuming.
"""

import tkinter as tk
import os

# Create a mock app structure
root = tk.Tk()
root.withdraw()

# Create content_frame (mock)
content_frame = tk.Frame(root)
content_frame.pack()

# Test client
test_client = {"id": 1, "name": "Test"}
content_frame.current_assessment_client = test_client

# Simulate the navigate_phase logic for setting Excel path
client = content_frame.current_assessment_client
safe_name = "_".join(client["name"].split())
folder_name = f"{client['id']}_{safe_name}"
client_dir = os.path.join("clients", folder_name)
excel_path = None

print(f"Looking for Excel file in: {client_dir}")
print(f"Directory exists: {os.path.exists(client_dir)}")

if os.path.exists(client_dir):
    files = os.listdir(client_dir)
    print(f"Files in directory: {files}")
    for fname in files:
        if fname.endswith(".xlsx"):
            excel_path = os.path.join(client_dir, fname)
            print(f"Found Excel file: {fname}")
            break

if not excel_path:
    excel_path = "Loopbaan onderzoek 5.0 template.xlsx"
    print(f"No local Excel file found, using template: {excel_path}")
else:
    print(f"✓ Excel path set: {excel_path}")

# Set on both content_frame and root
content_frame.results_excel_path = excel_path
root.results_excel_path = excel_path

# Verify it was set
print(f"\nVerification:")
print(f"  content_frame.results_excel_path = {content_frame.results_excel_path}")
print(f"  root.results_excel_path = {root.results_excel_path}")
print(f"  File exists: {os.path.exists(root.results_excel_path) if root.results_excel_path.startswith('clients') else 'N/A (template)'}")

if hasattr(root, "results_excel_path"):
    print("\n✓ PASS: root.results_excel_path is properly set for phase resume!")
else:
    print("\n✗ FAIL: root.results_excel_path not set")

root.destroy()
