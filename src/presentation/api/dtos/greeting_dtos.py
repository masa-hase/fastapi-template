"""DTOs for greeting endpoints."""
from pydantic import BaseModel, Field, ConfigDict


class PersonalizedGreetingRequest(BaseModel):
    """Request model for personalized greeting."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alice",
                "language": "en"
            }
        }
    )
    
    name: str = Field(..., min_length=1, max_length=100, description="Name of the person to greet")
    language: str = Field(default="en", pattern="^(en|ja|es|fr)$", description="Language for the greeting")


class GreetingResponse(BaseModel):
    """Response model for greeting endpoint."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Hello, World!"
            }
        }
    )
    
    message: str = Field(..., description="The greeting message")