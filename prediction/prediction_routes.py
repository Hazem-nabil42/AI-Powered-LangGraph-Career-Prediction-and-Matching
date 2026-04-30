# prediction/prediction_routes.py
"""
API routes for career prediction
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from prediction.models.career_classifier import classifier

router = APIRouter(prefix="/prediction", tags=["prediction"])


class QuizResponse(BaseModel):
    """User's quiz responses"""
    responses: Dict[str, Any]
    user_id: str = None


class PredictionResult(BaseModel):
    """Prediction result"""
    primary_career: str
    confidence_score: float
    alternative_careers: List[str]
    recommended_skills: List[Dict[str, str]]
    learning_paths: List[str]


@router.post("/quiz")
async def submit_quiz(data: QuizResponse) -> PredictionResult:
    """
    Submit quiz responses and get career prediction
    
    Args:
        data: User's quiz responses
        
    Returns:
        Prediction result with career recommendations
    """
    try:
        # Load model if not loaded
        if classifier.model is None:
            classifier.load_model()
        
        # Get prediction
        primary_career, confidence, alternatives = classifier.predict_career(data.responses)
        
        # Get recommended skills
        recommended_skills = get_recommended_skills(primary_career)
        
        # Get learning paths
        learning_paths = get_learning_paths(primary_career)
        
        return PredictionResult(
            primary_career=primary_career,
            confidence_score=confidence,
            alternative_careers=alternatives,
            recommended_skills=recommended_skills,
            learning_paths=learning_paths
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/skills/{career}")
async def get_skills(career: str):
    """Get recommended skills for a career"""
    return get_recommended_skills(career)


@router.get("/paths/{career}")
async def get_paths(career: str):
    """Get learning paths for a career"""
    return get_learning_paths(career)


# Helper functions
def get_recommended_skills(career: str) -> List[Dict[str, str]]:
    """Get recommended skills for a career path"""
    skills_map = {
        "Software Development": [
            {"skill": "Python", "demand": "90%"},
            {"skill": "APIs & Databases", "demand": "88%"},
            {"skill": "Cloud (AWS/GCP)", "demand": "85%"},
            {"skill": "DevOps/CI-CD", "demand": "82%"},
        ],
        "Data Science": [
            {"skill": "Python/R", "demand": "92%"},
            {"skill": "Machine Learning", "demand": "90%"},
            {"skill": "Data Visualization", "demand": "85%"},
            {"skill": "SQL", "demand": "88%"},
        ],
        "UX/UI Design": [
            {"skill": "Figma", "demand": "85%"},
            {"skill": "Prototyping", "demand": "80%"},
            {"skill": "User Research", "demand": "78%"},
            {"skill": "CSS/HTML", "demand": "70%"},
        ]
    }
    
    return skills_map.get(career, [])


def get_learning_paths(career: str) -> List[str]:
    """Get recommended learning paths"""
    paths_map = {
        "Software Development": [
            "Backend with Python/Django",
            "Full Stack with React & Node.js",
            "Mobile Development with React Native",
            "DevOps Engineering"
        ],
        "Data Science": [
            "Machine Learning Specialization",
            "Data Engineering Path",
            "Analytics Engineering",
            "AI & Deep Learning"
        ]
    }
    
    return paths_map.get(career, [])
