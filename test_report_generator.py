# test_report_generator.py

from report_generator import generate_report

if __name__ == "__main__":

    test_data = {
        "name": "Test User",
        "age": 23,

        "bigfive": {
            "Extraversie": "neutral",
            "Openheid": "high"
        },

        "loopbaanankers": [
            "OMHOOG_KOMEN",
            "VEILIG_VOELEN"
        ],

        "carriereclusters": [
            "EDUCATIE",
            "ARCHITECTUUR"            
        ],

        "cultures": [
            "INNOVATIEVE",
            "RESULTAATGERICHTE"            
        ],

        "jcm": {
            "Taakvaardigheid": "Here for the sake of testing I'm writing some text.",
            "Taakidentiteit": "I am doing the same thing here.",
            "Taakbetekenis": "3.14518, ok fully messed it up its 3.14159. But i mean i was kinda close.",
            "Autonomie": "What else can i remember without checking? Not much i don't think.",
            "Feedback": "How about some binary? 1, 2, 4, 8, 16, 32, 64, 128. I think that's it? Let me go check. Ok i was correct, that's nice. Is the fibanacchi number the same type? Ok first of all i knew i typed it wrong, its Fibonacci sequence but okay. And it is not the same thing at all. It's 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 etc. It is a similar thing in my head. Binary is just taking the number and times two, so 1+1=2, 2+2=4, 4+4=8, 8+8=16, and so on until 128. Fibonacci sequence is similar in my head. Just adding the two last numbers together, 1+1=2, 1+2=3, 2+3=5, 3+5=8, 5+8=13, 8+13=21 and so on. It's kinda similar, for me at least.  "
        }
    }

    generate_report(test_data, "test_report.docx")
    print("Report generated successfully!")