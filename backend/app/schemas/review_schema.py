from pydantic import BaseModel, Field
from datetime import datetime


class CodeReviewRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description="Python code to review"
    )


class CodeReviewResponse(BaseModel):
    id: int
    code: str
    review: str
    created_at: datetime

    class Config:
        from_attributes = True