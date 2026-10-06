from backend.analysis.skill_gap import analyze_skill_gap


# ============================================================
# ROLE PRIORITY SKILLS
# ============================================================

ROLE_PRIORITY_SKILLS = {

    "ai developer": [
        "python",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "generative ai",
        "natural language processing",
        "computer vision",
        "tensorflow",
        "pytorch",
    ],

    "ai engineer": [
        "python",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "generative ai",
    ],

    "machine learning engineer": [
        "machine learning",
        "python",
        "deep learning",
        "data preparation",
        "predictive modeling",
        "cloud platforms",
        "aws",
        "big data",
    ],

    "data scientist": [
        "machine learning",
        "statistics",
        "regressions",
        "data preparation",
        "data visualization",
        "predictive modeling",
        "data mining",
        "time series analysis",
        "python",
        "sql",
        "big data",
        "aws",
    ],

    "data analyst": [
        "sql",
        "data visualization",
        "tableau",
        "python",
        "data preparation",
        "data mining",
        "excel",
        "statistics",
        "power bi",
    ],

    "data engineer": [
        "python",
        "sql",
        "data pipelines",
        "big data",
        "aws",
        "cloud",
        "database",
    ],

    "frontend developer": [
        "javascript",
        "react",
        "html",
        "css",
        "web development",
    ],

    "backend developer": [
        "python",
        "java",
        "sql",
        "api",
        "database",
        "node.js",
        "spring boot",
    ],

    "full stack developer": [
        "javascript",
        "react",
        "node.js",
        "html",
        "css",
        "sql",
        "mongodb",
        "api",
    ],

    "python developer": [
        "python",
        "sql",
        "api",
        "django",
        "flask",
    ],

    "java developer": [
        "java",
        "sql",
        "spring boot",
        "api",
        "database",
    ],

    "cloud engineer": [
        "aws",
        "azure",
        "gcp",
        "cloud",
        "linux",
        "networking",
    ],

    "devops engineer": [
        "docker",
        "kubernetes",
        "linux",
        "ci/cd",
        "aws",
        "cloud",
        "git",
    ],

    "cybersecurity engineer": [
        "cybersecurity",
        "network security",
        "linux",
        "cloud security",
        "security",
    ],

    "cybersecurity analyst": [
        "cybersecurity",
        "security",
        "network security",
        "incident response",
        "risk management",
    ],

    "database administrator": [
        "sql",
        "database",
        "mysql",
        "postgresql",
        "backup",
        "database administration",
    ],

    "sql developer": [
        "sql",
        "database",
        "mysql",
        "postgresql",
        "database development",
    ],

    "business analyst": [
        "business analysis",
        "sql",
        "excel",
        "data analysis",
        "requirements analysis",
        "communication",
    ],

    "product manager": [
        "product management",
        "requirements",
        "communication",
        "analytics",
        "project management",
    ],

    "qa engineer": [
        "testing",
        "software testing",
        "test automation",
        "selenium",
        "quality assurance",
    ],

    "automation test engineer": [
        "test automation",
        "selenium",
        "python",
        "java",
        "testing",
    ],

    "ui/ux designer": [
        "ui design",
        "ux design",
        "figma",
        "wireframing",
        "prototyping",
    ],
}


# ============================================================
# ROLE PRIORITY
# ============================================================

def get_role_priority(target_job):

    normalized = (
        target_job
        .lower()
        .strip()
    )

    return ROLE_PRIORITY_SKILLS.get(
        normalized,
        []
    )


# ============================================================
# WEIGHTED READINESS
# ============================================================

def calculate_weighted_readiness(
    required_skills,
    matching_skills,
    target_job
):

    priority_order = get_role_priority(
        target_job
    )

    exact_matches = {
        skill.lower().strip()
        for skill in matching_skills
    }

    total_weight = 0
    earned_weight = 0

    for skill in required_skills:

        skill_name = (
            skill.lower().strip()
        )

        weight = (
            3
            if skill_name in priority_order
            else 1
        )

        total_weight += weight

        if skill_name in exact_matches:

            earned_weight += weight

    if total_weight == 0:
        return 0

    score = (
        earned_weight
        / total_weight
    ) * 100

    return round(
        min(score, 100),
        2
    )


