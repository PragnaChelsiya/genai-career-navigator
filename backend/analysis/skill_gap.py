import ast
import json
import re
from pathlib import Path

import pandas as pd

from backend.analysis.nlp_matcher import (
    normalize_skill,
    match_multiple_skills
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

PARQUET_FILE = DATA_DIR / "train-00000-of-00001.parquet"

IT_ROLES_FILE = (
    DATA_DIR /
    "Top_207_IT_Job_Roles_Skills_Database.json"
)

CAREER_ROLES_FILE = DATA_DIR / "career_roles.json"


# ============================================================
# ROLE ALIASES
# ============================================================

ROLE_ALIASES = {

    "ai developer": [
        "ai developer",
        "artificial intelligence developer",
        "ai engineer",
        "artificial intelligence engineer",
        "machine learning developer",
        "machine learning engineer",
        "developer",
    ],

    "ai engineer": [
        "ai engineer",
        "artificial intelligence engineer",
        "artificial intelligence",
        "machine learning engineer",
    ],

    "machine learning engineer": [
        "machine learning engineer",
        "ml engineer",
        "machine learning developer",
    ],

    "data scientist": [
        "data scientist",
        "data science",
    ],

    "data analyst": [
        "data analyst",
        "data analytics",
        "business data analyst",
    ],

    "data engineer": [
        "data engineer",
        "big data engineer",
        "data platform engineer",
    ],

    "software developer": [
        "software developer",
        "software engineer",
        "developer",
    ],

    "software engineer": [
        "software engineer",
        "software developer",
        "developer",
    ],

    "full stack developer": [
        "full stack developer",
        "full stack engineer",
        "fullstack developer",
    ],

    "frontend developer": [
        "frontend developer",
        "front end developer",
        "frontend engineer",
        "front end engineer",
    ],

    "backend developer": [
        "backend developer",
        "back end developer",
        "backend engineer",
        "back end engineer",
    ],

    "python developer": [
        "python developer",
        "python programmer",
        "software developer",
    ],

    "java developer": [
        "java developer",
        "java software developer",
        "software developer",
    ],

    "cloud engineer": [
        "cloud engineer",
        "cloud developer",
        "cloud architect",
    ],

    "devops engineer": [
        "devops engineer",
        "devops",
        "site reliability engineer",
    ],

    "cybersecurity engineer": [
        "cybersecurity engineer",
        "security engineer",
        "cyber security engineer",
    ],

    "cybersecurity analyst": [
        "cybersecurity analyst",
        "cyber security analyst",
        "security analyst",
        "information security analyst",
    ],

    "database administrator": [
        "database administrator",
        "database admin",
        "dba",
    ],

    "sql developer": [
        "sql developer",
        "database developer",
        "database engineer",
    ],

    "business analyst": [
        "business analyst",
        "business analytics",
    ],

    "product manager": [
        "product manager",
        "product management",
    ],

    "qa engineer": [
        "qa engineer",
        "quality assurance engineer",
        "test engineer",
    ],

    "automation test engineer": [
        "automation test engineer",
        "automation engineer",
        "qa automation engineer",
    ],

    "ui/ux designer": [
        "ui/ux designer",
        "ui designer",
        "ux designer",
        "user experience designer",
    ],
}


# ============================================================
# COMMON HELPERS
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return str(value).strip()


def normalize_role(role):

    role = clean_text(role).lower()

    role = role.replace("&", "and")
    role = role.replace("/", " ")
    role = role.replace("-", " ")

    role = re.sub(r"\s+", " ", role)
    role = re.sub(r"[^a-z0-9 ]", "", role)

    return role.strip()


# ============================================================
# SKILL PARSING
# ============================================================

def parse_skills(value):

    if value is None:
        return []

    if isinstance(value, list):

        return [
            clean_text(x)
            for x in value
            if clean_text(x)
        ]

    if isinstance(value, tuple):

        return [
            clean_text(x)
            for x in value
            if clean_text(x)
        ]

    if isinstance(value, set):

        return [
            clean_text(x)
            for x in value
            if clean_text(x)
        ]

    text = clean_text(value)

    if not text:
        return []

    # --------------------------------------------------------
    # Python / JSON list
    # --------------------------------------------------------

    if text.startswith("[") and text.endswith("]"):

        try:

            parsed = ast.literal_eval(text)

            if isinstance(
                parsed,
                (list, tuple, set)
            ):

                return [
                    clean_text(x)
                    for x in parsed
                    if clean_text(x)
                ]

        except Exception:
            pass

        try:

            parsed = json.loads(text)

            if isinstance(parsed, list):

                return [
                    clean_text(x)
                    for x in parsed
                    if clean_text(x)
                ]

        except Exception:
            pass

    # --------------------------------------------------------
    # Common separators
    # --------------------------------------------------------

    if ";" in text:

        parts = text.split(";")

    elif "|" in text:

        parts = text.split("|")

    elif "\n" in text:

        parts = text.splitlines()

    elif "," in text:

        parts = text.split(",")

    else:

        parts = [text]

    return [
        clean_text(part)
        for part in parts
        if clean_text(part)
    ]


# ============================================================
# 3050 ROW DATASET
# ============================================================

def load_main_dataset():

    if not PARQUET_FILE.exists():

        print(
            "WARNING: 3050-row dataset not found:",
            PARQUET_FILE
        )

        return pd.DataFrame(
            columns=[
                "Job Title",
                "Skills",
                "Job Description",
                "Source"
            ]
        )

    df = pd.read_parquet(
        PARQUET_FILE
    )

    result = pd.DataFrame()

    result["Job Title"] = (
        df["title"]
        .fillna("")
        .astype(str)
    )

    result["Skills"] = (
        df["required_skills"]
        .fillna("")
        .apply(
            lambda x:
            " | ".join(x)
            if isinstance(x, list)
            else str(x)
        )
    )

    result["Job Description"] = (
        df["job_description"]
        .fillna("")
        .astype(str)
    )

    result["Source"] = (
        "3050-row dataset"
    )

    return result


# ============================================================
# 207 ROLE JSON DATASET
# ============================================================

def load_it_roles_dataset():

    if not IT_ROLES_FILE.exists():

        print(
            "WARNING: 207-role dataset not found:",
            IT_ROLES_FILE
        )

        return pd.DataFrame(
            columns=[
                "Job Title",
                "Skills",
                "Job Description",
                "Source"
            ]
        )

    print(
        "Loading 207-role JSON dataset..."
    )

    try:

        with open(
            IT_ROLES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception as error:

        print(
            "ERROR reading 207-role JSON:",
            error
        )

        return pd.DataFrame(
            columns=[
                "Job Title",
                "Skills",
                "Job Description",
                "Source"
            ]
        )

    # --------------------------------------------------------
    # Find actual records
    # --------------------------------------------------------

    records = data

    if isinstance(data, dict):

        # Common dataset wrappers
        possible_keys = [
            "data",
            "records",
            "jobs",
            "roles",
            "items"
        ]

        found = None

        for key in possible_keys:

            if key in data and isinstance(
                data[key],
                list
            ):

                found = data[key]
                break

        if found is not None:

            records = found

        else:

            # Sometimes JSON is a dictionary
            # containing numeric keys
            values = list(data.values())

            if values and all(
                isinstance(x, dict)
                for x in values
            ):

                records = values

    if not isinstance(records, list):

        print(
            "WARNING: Could not identify records "
            "inside 207-role JSON."
        )

        return pd.DataFrame(
            columns=[
                "Job Title",
                "Skills",
                "Job Description",
                "Source"
            ]
        )

    rows = []

    for record in records:

        if not isinstance(
            record,
            dict
        ):
            continue

        # ----------------------------------------------------
        # Flexible column detection
        # ----------------------------------------------------

        title = ""

        skills = ""

        description = ""

        for key, value in record.items():

            normalized_key = (
                str(key)
                .strip()
                .lower()
                .replace("_", " ")
            )

            if normalized_key in [
                "job title",
                "job role",
                "job_role",
                "title",
                "role"
            ]:

                title = value

            elif normalized_key in [
                "skills",
                "required skills",
                "required_skills"
            ]:

                skills = value

            elif normalized_key in [
                "job description",
                "job_description",
                "description"
            ]:

                description = value

        rows.append({

            "Job Title":
                clean_text(title),

            "Skills":
                skills,

            "Job Description":
                clean_text(description),

            "Source":
                "207-role IT dataset"
        })

    result = pd.DataFrame(rows)

    if result.empty:

        return pd.DataFrame(
            columns=[
                "Job Title",
                "Skills",
                "Job Description",
                "Source"
            ]
        )

    return result


# ============================================================
# COMBINE DATASETS
# ============================================================

def load_dataset():

    main_df = load_main_dataset()

    it_df = load_it_roles_dataset()

    combined = pd.concat(
        [
            main_df,
            it_df
        ],
        ignore_index=True
    )

    combined = combined[
        combined["Job Title"]
        .astype(str)
        .str.strip()
        != ""
    ]

    combined = combined.drop_duplicates(
        subset=[
            "Job Title",
            "Skills",
            "Job Description"
        ]
    )

    combined = combined.reset_index(
        drop=True
    )

    print()
    print(
        "===================================="
    )
    print(
        "CAREER DATASET LOADED"
    )
    print(
        "===================================="
    )

    print(
        f"3050-row dataset: {len(main_df)} rows"
    )

    print(
        f"207-role dataset:  {len(it_df)} rows"
    )

    print(
        f"Combined dataset:  {len(combined)} rows"
    )

    print(
        "===================================="
    )

    print()

    return combined


# ============================================================
# CAREER ROLES
# ============================================================

def load_career_roles():

    if not CAREER_ROLES_FILE.exists():
        return []

    with open(
        CAREER_ROLES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        roles = json.load(file)

    if isinstance(
        roles,
        list
    ):

        return roles

    return []


# ============================================================
# ROLE CANDIDATES
# ============================================================

def get_role_candidates(
    target_job
):

    normalized_target = normalize_role(
        target_job
    )

    candidates = [
        normalized_target
    ]

    if normalized_target in ROLE_ALIASES:

        candidates.extend(
            normalize_role(role)
            for role in ROLE_ALIASES[
                normalized_target
            ]
        )

    return list(
        dict.fromkeys(
            candidates
        )
    )


# ============================================================
# FIND RELATED JOBS
# ============================================================

def find_related_jobs(
    df,
    target_job,
    limit=15
):

    if df.empty:
        return df.copy()

    target = normalize_role(
        target_job
    )

    candidates = get_role_candidates(
        target_job
    )

    working = df.copy()

    working["_normalized_title"] = (
        working["Job Title"]
        .fillna("")
        .apply(normalize_role)
    )

    # --------------------------------------------------------
    # Exact
    # --------------------------------------------------------

    exact = working[
        working["_normalized_title"]
        == target
    ]

    if not exact.empty:

        return exact.drop(
            columns=[
                "_normalized_title"
            ]
        ).head(limit)

    # --------------------------------------------------------
    # Alias
    # --------------------------------------------------------

    alias_matches = working[
        working["_normalized_title"]
        .isin(candidates)
    ]

    if not alias_matches.empty:

        return alias_matches.drop(
            columns=[
                "_normalized_title"
            ]
        ).head(limit)

    # --------------------------------------------------------
    # Token similarity
    # --------------------------------------------------------

    target_tokens = set(
        target.split()
    )

    def score(title):

        title_tokens = set(
            title.split()
        )

        if not title_tokens:
            return 0

        overlap = (
            target_tokens
            .intersection(
                title_tokens
            )
        )

        return (
            len(overlap)
            /
            max(
                len(target_tokens),
                1
            )
        )

    working["_score"] = (
        working["_normalized_title"]
        .apply(score)
    )

    related = working[
        working["_score"] > 0
    ].sort_values(
        "_score",
        ascending=False
    )

    if not related.empty:

        return related.drop(
            columns=[
                "_normalized_title",
                "_score"
            ]
        ).head(limit)

    # --------------------------------------------------------
    # AI fallback
    # --------------------------------------------------------

    if target in [
        "ai developer",
        "ai engineer",
        "artificial intelligence developer",
        "artificial intelligence engineer"
    ]:

        keywords = [
            "artificial intelligence",
            "ai",
            "machine learning",
            "developer",
            "engineer"
        ]

        mask = (
            working["_normalized_title"]
            .apply(
                lambda title:
                any(
                    keyword in title
                    for keyword in keywords
                )
            )
        )

        ai_related = working[mask]

        if not ai_related.empty:

            return ai_related.drop(
                columns=[
                    "_normalized_title"
                ]
            ).head(limit)

    return pd.DataFrame(
        columns=df.columns
    ).drop(
        columns=[
            "_normalized_title"
        ],
        errors="ignore"
    )


# ============================================================
# REQUIRED SKILLS
# ============================================================

def extract_required_skills(
    job_rows
):

    all_skills = []

    if job_rows.empty:
        return []

    for value in job_rows["Skills"]:

        skills = parse_skills(
            value
        )

        for skill in skills:

            normalized = normalize_skill(
                skill
            )

            if normalized:

                all_skills.append(
                    normalized
                )

    return list(
        dict.fromkeys(
            all_skills
        )
    )


# ============================================================
# JOB DESCRIPTION
# ============================================================

def get_job_description(
    job_rows
):

    if job_rows.empty:
        return ""

    descriptions = []

    for value in job_rows[
        "Job Description"
    ]:

        text = clean_text(
            value
        )

        if text:

            descriptions.append(
                text
            )

    if not descriptions:
        return ""

    return max(
        descriptions,
        key=len
    )


# ============================================================
# ANALYZE SKILL GAP
# ============================================================

def analyze_skill_gap(
    current_skills,
    target_job
):

    df = load_dataset()

    related_jobs = find_related_jobs(
        df,
        target_job,
        limit=15
    )

    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if related_jobs.empty:

        return {

            "Target Job":
                target_job,

            "Required Skills":
                [],

            "Matching Skills":
                [],

            "Missing Skills":
                [],

            "Readiness Score":
                0,

            "Job Description":
                "",

            "Related Jobs":
                [],

            "Message":
                (
                    f"No dataset records "
                    f"were found for "
                    f"'{target_job}'."
                )
        }

    # --------------------------------------------------------
    # Required skills
    # --------------------------------------------------------

    required_skills = (
        extract_required_skills(
            related_jobs
        )
    )

    # --------------------------------------------------------
    # User skills
    # --------------------------------------------------------

    if isinstance(
        current_skills,
        str
    ):

        user_skills = parse_skills(
            current_skills
        )

    else:

        user_skills = (
            current_skills
            or []
        )

    normalized_user_skills = []

    for skill in user_skills:

        normalized = normalize_skill(
            skill
        )

        if normalized:

            normalized_user_skills.append(
                normalized
            )

    normalized_user_skills = list(
        dict.fromkeys(
            normalized_user_skills
        )
    )

    # --------------------------------------------------------
    # NLP matching
    # --------------------------------------------------------

    matches = match_multiple_skills(
        normalized_user_skills,
        required_skills
    )

    matching_skills = [
        match["matched_skill"]
        for match in matches
    ]

    matched_normalized = {
        normalize_skill(skill)
        for skill in matching_skills
    }

    missing_skills = [

        skill

        for skill in required_skills

        if normalize_skill(skill)
        not in matched_normalized
    ]

    # --------------------------------------------------------
    # Readiness
    # --------------------------------------------------------

    if required_skills:

        readiness_score = round(
            (
                len(
                    matching_skills
                )
                /
                len(
                    required_skills
                )
            )
            * 100,
            2
        )

    else:

        readiness_score = 0

    # --------------------------------------------------------
    # Related jobs
    # --------------------------------------------------------

    related_job_names = list(
        dict.fromkeys(
            related_jobs[
                "Job Title"
            ]
            .astype(str)
            .tolist()
        )
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {

        "Target Job":
            target_job,

        "Required Skills":
            required_skills,

        "Matching Skills":
            matching_skills,

        "Missing Skills":
            missing_skills,

        "Readiness Score":
            readiness_score,

        "Job Description":
            get_job_description(
                related_jobs
            ),

        "Related Jobs":
            related_job_names
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "Testing combined career dataset..."
    )
    print()

    df = load_dataset()

    print(
        "Total rows:",
        len(df)
    )

    print()
    print(
        "Sample roles:"
    )

    print(
        df["Job Title"]
        .drop_duplicates()
        .head(20)
        .to_string(
            index=False
        )
    )

    print()
    print(
        "Testing AI Developer..."
    )

    result = analyze_skill_gap(
        ["Python"],
        "AI Developer"
    )

    print()
    print(
        "Target Job:"
    )

    print(
        result["Target Job"]
    )

    print()
    print(
        "Required Skills:"
    )

    print(
        result["Required Skills"]
    )

    print()
    print(
        "Matching Skills:"
    )

    print(
        result["Matching Skills"]
    )

    print()
    print(
        "Missing Skills:"
    )

    print(
        result["Missing Skills"]
    )

    print()
    print(
        "Readiness Score:"
    )

    print(
        result["Readiness Score"]
    )

    print()
    print(
        "Related Jobs:"
    )

    for job in result[
        "Related Jobs"
    ]:

        print(
            "-",
            job
        )