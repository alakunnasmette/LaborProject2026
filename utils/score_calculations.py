
def calculate_scores(all_answers):
    """
    Calculate total scores for all phases from raw answers.

    Returns a dict structured for report_helper.py
    """
    report_data = {}


    # Phase 1.1 - Big Five ----------------------------------------

    p11 = all_answers.get("phase1.1", {})
    report_data["phase1.1"] = {
        "Extraversie": (
            20 + p11.get(1,0) - p11.get(6,0) + p11.get(11,0) - p11.get(16,0)
            + p11.get(21,0) - p11.get(26,0) + p11.get(31,0) - p11.get(36,0)
            + p11.get(41,0) - p11.get(46,0)
        ),
        "Altruisme": (
            14 - p11.get(2,0) + p11.get(7,0) - p11.get(12,0) + p11.get(17,0)
            - p11.get(22,0) + p11.get(27,0) - p11.get(32,0) + p11.get(37,0)
            + p11.get(42,0) + p11.get(47,0)
        ),
        "Conscientieusheid": (
            14 + p11.get(3,0) - p11.get(8,0) + p11.get(13,0) - p11.get(18,0)
            + p11.get(23,0) - p11.get(28,0) + p11.get(33,0) - p11.get(38,0)
            + p11.get(43,0) + p11.get(48,0)
        ),
        "Neuroticisme": (
            38 - p11.get(4,0) + p11.get(9,0) - p11.get(14,0) + p11.get(19,0)
            - p11.get(24,0) - p11.get(29,0) - p11.get(34,0) - p11.get(39,0)
            - p11.get(44,0) - p11.get(49,0)
        ),
        "Openheid": (
            8 + p11.get(5,0) - p11.get(10,0) + p11.get(15,0) - p11.get(20,0)
            + p11.get(25,0) - p11.get(30,0) + p11.get(35,0) + p11.get(40,0)
            + p11.get(45,0) + p11.get(50,0) + p11.get(51,0)
        ),
    }


    # Phase 2.0 - Loopbaanankers ----------------------------------------

    p20 = all_answers.get("phase2.0", {})  # dict of question #: letter
    anchor_mapping = {
        "V": "OMHOOG_KOMEN",
        "W": "VEILIG_VOELEN",
        "X": "VRIJ_ZIJN",
        "Y": "BALANS_VINDEN",
        "Z": "UITDAGING_ZOEKEN"
    }
    anchors_count = {}
    for val in p20.values():
        if val in anchor_mapping:
            key = anchor_mapping[val]
            anchors_count[key] = anchors_count.get(key, 0) + 1
    report_data["phase2.0"] = anchors_count


    # Phase 2.1 - Carrièreclusters ----------------------------------------

    cluster_id_map = {
        1: "MILIEU", 2: "ARCHITECTUUR", 3: "KUNST", 4: "BUSINESS",
        5: "EDUCATIE", 6: "FINANCIEN", 7: "OVERHEID", 8: "GEZONDHEIDSWETENSCHAPPEN",
        9: "HOSPITALITY", 10: "HUMANITAIRE", 11: "ICT", 12: "VEILIGHEID",
        13: "FABRICAGE", 14: "MARKETING", 15: "STEM", 16: "TRANSPORT"
    }
    p21 = all_answers.get("phase2.1", {})  # {(cluster_id, q_idx): (main, skill, interest) or int}
    cluster_sums = {}
    for (cluster_id, _), scores in p21.items():
        name = cluster_id_map.get(cluster_id)
        if not name:
            continue
        if isinstance(scores, int):
            scores = [scores]
        elif isinstance(scores, (tuple, list)):
            scores = [int(s) for s in scores]
        else:
            scores = []
        cluster_sums[name] = cluster_sums.get(name, 0) + sum(scores)
    report_data["phase2.1"] = cluster_sums


    # Phase 2.2 - Cultuur analyse ----------------------------------------

    group_id_map = {
        1: "MENSGERICHTE",
        2: "INNOVATIEVE",
        3: "BEHEERSGERICHTE",
        4: "RESULTAATGERICHTE"
    }
    p22 = all_answers.get("phase2.2", {})  # {(group_id, stmt_idx): value}
    cultuur_totals = {}
    for (group_id, _), val in p22.items():
        name = group_id_map.get(group_id)
        if not name:
            continue
        try:
            cultuur_totals[name] = cultuur_totals.get(name, 0) + int(val)
        except Exception:
            cultuur_totals[name] = cultuur_totals.get(name, 0)
    report_data["phase2.2"] = cultuur_totals


    # Phase 2.3 - JCM ----------------------------------------

    p23 = all_answers.get("phase2.3", {})
    text_answers = {}
    for k, v in p23.items():
        text_answers[str(k)] = str(v)  # force everything to string
    report_data["phase2.3"] = text_answers


    # DEBUG, plz work

    print("--- DEBUG all_answers structure ---")
    for k,v in all_answers.items():
        print(f"{k} <class '{type(v).__name__}'>")
    print("--- DEBUG report_data preview ---")
    for k,v in report_data.items():
        print(f"{k}: {v}")

    return report_data