# report_generator.py

from docx import Document
from text_library import (
    static_texts,
    loopbaanfase_texts,
    personality_texts,
    loopbaanankers_texts,
    carriereclusters_texts,
    cultuuranalyse_texts
)


# mappings for dynamic text

JCM_MAPPING = {
    "Taakvaardigheid": ("SKILL_VARIETY_TITLE", "SKILL_VARIETY_TEXT"),
    "Taakidentiteit": ("TASK_IDENTITY_TITLE", "TASK_IDENTITY_TEXT"),
    "Taakbetekenis": ("TASK_SIGNIFICANCE_TITLE", "TASK_SIGNIFICANCE_TEXT"),
    "Autonomie": ("AUTONOMY_TITLE", "AUTONOMY_TEXT"),
    "Feedback": ("FEEDBACK_TITLE", "FEEDBACK_TEXT"),
}


BIGFIVE_MAPPING = {
    "Extraversie": "Extraversie",
    "Altruisme": "Altruisme",
    "Conscientieusheid": "Conscientieusheid",
    "Neuroticisme": "Neuroticisme",
    "Openheid": "Openheid"
}



# -------------------- Main report generator --------------------

def generate_report(user_data, filename):
    doc = Document()

    add_loopbaanfase_section(doc, user_data)
    add_bigfive_section(doc, user_data)
    add_loopbaanankers_section(doc, user_data)
    add_carriereclusters_section(doc, user_data)
    add_cultuur_section(doc, user_data)
    add_jcm_section(doc, user_data)

    doc.save(filename)



# Loopbaanfase
def add_loopbaanfase_section(doc, user_data):
    doc.add_heading(static_texts.LOOPBAANFASE_SECTION_TITLE, level=1)
    doc.add_paragraph(static_texts.LOOPBAANFASE_INTRO_TEXT)

    age = user_data.get("age", 0)
    if 17 <= age <= 21:
        text = loopbaanfase_texts.LOOPBAANFASE_17_21
    elif 22 <= age <= 28:
        text = loopbaanfase_texts.LOOPBAANFASE_22_28
    elif 29 <= age <= 33:
        text = loopbaanfase_texts.LOOPBAANFASE_29_33
    elif 34 <= age <= 40:
        text = loopbaanfase_texts.LOOPBAANFASE_34_40
    elif 41 <= age <= 45:
        text = loopbaanfase_texts.LOOPBAANFASE_41_45
    elif 46 <= age <= 64:
        text = loopbaanfase_texts.LOOPBAANFASE_46_64
    else:
        text = loopbaanfase_texts.LOOPBAANFASE_60_OLDER

    doc.add_paragraph(text)


# Big Five
def add_bigfive_section(doc, user_data):
    doc.add_heading(static_texts.PHASE1_1_SECTION_TITLE, level=1)
    doc.add_paragraph(static_texts.PHASE1_1_INTRO_TEXT)

    bigfive_data = user_data.get("bigfive", {})

    for trait, key in BIGFIVE_MAPPING.items():
        doc.add_heading(getattr(static_texts, f"PHASE1_1_{key.upper()}_TITLE").strip(), level=2)

        score = bigfive_data.get(trait, "neutral").lower()
        trait_text = personality_texts.BIGFIVE_TEXTS[key].get(score, "")
        doc.add_paragraph(trait_text.strip())



# Loopbaanankers
def add_loopbaanankers_section(doc, user_data):
    doc.add_heading(static_texts.PHASE2_0_SECTION_TITLE, level=1)
    doc.add_paragraph(static_texts.PHASE2_0_INTRO_TEXT)

    anchors = user_data.get("loopbaanankers", [])
    for i, anchor in enumerate(anchors[:2], 1):
        title = getattr(static_texts, f"PHASE2_0_HOOGSTE_SCORE_{i}_TITLE")
        text = getattr(loopbaanankers_texts, f"LOOPBAANANKERS_{anchor}")
        doc.add_heading(title.strip(), level=2)
        doc.add_paragraph(text.strip())



# Carrière Clusters
def add_carriereclusters_section(doc, user_data):
    doc.add_heading(static_texts.PHASE2_1_SECTION_TITLE, level=1)
    doc.add_paragraph(static_texts.PHASE2_1_INTRO_TEXT)

    clusters = user_data.get("carriereclusters", [])
    for i, cluster in enumerate(clusters[:2], 1):
        title = getattr(static_texts, f"PHASE2_1_HOOGSTE_SCORE_{i}_TITLE")
        text = getattr(carriereclusters_texts, f"CARRIER_CLUSTERS_{cluster}")
        doc.add_heading(title.strip(), level=2)
        doc.add_paragraph(text.strip())


# Cultuur Analyse
def add_cultuur_section(doc, user_data):
    doc.add_heading(static_texts.PHASE2_2_SECTION_TITLE, level=1)
    doc.add_paragraph(static_texts.PHASE2_2_INTRO_TEXT)

    cultures = user_data.get("cultures", [])
    for i, culture in enumerate(cultures[:2], 1):
        title = getattr(static_texts, f"PHASE2_2_HOOGSTE_SCORE_{i}_TITLE")
        text = getattr(cultuuranalyse_texts, f"CULTUUR_ANALYSE_{culture}")
        doc.add_heading(title.strip(), level=2)
        doc.add_paragraph(text.strip())


# JCM
def add_jcm_section(doc, user_data):
    doc.add_heading(static_texts.PHASE2_3_SECTION_TITLE.strip(), level=1)
    doc.add_paragraph(static_texts.PHASE2_3_INTRO_TEXT.strip())

    jcm_data = user_data.get("jcm", {})

    # definitions
    for attr, (title_var, text_var) in JCM_MAPPING.items():

        title = getattr(static_texts, f"PHASE2_3_{title_var}")
        explanation = getattr(static_texts, f"PHASE2_3_{text_var}")

        # bold title
        p = doc.add_paragraph()
        run = p.add_run(title.strip())
        run.bold = True

        doc.add_paragraph(explanation.strip())


    # user answers
    for attr, answer in jcm_data.items():

        p = doc.add_paragraph()
        run = p.add_run(attr)
        run.bold = True

        doc.add_paragraph(answer.strip())