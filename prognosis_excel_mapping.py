"""
Excel mapping for Prognosis Model
--------------------------------

Structure:

Each question maps to:
- row: Excel row containing answer percentages
- options: number of selectable options (columns D–P)
- dropdown_column: where selected value should be written

Columns:
C = question text
D–P = percentage options
Q = dropdown selection output
"""



"""
Column logic example:

option_index = 0 → column D
option_index = 1 → column E
option_index = 2 → column F

Implementation example:

column_letter = chr(ord("D") + option_index)
"""

PROGNOSIS_MAPPING = {

    "q1": {
        "depends_on": "gender",
        "man": {
            "row": 3,
            "options": 3
        },
        "woman": {
            "row": 20,
            "options": 3
        }
    },

    "q3": {"row": 37, "options": 3},

    "q4": {"row": 39, "options": 11},

    "q5": {"row": 41, "options": 3},

    "q6": {"row": 45, "options": 5},

    "q7": {"row": 48, "options": 5},

    "q8": {"row": 52, "options": 4},

    "q9": {"row": 68, "options": 5},

    "q10": {"row": 70, "options": 3},

    "q11": {"row": 74, "options": 3},

# i dont know why but in the excel sheet there are two question 12. i just put them here as they are idk man

    "q12": {"row": 76, "options": 5},

    "q12": {"row": 78, "options": 5},

    "q13": {"row": 80, "options": 5},

    "q14": {"row": 82, "options": 3},

    "q15": {"row": 84, "options": 2},

    "q16": {"row": 87, "options": 4},

    "q17": {"row": 90, "options": 3},

    "q18": {"row": 93, "options": 3},

    "q19": {"row": 95, "options": 3},

    "q20": {"row": 97, "options": 4},

    "q21": {"row": 100, "options": 3},

    "q22": {"row": 103, "options": 3},

    "q23": {"row": 106, "options": 3},

    "q24": {"row": 109, "options": 3},

    "q25": {
        "depends_on": "gender",
        "man": {
            "row": 113,
            "options": 4
        },
        "woman": {
            "row": 116,
            "options": 4
        }
    },

    "q26": {"row": 119, "options": 4},

    "q27": {"row": 122, "options": 3},

    "q28": {"row": 125, "options": 6},

}


DROPDOWN_COLUMN = "Q"
OPTIONS_START_COLUMN = "D"