from pydantic import BaseModel, Field
from typing import Optional

class ArticleRequest(BaseModel):
    """
    Pydantic model for validating the article generation request body.
    """
    topic: str = Field(..., description="The topic for the educational article.")
    difficulty: Optional[str] = Field("intermediate", description="The difficulty level of the article (e.g., beginner, intermediate, advanced).")
    audience: Optional[str] = Field("students", description="The target audience for the article (e.g., students, professionals, general public).")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "The Basics of Quantum Computing",
                "difficulty": "intermediate",
                "audience": "students"
            }
        }