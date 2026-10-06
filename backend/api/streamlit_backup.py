import streamlit as st
from career_engine import create_career_plan
from genai import generate_career_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GenAI Career Navigator",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .roadmap {
        padding: 18px;
        border: 1px solid #ddd;
        border-radius: 12px;
        margin-bottom: 12px;
        background: #fafafa;
    }

    .skill {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 7px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚀 GenAI Career Navigator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Personalized Skill Gap Analysis & Career Roadmap System'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("👤 Career Profile")

target_job = st.sidebar.selectbox(
    "🎯 Target Job Role",
    [
        "Data Scientist",
        "Data Analyst",
        "Machine Learning Engineer",
        "Frontend Developer",
        "Backend Developer"
    ]
)

skills_input = st.sidebar.text_area(
    "💻 Current Skills",
    value="Python, SQL, ML, Data Visualization"
)

experience_level = st.sidebar.selectbox(
    "📈 Experience Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

study_time = st.sidebar.number_input(
    "⏰ Study Hours / Week",
    min_value=1,
    max_value=60,
    value=10
)

learning_style = st.sidebar.selectbox(
    "📚 Learning Style",
    [
        "Project-Based",
        "Practice-Based",
        "Theory-Based"
    ]
)

analyze = st.sidebar.button(
    "🚀 ANALYZE MY CAREER",
    use_container_width=True
)


# ============================================================
# INTRO SCREEN
# ============================================================

if not analyze:

    st.info(
        "👈 Enter your details and click "
        "**ANALYZE MY CAREER** to generate your personalized career plan."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍 Skill Gap")
        st.write(
            "Identify the skills you already have "
            "and the skills you need for your target role."
        )

    with col2:
        st.markdown("### 🗺️ Career Roadmap")
        st.write(
            "Get a personalized learning path "
            "based on your profile."
        )

    with col3:
        st.markdown("### 🤖 GenAI")
        st.write(
            "Receive AI-powered career guidance, "
            "projects and interview preparation."
        )

    st.stop()


# ============================================================
# PROCESS INPUT
# ============================================================

current_skills = [
    skill.strip()
    for skill in skills_input.split(",")
    if skill.strip()
]


if not current_skills:

    st.error("Please enter at least one skill.")

    st.stop()


# ============================================================
# CAREER ENGINE
# ============================================================

with st.spinner(
    "🔎 Analyzing your career profile..."
):

    try:

        result = create_career_plan(
            target_job=target_job,
            current_skills=current_skills,
            study_time=study_time,
            experience_level=experience_level,
            learning_style=learning_style
        )

    except Exception as error:

        st.error(
            "Career analysis failed."
        )

        st.exception(error)

        st.stop()


if result is None:

    st.error(
        f"No matching information was found for {target_job}."
    )

    st.stop()


# ============================================================
# PROFILE
# ============================================================

st.markdown(
    '<div class="section-title">👤 Career Profile</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Target Role",
        result["target_job"]
    )

with c2:
    st.metric(
        "Experience",
        result["experience_level"]
    )

with c3:
    st.metric(
        "Study Time",
        f"{result['study_time']} hrs"
    )

with c4:
    st.metric(
        "Learning Style",
        result["learning_style"]
    )


# ============================================================
# SCORE
# ============================================================

st.markdown(
    '<div class="section-title">📊 Skill Match Score</div>',
    unsafe_allow_html=True
)

score = result["readiness"]

score_col1, score_col2 = st.columns([1, 3])

with score_col1:

    st.metric(
        "Skill Match",
        f"{score}%"
    )

with score_col2:

    st.progress(
        min(score / 100, 1.0)
    )

    st.caption(
        "This is a project-specific skill-match indicator "
        "based on the selected dataset and matching logic."
    )


# ============================================================
# SKILL ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Skill Analysis</div>',
    unsafe_allow_html=True
)

skill_col1, skill_col2 = st.columns(2)


with skill_col1:

    st.subheader("✅ Matching Skills")

    if result["matching_skills"]:

        for skill in result["matching_skills"]:

            st.markdown(
                f'<div class="skill">✅ {skill}</div>',
                unsafe_allow_html=True
            )

    else:

        st.info("No exact matches.")


with skill_col2:

    st.subheader("⚠️ Missing Skills")

    if result["missing_skills"]:

        for skill in result["missing_skills"]:

            st.markdown(
                f'<div class="skill">⚠️ {skill}</div>',
                unsafe_allow_html=True
            )

    else:

        st.success("No major skill gaps detected.")


# ============================================================
# NLP MATCHES
# ============================================================

st.markdown(
    '<div class="section-title">🔎 NLP Skill Matching</div>',
    unsafe_allow_html=True
)

if result["nlp_matches"]:

    for match in result["nlp_matches"]:

        n1, n2, n3 = st.columns(3)

        with n1:
            st.write(
                f"**Your Skill**  \n"
                f"{match['user_skill']}"
            )

        with n2:
            st.write(
                f"**Matched Skill**  \n"
                f"{match['matched_skill']}"
            )

        with n3:
            st.write(
                f"**Similarity**  \n"
                f"{match['similarity']}"
            )

else:

    st.info(
        "No additional NLP matches detected."
    )


# ============================================================
# PRIORITY SKILLS
# ============================================================

st.markdown(
    '<div class="section-title">🔥 Priority Skills</div>',
    unsafe_allow_html=True
)

priority_skills = result["priority_skills"]

if priority_skills:

    columns = st.columns(
        len(priority_skills)
    )

    for i, skill in enumerate(
        priority_skills
    ):

        with columns[i]:

            st.metric(
                f"Priority {i + 1}",
                skill
            )


# ============================================================
# ROADMAP
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ Personalized Roadmap</div>',
    unsafe_allow_html=True
)

for week in result["roadmap"]:

    st.markdown(
        f"""
        <div class="roadmap">
        📅 {week}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PROJECTS
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Recommended Projects</div>',
    unsafe_allow_html=True
)

for i, project in enumerate(
    result["project_ideas"],
    start=1
):

    with st.expander(
        f"Project {i}"
    ):

        st.write(project)


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Interview Preparation</div>',
    unsafe_allow_html=True
)

for i, question in enumerate(
    result["interview_questions"],
    start=1
):

    with st.expander(
        f"Question {i}"
    ):

        st.write(question)


# ============================================================
# GENAI
# ============================================================

st.markdown(
    '<div class="section-title">🤖 GenAI Career Assistant</div>',
    unsafe_allow_html=True
)

st.write(
    "Groq AI uses your career-analysis results to provide "
    "additional personalized guidance."
)


if st.button(
    "🤖 Generate AI Career Guidance",
    use_container_width=True
):

    with st.spinner(
        "🤖 Groq AI is generating your personalized guidance..."
    ):

        try:

            ai_response = generate_career_response(

                target_job=result["target_job"],

                current_skills=result["current_skills"],

                missing_skills=result["missing_skills"],

                study_time=result["study_time"],

                experience_level=result["experience_level"],

                learning_style=result["learning_style"]
            )

            st.success(
                "AI Career Guidance Generated!"
            )

            st.markdown(
                ai_response
            )

        except Exception as error:

            st.error(
                "Unable to generate AI guidance."
            )

            st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
    GenAI Career Navigator | Skill Intelligence + NLP + Generative AI
    </div>
    """,
    unsafe_allow_html=True
)