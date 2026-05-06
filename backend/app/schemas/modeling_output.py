from pydantic import BaseModel, Field


class LocalizedText(BaseModel):
    en: str = Field(min_length=1)
    zh: str = Field(min_length=1)


class SelectedTagSuggestion(BaseModel):
    tag_code: str = Field(min_length=1)
    suggested_weight: int = Field(ge=1, le=5)
    confidence: float = Field(ge=0, le=1)
    evidence_snippets: list[LocalizedText] = Field(default_factory=list, min_length=1)
    reason: LocalizedText


class ModelingResult(BaseModel):
    overall_summary: str = Field(min_length=1)
    selected_existing_tags: list[SelectedTagSuggestion] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