# ============================================================
# PRIORITIZE MISSING SKILLS
# ============================================================

def prioritize_missing_skills(
    missing_skills,
    target_job
):

    priority_order = get_role_priority(
        target_job
    )

    priority = []
    others = []

    for skill in missing_skills:

        normalized = (
            skill.lower().strip()
        )

        if normalized in priority_order:

            priority.append(skill)

        else:

            others.append(skill)

    priority.sort(
        key=lambda skill:
        priority_order.index(
            skill.lower().strip()
        )
    )

    return priority + others


# ============================================================
# ROADMAP
# ============================================================

def create_roadmap(
    priority_skills,
    target_job,
    study_time,
    experience_level,
    learning_style
):

    hours = max(
        1,
        int(study_time)
    )

    # --------------------------------------------------------
    # No missing skills
    # --------------------------------------------------------

    if not priority_skills:

        return [

            {
                "title":
                    "Strengthen Existing Skills",

                "description":
                    "Review and strengthen your current technical skills."
            },

            {
                "title":
                    "Build Practical Projects",

                "description":
                    f"Build practical {target_job} projects."
            },

            {
                "title":
                    "Practice Interviews",

                "description":
                    "Practice technical and behavioral interview questions."
            },

            {
                "title":
                    "Prepare Portfolio",

                "description":
                    "Organize projects and prepare your professional portfolio."
            }

        ]

    first = priority_skills[0]

    second = (
        priority_skills[1]
        if len(priority_skills) > 1
        else first
    )

    third = (
        priority_skills[2]
        if len(priority_skills) > 2
        else second
    )

    experience = (
        experience_level
        .lower()
    )

    learning = (
        learning_style
        .lower()
    )

    # --------------------------------------------------------
    # Week 1 & 2
    # --------------------------------------------------------

    if experience == "beginner":

        week1 = {

            "title":
                f"Learn {first.title()}",

            "description":
                (
                    f"Learn the fundamentals of "
                    f"{first} with {hours} "
                    f"hours of study per week."
                )
        }

        week2 = {

            "title":
                f"Practice {second.title()}",

            "description":
                (
                    f"Practice {first} and "
                    f"{second} through "
                    f"beginner-friendly exercises."
                )
        }

    elif experience == "intermediate":

        week1 = {

            "title":
                f"Strengthen {first.title()}",

            "description":
                (
                    f"Study advanced concepts "
                    f"and practical applications "
                    f"of {first}."
                )
        }

        week2 = {

            "title":
                f"Apply {second.title()}",

            "description":
                (
                    f"Solve practical problems "
                    f"using {first} and {second}."
                )
        }

    else:

        week1 = {

            "title":
                f"Advanced {first.title()}",

            "description":
                (
                    f"Study advanced industry "
                    f"applications of {first}."
                )
        }

        week2 = {

            "title":
                "Industry Practice",

            "description":
                (
                    f"Work on industry-level "
                    f"problems using {first} "
                    f"and {second}."
                )
        }

    # --------------------------------------------------------
    # Week 3
    # --------------------------------------------------------

    if learning == "project-based":

        week3 = {

            "title":
                f"Build a {target_job} Project",

            "description":
                (
                    f"Build a hands-on project "
                    f"using {third}."
                )
        }

    elif learning == "practice-based":

        week3 = {

            "title":
                "Practical Exercises",

            "description":
                (
                    f"Solve practical exercises "
                    f"and coding problems using "
                    f"{third}."
                )
        }

    else:

        week3 = {

            "title":
                f"Study {third.title()}",

            "description":
                (
                    f"Learn {third} and apply it "
                    f"through practical examples."
                )
        }

    # --------------------------------------------------------
    # Week 4
    # --------------------------------------------------------

    week4 = {

        "title":
            "Portfolio & Interview Preparation",

        "description":
            (
                f"Build a portfolio-ready "
                f"{target_job} project and "
                f"prepare for interviews."
            )
    }

    return [
        week1,
        week2,
        week3,
        week4
    ]


# ============================================================
# PROJECT IDEAS
# ============================================================

