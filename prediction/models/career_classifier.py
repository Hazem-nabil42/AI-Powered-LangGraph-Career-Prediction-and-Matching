# prediction/models/career_classifier.py
"""
Career Prediction Model using Classification
Predicts user career preferences based on responses
"""

from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from typing import Dict, List, Tuple

class CareerClassifier:
    def __init__(self):
        self.model = None
        self.model_path = "prediction/models/career_model.pkl"
        self.label_encoder = None
        
    def load_model(self):
        """Load pre-trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
    
    def predict_career(self, responses: Dict) -> Tuple[str, float, List[str]]:
        """
        Predict career path based on user responses
        
        Args:
            responses: Dict of user quiz responses
            
        Returns:
            (primary_career, confidence_score, alternative_careers)
        """
        # Process responses into features
        features = self._process_responses(responses)
        
        # Make prediction
        prediction = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features]).max()
        
        # Get alternatives
        alternatives = self._get_alternatives(features)
        
        return prediction, confidence, alternatives
    
    def _process_responses(self, responses: Dict) -> List[float]:
        """Convert quiz responses to ML features"""
        # TODO: Implement feature engineering based on quiz questions
        pass
    
    def _get_alternatives(self, features: List[float]) -> List[str]:
        """Get alternative career paths"""
        # TODO: Get top N predictions
        pass
    
    def train(self, X_train, y_train):
        """Train the model"""
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, self.model_path)


# Export
classifier = CareerClassifier()
