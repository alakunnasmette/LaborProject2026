from utils.score_calculations import calculate_scores
from report_generator import generate_report
from text_library import static_texts, personality_texts, carriereclusters_texts, cultuuranalyse_texts, loopbaanankers_texts

def generate_report_from_answers(all_answers, age=30, filename="results_report.docx"):
    """
    Converts calculated scores to user_data and generates the Word report.
    """
    report_data = calculate_scores(all_answers)
    report_data["age"] = age

    user_data = {
        "bigfive": {},
        "loopbaanankers": [],
        "carriereclusters": [],
        "cultures": [],
        "jcm": report_data.get("phase2.3", {}),
        "age": age
    }


    # Phase 1.1 - Big Five ----------------------------------------

    for trait, score in report_data.get("phase1.1", {}).items():
        level = "neutral"
        if score >= 20:
            level = "high"
        elif score <= 10:
            level = "low"
        user_data["bigfive"][trait] = {
            "score": score,
            "total": 30,
            "level": level
        }


    # Phase 2.0 - Loopbaanankers ----------------------------------------

    anchors_dict = report_data.get("phase2.0", {})
    top_anchors = sorted(anchors_dict.items(), key=lambda x: x[1], reverse=True)
    user_data["loopbaanankers"] = [k for k,_ in top_anchors[:2]]


    # Phase 2.1 - Carrièreclusters top 2  ----------------------------------------

    clusters_dict = report_data.get("phase2.1", {})
    top_clusters = sorted(clusters_dict.items(), key=lambda x: x[1], reverse=True)
    user_data["carriereclusters"] = [k for k,_ in top_clusters[:2]]


    # Phase 2.2 - Cultuur top 2 ----------------------------------------

    cultures_dict = report_data.get("phase2.2", {})
    top_cultures = sorted(cultures_dict.items(), key=lambda x: x[1], reverse=True)
    user_data["cultures"] = [k for k,_ in top_cultures[:2]]


    # DEBUG

    print("--- DEBUG user_data prepared for report ---")
    for k,v in user_data.items():
        print(f"{k}: {v}")


    # Generate Word report ----------------------------------------

    generate_report(user_data, filename)
    return filename