def create_project_ideas(
    target_job,
    priority_skills
):

    skills = ", ".join(
        priority_skills[:3]
    )

    if not skills:
        skills = "your existing skills"

    return [

        (
            f"{target_job} portfolio project "
            f"using {skills}."
        ),

        (
            f"Real-world {target_job} "
            f"solution using {skills}."
        ),

        (
            f"End-to-end {target_job} "
            f"project using {skills}."
        ),

    ]


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

def create_interview_questions(
    target_job,
    priority_skills
):

    questions = [

        f"What skills are important for a {target_job}?",

        "Explain your strongest technical skill.",

        "Explain a project you have built.",

        "What technical challenge did you face?",

        f"Why do you want to become a {target_job}?",
    ]

    for skill in priority_skills[:5]:

        questions.append(
            f"Explain {skill} in the context of {target_job}."
        )

    return questions


# ============================================================
# COMPLETE CAREER PLAN
# ============================================================

def create_career_plan(
    target_job,
    current_skills,
    study_time,
    experience_level="Beginner",
    learning_style="Project-Based"
):

    # --------------------------------------------------------
    # Run new skill-gap engine
    # --------------------------------------------------------

    result = analyze_skill_gap(
        current_skills,
        target_job
    )

    if not result:

        return None

    # --------------------------------------------------------
    # NEW skill_gap.py uses these keys
    # --------------------------------------------------------

    required_skills = result.get(
        "Required Skills",
        []
    )

    matching_skills = result.get(
        "Matching Skills",
        []
    )

    missing_skills = result.get(
        "Missing Skills",
        []
    )

    # --------------------------------------------------------
    # Calculate weighted readiness
    # --------------------------------------------------------

    readiness = calculate_weighted_readiness(
        required_skills,
        matching_skills,
        target_job
    )

    # If weighted calculation has no data,
    # fall back to skill-gap readiness.
    if not required_skills:

        readiness = result.get(
            "Readiness Score",
            0
        )

    # --------------------------------------------------------
    # Prioritize missing skills
    # --------------------------------------------------------

    prioritized = prioritize_missing_skills(
        missing_skills,
        target_job
    )

    priority_skills = prioritized[:5]

    # --------------------------------------------------------
    # Roadmap
    # --------------------------------------------------------

    roadmap = create_roadmap(

        priority_skills,

        target_job,

        study_time,

        experience_level,

        learning_style
    )

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {

        "target_job":
            target_job,

        "current_skills":
            current_skills,

        "required_skills":
            required_skills,

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "readiness":
            readiness,

        "study_time":
            study_time,

        "experience_level":
            experience_level,

        "learning_style":
            learning_style,

        "priority_skills":
            priority_skills,

        "roadmap":
            roadmap,

        "project_ideas":
            create_project_ideas(
                target_job,
                priority_skills
            ),

        "interview_questions":
            create_interview_questions(
                target_job,
                priority_skills
            ),

        "job_description":
            result.get(
                "Job Description",
                ""
            ),

        "related_jobs":
            result.get(
                "Related Jobs",
                []
            ),
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = create_career_plan(

        target_job="AI Developer",

        current_skills=[
            "Python"
        ],

        study_time=10,

        experience_level="Beginner",

        learning_style="Project-Based"
    )

    if result is None:

        print(
            "\nTarget job not found."
        )

    else:

        print(
            "\n======================================"
        )

        print(
            "       GENAI CAREER NAVIGATOR"
        )

        print(
            "======================================"
        )

        print(
            f"\nTarget Job: "
            f"{result['target_job']}"
        )

        print(
            f"\nReadiness: "
            f"{result['readiness']}%"
        )

        print(
            "\nMatching Skills:"
        )

        for skill in result[
            "matching_skills"
        ]:

            print(
                f"  ✓ {skill}"
            )

        print(
            "\nMissing Skills:"
        )

        for skill in result[
            "missing_skills"
        ]:

            print(
                f"  • {skill}"
            )

        print(
            "\nPriority Skills:"
        )

        for index, skill in enumerate(
            result["priority_skills"],
            start=1
        ):

            print(
                f"  {index}. {skill}"
            )

        print(
            "\nRoadmap:"
        )

        for index, week in enumerate(
            result["roadmap"],
            start=1
        ):

            print(
                f"\nWeek {index}: "
                f"{week['title']}"
            )

            print(
                week["description"]
            )