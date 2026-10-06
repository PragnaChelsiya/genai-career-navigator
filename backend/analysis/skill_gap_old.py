from pathlib import Path

import pandas as pd

from .nlp_matcher import match_multiple_skills


# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "new_jobs.csv"
)


# ==========================================
# DATASET
# ==========================================

def load_dataset():

    try:

        return pd.read_csv(
            DATASET_PATH
        )

    except FileNotFoundError:

        print(
            f"Dataset not found: "
            f"{DATASET_PATH}"
        )

        return pd.DataFrame()

    except Exception as error:

        print(
            f"Dataset loading error: "
            f"{error}"
        )

        return pd.DataFrame()


# ==========================================
# NORMALIZATION
# ==========================================

def normalize_skill(skill):

    if not isinstance(skill, str):
        return ""

    return " ".join(
        skill.lower().strip().split()
    )


def normalize_job_title(title):

    if not isinstance(title, str):
        return ""

    title = title.lower().strip()

    title = title.replace("-", " ")
    title = title.replace("_", " ")
    title = title.replace("/", " ")

    return " ".join(
        title.split()
    )


# ==========================================
# PARSE SKILLS
# ==========================================

def parse_skills(skills):

    if isinstance(skills, list):
        return skills

    if not isinstance(skills, str):
        return []

    skills = skills.strip()

    if not skills:
        return []

    # Try Python-list format
    try:

        import ast

        parsed = ast.literal_eval(
            skills
        )

        if isinstance(parsed, list):

            return [
                str(skill).strip()
                for skill in parsed
                if str(skill).strip()
            ]

    except (
        ValueError,
        SyntaxError
    ):
        pass

    # Try comma-separated skills
    return [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]


# ==========================================
# FIND JOB
# ==========================================

def find_job(target_job):

    df = load_dataset()

    if df.empty:
        return pd.DataFrame()

    target = normalize_job_title(
        target_job
    )

    job_titles = (
        df["Job Title"]
        .fillna("")
        .astype(str)
        .apply(normalize_job_title)
    )

    # ======================================
    # EXACT MATCH
    # ======================================

    exact_matches = df[
        job_titles == target
    ]

    if not exact_matches.empty:

        return exact_matches

    # ======================================
    # PARTIAL MATCH
    # ======================================

    partial_matches = df[
        job_titles.str.contains(
            target,
            case=False,
            na=False,
            regex=False
        )
    ]

    return partial_matches


# ==========================================
# GET REQUIRED SKILLS
# ==========================================

def get_required_skills(target_job):

    matches = find_job(
        target_job
    )

    if matches.empty:
        return []

    all_skills = []

    for skills in matches["Skills"]:

        all_skills.extend(
            parse_skills(skills)
        )

    required_skills = sorted(
        {
            normalize_skill(skill)
            for skill in all_skills
            if normalize_skill(skill)
        }
    )

    return required_skills


# ==========================================
# GET JOB DESCRIPTION
# ==========================================

def get_job_description(target_job):

    matches = find_job(
        target_job
    )

    if matches.empty:
        return ""

    descriptions = (
        matches["Job Description"]
        .dropna()
        .astype(str)
        .tolist()
    )

    if not descriptions:
        return ""

    return descriptions[0]


# ==========================================
# ANALYZE SKILL GAP
# ==========================================

def analyze_skill_gap(
    current_skills,
    target_job
):

    required_skills = get_required_skills(
        target_job
    )

    if not required_skills:
        return None

    # ======================================
    # CLEAN USER SKILLS
    # ======================================

    current_skills_clean = [

        normalize_skill(skill)

        for skill in current_skills

        if normalize_skill(skill)

    ]

    current_skill_set = set(
        current_skills_clean
    )

    required_skill_set = set(
        required_skills
    )

    # ======================================
    # EXACT MATCHES
    # ======================================

    exact_matches = sorted(

        current_skill_set.intersection(
            required_skill_set
        )

    )

    # ======================================
    # UNMATCHED USER SKILLS
    # ======================================

    unmatched_user_skills = [

        skill

        for skill in current_skill_set

        if skill not in required_skill_set

    ]

    # ======================================
    # UNMATCHED REQUIRED SKILLS
    # ======================================

    unmatched_required_skills = [

        skill

        for skill in required_skills

        if skill not in exact_matches

    ]

    # ======================================
    # NLP MATCHING
    # ======================================

    nlp_matches = match_multiple_skills(

        unmatched_user_skills,

        unmatched_required_skills

    )

    nlp_matched_skills = {

        normalize_skill(
            match["matched_skill"]
        )

        for match in nlp_matches

    }

    # ======================================
    # MISSING SKILLS
    # ======================================

    missing_skills = sorted(

        required_skill_set

        - set(exact_matches)

        - nlp_matched_skills

    )

    # ======================================
    # READINESS SCORE
    # ======================================

    exact_count = len(
        exact_matches
    )

    nlp_score = sum(

        match["similarity"]

        for match in nlp_matches

    )

    effective_matches = (
        exact_count
        + nlp_score
    )

    if len(required_skills) > 0:

        skill_match_score = (

            effective_matches
            / len(required_skills)

        ) * 100

    else:

        skill_match_score = 0

    skill_match_score = round(

        min(
            skill_match_score,
            100
        ),

        2

    )

    # ======================================
    # RESULT
    # ======================================

    return {

        "target_job":
            target_job,

        "required_skills":
            required_skills,

        "matching_skills":
            exact_matches,

        "nlp_matches":
            nlp_matches,

        "missing_skills":
            missing_skills,

        "readiness":
            skill_match_score,

        "job_description":
            get_job_description(
                target_job
            )

    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_roles = [

        "Data Scientist",

        "Data Analyst",

        "AI Engineer",

        "Machine Learning Engineer",

        "Python Developer",

        "Frontend Developer",

        "Backend Developer",

    ]

    print(
        "\n======================================"
    )

    print(
        "       NEW CAREER DATASET TEST"
    )

    print(
        "======================================"
    )

    df = load_dataset()

    print(
        f"\nDataset rows: {len(df)}"
    )

    print(
        f"Dataset columns: "
        f"{list(df.columns)}"
    )

    print(
        f"Unique roles: "
        f"{df['Job Title'].nunique()}"
    )

    for role in test_roles:

        skills = get_required_skills(
            role
        )

        print(
            f"\n{role}"
        )

        print(
            f"Required skills: "
            f"{len(skills)}"
        )

        print(
            skills
        )