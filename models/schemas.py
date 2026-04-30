"""
Shared Pydantic Models
Used across the application
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class OpportunityType(str, Enum):
    """Types of opportunities"""
    JOB = "job"
    INTERNSHIP = "internship"
    LEARNING = "learning"
    VOLUNTEERING = "volunteering"
    FREELANCE = "freelance"


class ExperienceLevel(str, Enum):
    """Experience levels"""
    FRESH = "fresh"
    JUNIOR = "junior"
    INTERMEDIATE = "intermediate"
    SENIOR = "senior"
    LEAD = "lead"


class Opportunity(BaseModel):
    """Opportunity data model"""
    id: str
    title: str
    company: str
    description: str
    location: str
    type: OpportunityType
    experience_level: ExperienceLevel
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    posted_date: datetime
    url: str
    source: str  # LinkedIn, Wuzzuf, ITI, etc.
    match_score: float = Field(default=0.0, le=100.0, ge=0.0)
    keywords: List[str] = []
    
    class Config:
        use_enum_values = True


class JobAlert(BaseModel):
    """Job alert configuration"""
    id: Optional[str] = None
    user_id: str
    keywords: List[str]
    location: str
    experience_level: Optional[ExperienceLevel] = None
    frequency: str = "instant"  # instant, daily, weekly
    active: bool = True
    created_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


class User(BaseModel):
    """User profile"""
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    skills: List[str] = []
    preferences: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    
    class Config:
        use_enum_values = True


class CareerPredictionResult(BaseModel):
    """Career prediction result"""
    user_id: Optional[str] = None
    primary_career: str
    confidence_score: float = Field(le=1.0, ge=0.0)
    alternative_careers: List[Dict[str, str]]
    recommended_skills: List[Dict[str, str]]
    learning_paths: List[str]
    predicted_at: datetime
    
    class Config:
        use_enum_values = True


class NotificationPreferences(BaseModel):
    """User notification preferences"""
    user_id: str
    email_enabled: bool = True
    push_enabled: bool = True
    whatsapp_enabled: bool = False
    telegram_enabled: bool = False
    sms_enabled: bool = False
    frequency: str = "instant"
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    
    class Config:
        use_enum_values = True


class Notification(BaseModel):
    """Notification data"""
    id: Optional[str] = None
    user_id: str
    type: str  # job_alert, learning, etc.
    title: str
    message: str
    data: Dict[str, Any]
    read: bool = False
    sent_at: datetime
    clicked_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True
