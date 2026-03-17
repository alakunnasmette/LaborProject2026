from utils.read_results_from_excel import read_results_from_excel
from report_generator import generate_report

def generate_report_from_excel(excel_file, age=30):
    """
    Reads Excel results, adds a dummy age, and generates Word report.
    """
    user_data = read_results_from_excel(excel_file)
    user_data["age"] = age  # dummy age

    report_file = excel_file.replace(".xlsx", "_report.docx")
    generate_report(user_data, report_file)
    return report_file