"""Base models for agent state bridge"""
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Request model for agent chat endpoint"""
    message: str = Field(..., description="User message to the agent")
    state: Dict[str, Any] = Field(default_factory=dict, description="Application state")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Add product to cart",
                "state": {
                    "cart": {"items": [], "total": 0},
                    "user": {"id": "123"}
                }
            }
        }
    }


class AgentResponse(BaseModel):
    """Response model for agent chat endpoint"""
    response: str = Field(..., description="Agent response message")
    state: Optional[Dict[str, Any]] = Field(None, description="Updated application state (optional)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "response": "I've added the product to your cart!",
                "state": {"cart": {"items": [{"id": 1}], "total": 29.99}}
            }
        }
    }
