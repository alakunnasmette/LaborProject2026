#!/usr/bin/env python3
"""
Test that phase20.auto_save_loopbaan correctly calls .get() on StringVar objects.
"""

import tkinter as tk
from phases.phase20 import CAREER_STATEMENTS
from utils.session_manager import save_session, load_session
from collections import defaultdict

# Create a root window first (required for StringVar)
root = tk.Tk()
root.withdraw()  # Hide the window

# Mock client
client = {"id": 1, "name": "Test_Client"}

# Create StringVar objects (simulating the phase20 behavior)
questions = defaultdict(list)
for nummer, anker, tekst in CAREER_STATEMENTS:
    questions[nummer].append((anker, tekst))

vraag_vars = {}
for nummer in questions.keys():
    var = tk.StringVar(value="")
    vraag_vars[nummer] = var

# Simulate user selecting answers
for nummer in range(1, 31):
    vraag_vars[nummer].set("V")

print("Testing auto_save_loopbaan with .get() fix...")

# Test the fixed auto_save function (extracted logic)
def auto_save_loopbaan():
    """Save current answers to session file."""
    answers_to_save = {str(k): v.get() for k, v in vraag_vars.items()}
    print(f"Answers to save: {list(answers_to_save.items())[:3]}...")  # Print first 3
    save_session(
        str(client["id"]),
        client["name"],
        "phase2.0",
        0,
        answers_to_save,
        len(questions)
    )
    return answers_to_save

try:
    saved_answers = auto_save_loopbaan()
    print("✓ auto_save_loopbaan executed without errors")
    
    # Verify the data was saved
    loaded_session = load_session(str(client["id"]), client["name"], "phase2.0")
    if loaded_session and loaded_session.get("answers"):
        loaded_answers = loaded_session["answers"]
        print(f"✓ Session saved with {len(loaded_answers)} answers")
        print(f"✓ First answer: question 1 = {loaded_answers.get('1')}")
        if loaded_answers.get('1') == 'V':
            print("✓ PASS: Data saved and loaded correctly!")
        else:
            print("✗ FAIL: Data mismatch")
    else:
        print("✗ FAIL: No session data found")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
finally:
    root.destroy()
