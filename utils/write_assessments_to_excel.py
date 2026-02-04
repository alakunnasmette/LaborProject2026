import openpyxl
import os
import shutil
from datetime import datetime


def write_assessment_answers_to_excel(
    assessment_results: dict,
    excel_path: str = "Loopbaan onderzoek 5.0 template.xlsx",
) -> str | bool:
    """Write Big Five answers into a copy of the Excel template.

    Mapping: Q1→C4, Q2→D5, Q3→E6, Q4→F7, Q5→G8, Q6→C9, ... (cycle C-G every 5).
    Returns the path to the saved file on success, otherwise False.
    """
    try:
        if not os.path.exists(excel_path):
            print(f"Error: Excel file not found at {excel_path}")
            return False

        folder = os.path.dirname(excel_path) or "."
        filled_dir = os.path.join(folder, "results")
        base_name = os.path.splitext(os.path.basename(excel_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_name = f"{base_name} - filled {timestamp}.xlsx"
        new_path = os.path.join(filled_dir, new_name)
        shutil.copy2(excel_path, new_path)

        wb = openpyxl.load_workbook(new_path)
        ws = wb.worksheets[1]

        cols = [3, 4, 5, 6, 7]
        for item_num in sorted(assessment_results.keys()):
            val = assessment_results[item_num]
            pos = (item_num - 1) % 5
            cycle = (item_num - 1) // 5
            col = cols[pos]
            row = 4 + cycle * 5 + pos
            ws.cell(row=row, column=col, value=val)

        wb.save(new_path)
        return new_path

    except Exception as e:
        print(f"Error writing to Excel: {e}")
        return False

#could be removed
def write_loopbaan_answers_to_excel(loopbaan_results: dict, excel_path: str = "Loopbaan onderzoek 5.0 template.xlsx") -> str | bool:
    """Copy template into `resultaten` and return the path; caller may write cells."""
    if not os.path.exists(excel_path):
        return False
    folder = os.path.dirname(excel_path) or "."
    filled_dir = os.path.join(folder, "results")
    base_name = os.path.splitext(os.path.basename(excel_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_name = f"{base_name} - filled {timestamp}.xlsx"
    new_path = os.path.join(filled_dir, new_name)
    shutil.copy2(excel_path, new_path)
    return new_path
