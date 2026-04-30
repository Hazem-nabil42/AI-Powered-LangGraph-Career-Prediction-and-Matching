# notification_engine/n8n_integration.py
"""
n8n Integration for Intelligent Notification Management
Handles webhook integration with n8n automation workflows
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

N8N_BASE_URL = os.getenv("N8N_BASE_URL", "http://localhost:5678")
N8N_API_KEY = os.getenv("N8N_API_KEY")


class NotificationType(str, Enum):
    """Types of notifications"""
    JOB_ALERT = "job_alert"
    INTERNSHIP = "internship"
    LEARNING_OPPORTUNITY = "learning"
    VOLUNTEERING = "volunteering"
    SKILL_MATCH = "skill_match"


class NotificationChannel(str, Enum):
    """Notification delivery channels"""
    EMAIL = "email"
    PUSH = "push"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    IN_APP = "in_app"


class N8NIntegration:
    """
    n8n Workflow Integration for notifications
    Manages automated workflows and webhook triggers
    """
    
    def __init__(self):
        self.base_url = N8N_BASE_URL
        self.api_key = N8N_API_KEY
        self.workflows = {}
        self.webhook_endpoints = {}
    
    def trigger_workflow(
        self,
        workflow_id: str,
        payload: Dict[str, Any],
        async_execution: bool = False
    ) -> Dict:
        """
        Trigger an n8n workflow
        
        Args:
            workflow_id: ID of the workflow to trigger
            payload: Data to send to the workflow
            async_execution: Whether to execute asynchronously
            
        Returns:
            Workflow execution result
        """
        try:
            url = f"{self.base_url}/api/v1/workflows/{workflow_id}/execute"
            
            headers = {
                "X-N8N-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "execution_id": response.json().get("executionId"),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": response.text,
                    "code": response.status_code
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def send_notification(
        self,
        user_id: str,
        notification_type: NotificationType,
        channels: List[NotificationChannel],
        data: Dict[str, Any],
        scheduled_at: Optional[str] = None
    ) -> Dict:
        """
        Send notification via n8n workflow
        
        Args:
            user_id: Target user ID
            notification_type: Type of notification
            channels: Delivery channels
            data: Notification data
            scheduled_at: ISO timestamp for scheduled delivery
            
        Returns:
            Notification send result
        """
        
        payload = {
            "user_id": user_id,
            "notification_type": notification_type.value,
            "channels": [c.value for c in channels],
            "data": data,
            "scheduled_at": scheduled_at,
            "sent_at": datetime.now().isoformat()
        }
        
        # Trigger n8n "Send Notification" workflow
        return self.trigger_workflow("notification_sender", payload)
    
    def schedule_job_alert(
        self,
        user_id: str,
        criteria: Dict,
        frequency: str = "instant"  # instant, daily, weekly
    ) -> Dict:
        """
        Schedule a job alert workflow
        
        Args:
            user_id: User ID
            criteria: Job search criteria (keywords, location, etc.)
            frequency: Alert frequency
            
        Returns:
            Workflow creation result
        """
        
        payload = {
            "user_id": user_id,
            "criteria": criteria,
            "frequency": frequency,
            "created_at": datetime.now().isoformat()
        }
        
        return self.trigger_workflow("job_alert_scheduler", payload)
    
    def create_daily_digest(
        self,
        user_id: str,
        digest_time: str = "09:00"  # HH:MM format
    ) -> Dict:
        """
        Create a daily digest workflow
        
        Args:
            user_id: User ID
            digest_time: Time to send digest (24-hour format)
            
        Returns:
            Workflow creation result
        """
        
        payload = {
            "user_id": user_id,
            "digest_time": digest_time,
            "created_at": datetime.now().isoformat()
        }
        
        return self.trigger_workflow("daily_digest_creator", payload)
    
    def register_webhook(
        self,
        webhook_id: str,
        webhook_url: str,
        event_types: List[str]
    ) -> Dict:
        """
        Register a webhook for n8n events
        
        Args:
            webhook_id: ID of the webhook
            webhook_url: URL to receive webhook events
            event_types: Types of events to listen for
            
        Returns:
            Registration result
        """
        
        try:
            url = f"{self.base_url}/api/v1/webhooks"
            
            headers = {
                "X-N8N-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "webhook_id": webhook_id,
                "webhook_url": webhook_url,
                "event_types": event_types,
                "registered_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.webhook_endpoints[webhook_id] = webhook_url
                return {
                    "status": "success",
                    "webhook_id": webhook_id
                }
            else:
                return {
                    "status": "error",
                    "error": response.text
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get the status of a workflow"""
        
        try:
            url = f"{self.base_url}/api/v1/workflows/{workflow_id}"
            
            headers = {"X-N8N-API-KEY": self.api_key}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "workflow": response.json()
                }
            else:
                return {
                    "status": "error",
                    "error": response.text
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Singleton instance
n8n_manager = N8NIntegration()
