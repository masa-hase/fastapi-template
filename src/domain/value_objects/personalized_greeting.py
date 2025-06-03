from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal


class PersonalizedGreeting(BaseModel):
    """Value object for personalized greeting."""
    
    model_config = ConfigDict(frozen=True)
    
    name: str = Field(..., min_length=1, max_length=100)
    language: Literal["en", "ja", "es", "fr"] = Field(default="en")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or only whitespace")
        return v
    
    def generate_message(self) -> str:
        """Generate greeting message based on language."""
        greetings = {
            "en": f"Hello, {self.name}!",
            "ja": f"こんにちは、{self.name}さん！",
            "es": f"¡Hola, {self.name}!",
            "fr": f"Bonjour, {self.name}!"
        }
        return greetings[self.language]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for response."""
        return {"message": self.generate_message()}