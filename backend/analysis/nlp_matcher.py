from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Common skill variations
SKILL_ALIASES = {
    "python programming": "python",
    "python language": "python",
    "python developer": "python",

    "ml": "machine learning",
    "ml algorithms": "machine learning",
    "machine learning algorithms": "machine learning",

    "ai": "artificial intelligence",
    "ai programming": "artificial intelligence",

    "powerbi": "power bi",
    "power bi desktop": "power bi",
    "microsoft power bi": "power bi",

    "ms excel": "excel",
    "microsoft excel": "excel",

    "js": "javascript",
    "javascript programming": "javascript",

    "react js": "react",
    "react.js": "react",

    "nodejs": "node.js",
    "node js": "node.js",

    "sql programming": "sql",
    "structured query language": "sql",

    "data viz": "data visualization",
    "data visualization tools": "data visualization",

    "statistics": "statistics",
    "statistical analysis": "statistics",

    "regression analysis": "regressions",
    "regression": "regressions",

    "predictive analytics": "predictive modeling",

    "big data analytics": "big data",

    "amazon web services": "aws",
}


def normalize_skill(skill):
    """
    Convert different skill names
    into a standard representation.
    """

    if not isinstance(skill, str):
        return ""

    skill = skill.lower().strip()

    skill = " ".join(skill.split())

    return SKILL_ALIASES.get(
        skill,
        skill
    )


def exact_or_alias_match(user_skill, required_skills):
    """
    Check direct and alias-based matches.
    """

    normalized_user = normalize_skill(user_skill)

    for required_skill in required_skills:

        normalized_required = normalize_skill(
            required_skill
        )

        if normalized_user == normalized_required:

            return {
                "matched_skill": required_skill,
                "similarity": 1.0,
                "match_type": "exact/alias"
            }

    return None


def find_similar_skill(
    user_skill,
    required_skills,
    threshold=0.45
):
    """
    Find the most similar required skill
    using aliases and TF-IDF cosine similarity.
    """

    if not required_skills:
        return None

    # Exact / alias matching
    direct_match = exact_or_alias_match(
        user_skill,
        required_skills
    )

    if direct_match is not None:
        return direct_match

    normalized_user = normalize_skill(
        user_skill
    )

    normalized_required = [
        normalize_skill(skill)
        for skill in required_skills
    ]

    # TF-IDF similarity
    documents = [
        normalized_user
    ] + normalized_required

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform(
            documents
        )

    except ValueError:
        return None

    similarities = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    best_index = similarities.argmax()

    best_score = float(
        similarities[best_index]
    )

    if best_score >= threshold:

        return {
            "matched_skill":
                required_skills[best_index],

            "similarity":
                round(best_score, 3),

            "match_type":
                "semantic"
        }

    return None


def match_multiple_skills(
    user_skills,
    required_skills
):
    """
    Match multiple user skills
    against required job skills.
    """

    matches = []

    already_matched = set()

    for user_skill in user_skills:

        result = find_similar_skill(
            user_skill,
            required_skills
        )

        if result is None:
            continue

        matched_skill = result[
            "matched_skill"
        ]

        normalized_matched = normalize_skill(
            matched_skill
        )

        # Prevent multiple user skills
        # from matching the same required skill
        if normalized_matched in already_matched:
            continue

        already_matched.add(
            normalized_matched
        )

        matches.append({
            "user_skill":
                user_skill,

            "matched_skill":
                matched_skill,

            "similarity":
                result["similarity"],

            "match_type":
                result["match_type"]
        })

    return matches


if __name__ == "__main__":

    required_skills = [
        "python",
        "machine learning",
        "data visualization",
        "sql",
        "statistics",
        "regressions",
        "predictive modeling",
        "big data",
        "aws"
    ]

    user_skills = [
        "Python programming",
        "ML",
        "data viz",
        "regression analysis",
        "Amazon Web Services"
    ]

    print(
        "======================================"
    )

    print(
        "       NLP SKILL MATCHING TEST"
    )

    print(
        "======================================"
    )

    matches = match_multiple_skills(
        user_skills,
        required_skills
    )

    for match in matches:

        print(
            f"\n{match['user_skill']}"
        )

        print(
            f"  → {match['matched_skill']}"
        )

        print(
            f"  Similarity: "
            f"{match['similarity']}"
        )

        print(
            f"  Type: "
            f"{match['match_type']}"
        )