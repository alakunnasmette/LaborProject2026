# LABOR Arbeidsmarktintegratie - Modular Program
LABOR's modular program is a local Python/Tkinter application designed to streamline assessments and generate prognosis reports. The application allows users to complete various assessments, automatically calculate scores, and produce a clear report with percentages, results, and conclusions. All data is stored locally within the file explorer.

## Technologies

### Core language
- Python

### UI framework
- Tkinter
- Custom UI component layer `ui_components.py`
- Centralized styling layer `ui_styles.py`

### Data processing
- Pandas

### File I/O (Input/Output)
- OpenPyXL
- xlrd

### Platform integration
- pywin32

### Media
- Pillow

## Getting started

### Prerequisites

Ensure that [Python](https://www.python.org/downloads/) is installed on your system.

### Installation

1. **Open VSCode and open the GitHub folder**  
   Ensure you open the root `/GitHub` folder so that project paths work correctly.
   
2. **Clone the repository**  
   In the VSCode terminal, run:
   ```powershell
   git clone https://github.com/FlyyLee/labor-project2026
   cd labor-project2026
   ```

3. **Create a virtual environment**
   ```powershell
   python -m venv .venv
   ```
   This creates a `.venv` folder in the project root.

4. **Activate the virtual environment**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
     The terminal prompt should now show `(.venv)`.

5. **Select the virtual environment in VSCode**
   Press `Ctrl+Shift+P ` → `Python: Select Interpreter` → choose `.venv` interpreter (`.venv\Scripts\python.exe`).

6. **Upgrade pip (optional)**
   ```powershell
   python -m pip install --upgrade pip
   ```

7. **Install dependencies**
   ```powershell
   pip install --upgrade --force-reinstall -r requirements.txt
   ```

8. **Run the application**
   ```powershell
   python app.py
   ```
   The Tkinter application window should open.
