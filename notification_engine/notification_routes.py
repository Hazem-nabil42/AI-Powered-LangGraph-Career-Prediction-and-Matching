# notification_engine/notification_routes.py
"""
API routes for Notification Management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from notification_engine.n8n_integration import (
    n8n_manager,
    NotificationType,
    NotificationChannel
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationRequest(BaseModel):
    """Send a notification"""
    user_id: str
    notification_type: str
    channels: List[str]
    data: Dict
    scheduled_at: Optional[str] = None


class JobAlertConfig(BaseModel):
    """Job alert configuration"""
    user_id: str
    keywords: List[str]
    location: str
    experience_level: str
    frequency: str = "instant"


class DigestConfig(BaseModel):
    """Daily digest configuration"""
    user_id: str
    digest_time: str
    categories: List[str]


class NotificationSettings(BaseModel):
    """User notification settings"""
    user_id: str
    email_enabled: bool = True
    push_enabled: bool = True
    whatsapp_enabled: bool = False
    telegram_enabled: bool = False
    frequency: str = "instant"  # instant, daily, weekly


@router.post("/send")
async def send_notification(data: NotificationRequest):
    """
    Send a notification via n8n
    
    Args:
        data: Notification details
        
    Returns:
        Notification send result
    """
    try:
        # Convert string types to enums
        notif_type = NotificationType(data.notification_type)
        channels = [NotificationChannel(c) for c in data.channels]
        
        # Send via n8n
        result = n8n_manager.send_notification(
            user_id=data.user_id,
            notification_type=notif_type,
            channels=channels,
            data=data.data,
            scheduled_at=data.scheduled_at
        )
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/job-alert")
async def create_job_alert(config: JobAlertConfig):
    """
    Create a job alert workflow
    
    Args:
        config: Job alert configuration
        
    Returns:
        Workflow creation result
    """
    try:
        criteria = {
            "keywords": config.keywords,
            "location": config.location,
            "experience_level": config.experience_level
        }
        
        result = n8n_manager.schedule_job_alert(
            user_id=config.user_id,
            criteria=criteria,
            frequency=config.frequency
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/daily-digest")
async def create_daily_digest(config: DigestConfig):
    """
    Create a daily digest workflow
    
    Args:
        config: Digest configuration
        
    Returns:
        Workflow creation result
    """
    try:
        result = n8n_manager.create_daily_digest(
            user_id=config.user_id,
            digest_time=config.digest_time
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/settings")
async def update_notification_settings(settings: NotificationSettings):
    """
    Update user notification settings
    
    Args:
        settings: Notification preferences
        
    Returns:
        Updated settings
    """
    try:
        # TODO: Save to database
        # This would typically update user preferences in a database
        
        return {
            "status": "success",
            "message": "Notification settings updated",
            "settings": settings
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/register")
async def register_webhook(webhook_id: str, webhook_url: str, event_types: List[str]):
    """
    Register a webhook for n8n events
    
    Args:
        webhook_id: ID of the webhook
        webhook_url: URL to receive events
        event_types: Types of events to listen for
        
    Returns:
        Webhook registration result
    """
    try:
        result = n8n_manager.register_webhook(
            webhook_id=webhook_id,
            webhook_url=webhook_url,
            event_types=event_types
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """
    Get status of an n8n workflow
    
    Args:
        workflow_id: ID of the workflow
        
    Returns:
        Workflow status
    """
    try:
        result = n8n_manager.get_workflow_status(workflow_id)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sources")
async def get_active_sources():
    """
    Get list of active notification sources
    
    Returns:
        List of notification sources and their status
    """
    return {
        "sources": {
            "email": {"enabled": True, "status": "active"},
            "push": {"enabled": True, "status": "active"},
            "whatsapp": {"enabled": False, "status": "inactive"},
            "telegram": {"enabled": False, "status": "inactive"}
        }
    }


@router.get("/alerts")
async def get_user_alerts(user_id: str):
    """
    Get all active alerts for a user
    
    Args:
        user_id: User ID
        
    Returns:
        List of active alerts
    """
    # TODO: Fetch from database
    return {
        "alerts": [
            {
                "id": "alert_1",
                "type": "job",
                "criteria": {"keywords": ["Python", "Developer"], "location": "Cairo"},
                "frequency": "instant",
                "created_at": "2024-01-15T10:00:00"
            }
        ]
    }
