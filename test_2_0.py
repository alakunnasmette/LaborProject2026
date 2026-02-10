print("Starting Phase 2.0 test script...")

from write_assessments_to_excel import (
    open_existing_results_excel,
    write_phase_2_0,
)

# Path to the Excel file created by Phase 1.1
excel_path = r"C:\Git\labor-project2026\results\Loopbaan onderzoek 5.0 template - filled 20260203-085934.xlsx"

# Fake test answers for Phase 2.2
answers_2_0 = [
    1, 2, 3, 4,
    2, 1, 4, 3,
    3, 2, 1, 4,
    4, 3, 2, 1
]

# Open the existing Excel file on sheet 2.2
wb, ws = open_existing_results_excel(excel_path, "2.0")

# Safety check
if wb is None or ws is None:
    print("Failed to open Excel file")
    exit()

# Write Phase 2.2 answers
write_phase_2_0(ws, answers_2_0)

# Save the same file
wb.save(excel_path)

print("Phase 2.0 test completed")
