from typing import List, Optional
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.core.career_engine import create_career_plan
from backend.ai.genai import generate_career_response


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="GenAI Career Navigator API",
    description=(
        "AI-powered skill gap analysis and "
        "personalized career roadmap system."
    ),
    version="1.0.0",
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST MODELS
# ==========================================

class AnalyzeRequest(BaseModel):

    target_job: str = Field(
        ...,
        min_length=1
    )

    current_skills: List[str] = Field(
        default_factory=list
    )

    study_time: int = Field(
        default=10,
        ge=1,
        le=60
    )

    experience_level: str = "Beginner"

    learning_style: str = "Project-Based"


class AIRequest(BaseModel):

    target_job: str = Field(
        ...,
        min_length=1
    )

    current_skills: List[str] = Field(
        default_factory=list
    )

    missing_skills: Optional[List[str]] = None

    study_time: int = Field(
        default=10,
        ge=1,
        le=60
    )

    experience_level: str = "Beginner"

    learning_style: str = "Project-Based"


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def root():

    return {
        "message": "GenAI Career Navigator API is running",
        "status": "healthy",
        "version": "1.0.0",
    }


# ==========================================
# GET ALL JOB ROLES
# ==========================================

@app.get("/roles")
def get_roles():

    roles_file = Path("data/career_roles.json")

    try:

        with open(
            roles_file,
            "r",
            encoding="utf-8"
        ) as file:

            roles = json.load(file)

        return {
            "roles": roles
        }

    except FileNotFoundError:

        raise HTTPException(
            status_code=500,
            detail="career_roles.json file was not found."
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="career_roles.json contains invalid JSON."
        )


# ==========================================
# ANALYZE CAREER
# ==========================================

@app.post("/analyze")
def analyze_career(
    request: AnalyzeRequest
):

    try:

        result = create_career_plan(

            target_job=request.target_job,

            current_skills=request.current_skills,

            study_time=request.study_time,

            experience_level=request.experience_level,

            learning_style=request.learning_style,
        )

        if result is None:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Target job "
                    f"'{request.target_job}' "
                    f"was not found."
                )
            )

        return {
            "success": True,
            "data": result,
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Career analysis failed: "
                f"{error}"
            )
        )


# ==========================================
# GENERATE AI CAREER PLAN
# ==========================================

@app.post("/generate-ai")
def generate_ai_plan(
    request: AIRequest
):

    try:

        missing_skills = request.missing_skills

        # If missing skills were not provided,
        # calculate them automatically.
        if missing_skills is None:

            career_result = create_career_plan(

                target_job=request.target_job,

                current_skills=request.current_skills,

                study_time=request.study_time,

                experience_level=request.experience_level,

                learning_style=request.learning_style,
            )

            if career_result is None:

                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Target job "
                        f"'{request.target_job}' "
                        f"was not found."
                    )
                )

            missing_skills = career_result[
                "missing_skills"
            ]

        # Generate personalized GenAI response
        ai_response = generate_career_response(

            target_job=request.target_job,

            current_skills=request.current_skills,

            missing_skills=missing_skills,

            study_time=request.study_time,

            experience_level=request.experience_level,

            learning_style=request.learning_style,
        )

        return {
            "success": True,
            "target_job": request.target_job,
            "response": ai_response,
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"AI generation failed: "
                f"{error}"
            )
        )


# ==========================================
# SERVER TEST
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )