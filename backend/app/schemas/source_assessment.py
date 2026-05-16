from pydantic import BaseModel, Field


class SourceAssessment(BaseModel):
    is_sufficient: bool
    confidence: float = Field(ge=0, le=1)
    missing_information: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1)
    recommended_action: str = Field(pattern="^(continue_modeling|fetch_supplemental_sources)$")
