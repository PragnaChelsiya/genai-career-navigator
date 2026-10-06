import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Load .env from project root
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"


# Create Groq client only when API key exists
client = None

if GROQ_API_KEY:
    client = Groq(
        api_key=GROQ_API_KEY
    )


def generate_career_response(
    target_job,
    current_skills,
    missing_skills,
    study_time,
    experience_level,
    learning_style
):
    """
    Generate a personalized career plan using Groq GenAI.
    """

    if client is None:

        return (
            "Groq API key was not found.\n\n"
            "Please check your .env file."
        )

    prompt = f"""
You are an expert AI career advisor.

Create a personalized career development plan
for a computer science student.

Target Job:
{target_job}

Current Skills:
{", ".join(current_skills)}

Missing Skills:
{", ".join(missing_skills)}

Experience Level:
{experience_level}

Available Study Time:
{study_time} hours per week

Learning Style:
{learning_style}

Provide the response using these sections:

1. Career Analysis

Explain the student's current position
and what the target role requires.

2. Skill Gap Explanation

Explain the most important missing skills
and why they matter for the target role.

3. Personalized Learning Roadmap

Create a practical step-by-step roadmap.
Prioritize the most important missing skills.
Make the plan realistic for the available
study time.

4. Recommended Projects

Suggest practical projects that can strengthen
the student's portfolio.

5. Interview Preparation

Provide useful technical interview questions
and important topics to prepare.

6. Career Advice

Give practical advice about learning,
projects, portfolio building and interviews.

Requirements:

- Keep the explanation practical.
- Use clear and simple language.
- Prioritize important skills.
- Make the roadmap realistic.
- Suggest projects related to the target role.
- Include technical interview preparation.
- Do not claim that readiness scores guarantee employment.
- Do not invent job offers or employment guarantees.
"""

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional "
                        "AI career guidance assistant. "
                        "Give practical, personalized "
                        "and technically accurate advice."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,

            max_completion_tokens=2500
        )

        return response.choices[
            0
        ].message.content

    except Exception as error:

        return (
            "Unable to generate the AI response.\n\n"
            f"Error: {error}"
        )


if __name__ == "__main__":

    print(
        "======================================"
    )

    print(
        "       GROQ GENAI TEST"
    )

    print(
        "======================================"
    )

    result = generate_career_response(

        target_job="Data Scientist",

        current_skills=[
            "Python",
            "SQL",
            "Machine Learning",
            "Data Visualization"
        ],

        missing_skills=[
            "Statistics",
            "Data Preparation",
            "Predictive Modeling",
            "Data Mining",
            "AWS"
        ],

        study_time=10,

        experience_level="Beginner",

        learning_style="Project-Based"
    )

    print("\n")
    print(result)