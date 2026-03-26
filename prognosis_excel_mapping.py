# explanation i guess:
# a few questions have different outcomes based on genders
# so question 1, if youre a man, the answer row is 3, if youre a woman, the answer row is 20
# all the others work this way:
# "q3": {"row": 37, "options": 3}, means question 3 is on row 37 and has 3 options, meaning column D, E, and F
# different question have different amount of options, but they all start at column D
# the most amount is 12, i think?
# drop down menu for the answers is on column Q
# basically the logic is that in the questionnaire, all the choices connect to a specific cell. option 1 = D, option 2 = E etc.
# the program will read what percentage is in the cell for that answer, so like D3 in the excel is 33.33%
# it will then take that number and write it down on to the answer cell, which would be Q3.
# the number in the cells might change in the future, since its based on statistics, so the python script should NOT have any percentages.
# it just reads the cell itself.
# it's not as complicated as it sounds, it's just tedious and annoying, but you'll survive.
# Good luck with the project!
# ❤ Mette

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

    "q29": {"row": 127, "options": 3},

    "q30": {"row": 129, "options": 3},

    "q31": {"row": 131, "options": 3},

    "q32": {"row": 133, "options": 3},

    "q33": {"row": 135, "options": 3},

    "q34": {"row": 137, "options": 3},

    "q35": {"row": 140, "options": 4},

    "q36": {"row": 143, "options": 4},

    "q37": {"row": 146, "options": 2},

    "q38": {"row": 148, "options": 2},

    "q39": {"row": 150, "options": 2},

    "q40": {"row": 152, "options": 4},

}


DROPDOWN_COLUMN = "Q"
OPTIONS_START_COLUMN = "D"