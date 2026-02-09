import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.write_assessments_to_excel import write_assessment_answers_to_excel




title = tk.Label(
        scroll_frame,
        text="Fase 2.3 – Werk karakteristieken modellen",
        bg="white",
        fg="black",
        font=("Segoe UI", 14, "bold"),
        anchor="w",
    )
title.pack(fill="x", padx=20, pady=(15, 5))

subtitle = tk.Label(
        scroll_frame,
        text=(
            "Beoordeel elke stelling in het algemeen voor jezelf.\n"
            "1 = oneens · 2 = deels oneens · 3 = neutraal · 4 = deels eens · 5 = volledig eens."
        ),
        bg="white",
        fg="black",
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    )
subtitle.pack(fill="x", padx=20, pady=(0, 15))