import openpyxl
import os
import shutil
from datetime import datetime


def create_or_update_assessment_file(
    excel_path: str = "Loopbaan onderzoek 5.0 template.xlsx",
    is_first_save: bool = True,
    timestamp: str = None,
) -> str | bool:
    """Create a new assessment file or return path to existing one.
    
    If is_first_save=True, creates a copy of the template with a timestamp.
    If is_first_save=False, returns the path (file should already exist).
    Returns the path to the assessment file, or False on error.
    """
    try:
        if not os.path.exists(excel_path):
            print(f"Error: Excel template not found at {excel_path}")
            return False
        
        folder = os.path.dirname(excel_path) or "."
        filled_dir = os.path.join(folder, "results")
        
        # Ensure results directory exists
        os.makedirs(filled_dir, exist_ok=True)
        
        if is_first_save:
            if timestamp is None:
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            base_name = os.path.splitext(os.path.basename(excel_path))[0]
            new_name = f"{base_name} - filled {timestamp}.xlsx"
            new_path = os.path.join(filled_dir, new_name)
            shutil.copy2(excel_path, new_path)
            return new_path
        else:
            # Just return path (caller will open/update existing file)
            return True
            
    except Exception as e:
        print(f"Error creating assessment file: {e}")
        return False


def write_assessment_answers_to_excel(
    assessment_results: dict,
    excel_path: str = "Loopbaan onderzoek 5.0 template.xlsx",
) -> str | bool:
    """Write Big Five answers into a copy of the Excel template.

    Mapping: Q1→C4, Q2→D5, Q3→E6, Q4→F7, Q5→G8, Q6→C9, ... (cycle C-G every 5).
    Returns the path to the saved file on success, otherwise False.
    """
    try:
        template_path = excel_path
        if not os.path.exists(template_path):
            print(f"Error: Excel file not found at {template_path}")
            return False

        folder = os.path.dirname(template_path) or "."
        filled_dir = os.path.join(folder, "results")
        os.makedirs(filled_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(template_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_name = f"{base_name} - filled {timestamp}.xlsx"
        new_path = os.path.join(filled_dir, new_name)
        shutil.copy2(template_path, new_path)

        wb = openpyxl.load_workbook(new_path)
        ws = wb.worksheets[1]  # Sheet: "Fase 1.1 | Big Five Dimensies"

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


def add_career_anchors_to_excel(excel_file_path: str, career_results: dict) -> bool:
    """Add career anchor scores to existing assessment Excel file.
    
    Args:
        excel_file_path: Path to the filled assessment Excel file
        career_results: Dict of {row_id: anchor_letter} where anchor_letter is V, W, X, Y, or Z
    
    Returns:
        True on success, False on error.
    """
    try:
        if not os.path.exists(excel_file_path):
            print(f"Error: Excel file not found at {excel_file_path}")
            return False
        
        wb = openpyxl.load_workbook(excel_file_path)
        
        # Find the sheet "Fase 2.0 | Loopbaanankers"
        sheet_name = "Fase 2.0 | Loopbaanankers"
        if sheet_name not in wb.sheetnames:
            print(f"Error: Sheet '{sheet_name}' not found in workbook")
            return False
        
        ws = wb[sheet_name]

        # Map each anchor letter to a column in the sheet
        anchor_cols = {"V": 3, "W": 4, "X": 5, "Y": 6, "Z": 7}

        # Import the statement texts from phase20 to locate exact rows
        try:
            from phases.phase20 import CAREER_STATEMENTS
        except Exception:
            CAREER_STATEMENTS = None

        for row_id, anchor_letter in career_results.items():
            if anchor_letter not in anchor_cols:
                continue
            col = anchor_cols[anchor_letter]

            excel_row = None
            # Try to locate the statement text in column B
            if CAREER_STATEMENTS and 1 <= row_id <= len(CAREER_STATEMENTS):
                _, _, stmt_text = CAREER_STATEMENTS[row_id - 1]
                snippet = stmt_text.strip()[:40]
                for r in range(4, ws.max_row + 1):
                    cell = ws.cell(row=r, column=2).value
                    if cell and snippet in str(cell):
                        excel_row = r
                        break

            # Fallback: assume sequential rows starting at row 4
            if excel_row is None:
                excel_row = row_id + 3

            ws.cell(row=excel_row, column=col, value=1)
        
        wb.save(excel_file_path)
        return True
        
    except Exception as e:
        print(f"Error adding career anchors to Excel: {e}")
        return False


def add_career_clusters_to_excel(excel_file_path: str, cluster_scores: dict) -> bool:
    """Add career cluster scores to existing assessment Excel file.
    
    Args:
        excel_file_path: Path to the filled assessment Excel file
        cluster_scores: Dict of {cluster_id: {"act": int, "comp": int, "edu": int}}
    
    Returns:
        True on success, False on error.
    """
    try:
        if not os.path.exists(excel_file_path):
            print(f"Error: Excel file not found at {excel_file_path}")
            return False
        
        wb = openpyxl.load_workbook(excel_file_path)
        
        # Find the sheet "Fase 2.1 | Carriere Clusters"
        sheet_name = "Fase 2.1 | Carriere Clusters"
        if sheet_name not in wb.sheetnames:
            print(f"Error: Sheet '{sheet_name}' not found in workbook")
            return False
        
        ws = wb[sheet_name]

        # Write cluster scores. The sheet layout groups each cluster in a block
        # starting with the cluster id in column A; below that the activities/competences
        # and then a totals row which contains formulas (we will replace those with values).
        for cluster_id, scores in cluster_scores.items():
            act_score = scores.get("act", 0)
            comp_score = scores.get("comp", 0)
            edu_score = scores.get("edu", 0)
            total_score = act_score + comp_score + edu_score

            # Find the cluster start row by searching column A for cluster_id
            start_row = None
            for r in range(4, ws.max_row + 1):
                cell = ws.cell(row=r, column=1).value
                if cell == cluster_id:
                    start_row = r
                    break

            if start_row is None:
                # Could not find cluster; skip
                continue

            # Look for the totals/formula row within the next 12 rows
            total_row = None
            for r in range(start_row, min(start_row + 15, ws.max_row + 1)):
                cval = ws.cell(row=r, column=3).value
                if isinstance(cval, str) and cval.strip().startswith('='):
                    total_row = r
                    break

            # Fallback: assume totals row is start_row + 7
            if total_row is None:
                total_row = start_row + 7

            # Write the aggregated scores into the totals cells (columns C, E, G)
            ws.cell(row=total_row, column=3, value=act_score)
            ws.cell(row=total_row, column=5, value=comp_score)
            ws.cell(row=total_row, column=7, value=edu_score)
        
        wb.save(excel_file_path)
        return True
        
    except Exception as e:
        print(f"Error adding career clusters to Excel: {e}")
        return False


#could be removed
def write_loopbaan_answers_to_excel(loopbaan_results: dict, excel_path: str = "Loopbaan onderzoek 5.0 template.xlsx") -> str | bool:
    """Copy template into `resultaten` and return the path; caller may write cells."""
    if not os.path.exists(excel_path):
        return False
    folder = os.path.dirname(excel_path) or "."
    filled_dir = os.path.join(folder, "results")
    os.makedirs(filled_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(excel_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_name = f"{base_name} - filled {timestamp}.xlsx"
    new_path = os.path.join(filled_dir, new_name)
    shutil.copy2(excel_path, new_path)
    return new_path
