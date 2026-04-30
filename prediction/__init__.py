# prediction/__init__.py
"""Career Prediction Module"""

from prediction.models.career_classifier import classifier
from prediction.prediction_routes import router

__all__ = ['classifier', 'router']
