from pydantic import BaseModel, Field, field_validator, ConfigDict


class GreetingMessage(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "content": "Hello, World!"
            }
        }
    )
    
    content: str = Field(..., min_length=1, description="The greeting message content")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Greeting message cannot be empty or only whitespace")
        return v
    
    def to_dict(self) -> dict:
        return {"message": self.content}