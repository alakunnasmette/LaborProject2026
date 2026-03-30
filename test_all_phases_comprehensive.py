#!/usr/bin/env python3
"""
Comprehensive test verifying all phases save/load data correctly.
"""

import tkinter as tk
import os
import json
from utils.session_manager import save_session, load_session, mark_session_complete
from collections import defaultdict
from phases.phase20 import CAREER_STATEMENTS
from phases.phase22 import GROUPS

# Create a root window
root = tk.Tk()
root.withdraw()

# Test data
test_client = {"id": 999, "name": "TestClient_AllPhases"}
client_id = str(test_client["id"])
client_name = test_client["name"]

print("=" * 60)
print("COMPREHENSIVE PHASE PERSISTENCE TEST")
print("=" * 60)

# ============ PHASE 2.0 TEST ============
print("\n[PHASE 2.0] Testing Career Anchors auto_save...")
try:
    questions = defaultdict(list)
    for nummer, anker, tekst in CAREER_STATEMENTS:
        questions[nummer].append((anker, tekst))
    
    vraag_vars = {}
    for nummer in questions.keys():
        var = tk.StringVar(value="")
        vraag_vars[nummer] = var
    
    # Simulate user input
    for nummer in range(1, 31):
        vraag_vars[nummer].set("V" if nummer % 2 == 0 else "W")
    
    # Simulate auto_save
    answers_to_save = {str(k): v.get() for k, v in vraag_vars.items()}
    save_session(client_id, client_name, "phase2.0", 0, answers_to_save, len(questions))
    
    # Load and verify
    loaded = load_session(client_id, client_name, "phase2.0")
    if loaded and loaded["answers"] == answers_to_save:
        print("  ✓ PASS: Phase 2.0 save/load works correctly")
    else:
        print("  ✗ FAIL: Phase 2.0 data mismatch")
except Exception as e:
    print(f"  ✗ FAIL: {e}")

# ============ PHASE 2.1 TEST ============
print("\n[PHASE 2.1] Testing Career Clusters auto_save...")
try:
    vars_2_1 = {}
    cluster_keys = [("CC01", 0), ("CC01", 1), ("CC02", 0)]
    
    for key in cluster_keys:
        main_var = tk.IntVar(value=0)
        skill_var = tk.IntVar(value=0)
        interest_var = tk.IntVar(value=1)
        vars_2_1[key] = (main_var, skill_var, interest_var)
    
    # Simulate auto_save
    answers_to_save_2_1 = {}
    for key, var_tuple in vars_2_1.items():
        main_var, skill_var, interest_var = var_tuple
        answers_to_save_2_1[str(key)] = [
            int(main_var.get()),
            int(skill_var.get()),
            int(interest_var.get())
        ]
    
    save_session(client_id, client_name, "phase2.1", 0, answers_to_save_2_1, len(vars_2_1))
    
    # Load and verify
    loaded = load_session(client_id, client_name, "phase2.1")
    if loaded and loaded["answers"] == answers_to_save_2_1:
        print("  ✓ PASS: Phase 2.1 save/load works correctly")
    else:
        print("  ✗ FAIL: Phase 2.1 data mismatch")
except Exception as e:
    print(f"  ✗ FAIL: {e}")

# ============ PHASE 2.2 TEST ============
print("\n[PHASE 2.2] Testing Culture auto_save...")
try:
    vars_2_2 = {}
    culture_keys = [("G001", 0), ("G001", 1), ("G002", 0), ("G002", 1)]
    
    for key in culture_keys:
        var = tk.StringVar(value="3")
        vars_2_2[key] = var
    
    # Simulate auto_save
    answers_to_save_2_2 = {}
    for (gid, i), var in vars_2_2.items():
        value = var.get().strip()
        if value:
            answers_to_save_2_2[str((gid, i))] = value
    
    save_session(client_id, client_name, "phase2.2", 0, answers_to_save_2_2, 16)
    
    # Load and verify
    loaded = load_session(client_id, client_name, "phase2.2")
    if loaded and loaded["answers"] == answers_to_save_2_2:
        print("  ✓ PASS: Phase 2.2 save/load works correctly")
    else:
        print("  ✗ FAIL: Phase 2.2 data mismatch")
except Exception as e:
    print(f"  ✗ FAIL: {e}")

# ============ PHASE 2.3 TEST ============
print("\n[PHASE 2.3] Testing Job Characteristics auto_save...")
try:
    # Simulate text entries
    text_entries = {}
    for q_num in range(1, 6):
        text_var = tk.Text(root, height=4, width=80)
        text_var.insert("1.0", f"Answer to question {q_num}")
        text_entries[q_num] = text_var
    
    # Simulate auto_save
    answers_to_save_2_3 = {}
    for qn, tb in text_entries.items():
        answer = tb.get("1.0", "end-1c").strip()
        if answer:
            answers_to_save_2_3[str(qn)] = answer
    
    save_session(client_id, client_name, "phase2.3", 0, answers_to_save_2_3, 5)
    
    # Load and verify
    loaded = load_session(client_id, client_name, "phase2.3")
    if loaded and loaded["answers"] == answers_to_save_2_3:
        print("  ✓ PASS: Phase 2.3 save/load works correctly")
    else:
        print("  ✗ FAIL: Phase 2.3 data mismatch")
except Exception as e:
    print(f"  ✗ FAIL: {e}")

# ============ MARK COMPLETE TEST ============
print("\n[COMPLETION] Testing mark_session_complete...")
try:
    mark_session_complete(client_id, client_name, "phase2.0")
    
    # Verify it's marked complete
    loaded = load_session(client_id, client_name, "phase2.0")
    if loaded and loaded["status"] == "completed":
        print("  ✓ PASS: mark_session_complete works correctly")
    else:
        print("  ✗ FAIL: Status not marked as completed")
except Exception as e:
    print(f"  ✗ FAIL: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

root.destroy()
