from pydantic import BaseModel, Field


class SourceBundleData(BaseModel):
    short_description: str | None = None
    detailed_description: str | None = None
    review_summary: str | None = None
    official_genres: list[str] = Field(default_factory=list)
    official_categories: list[str] = Field(default_factory=list)
    popular_user_tags: list[str] = Field(default_factory=list)
    page_text: str | None = None
    source_urls: list[str] = Field(default_factory=list)
    extraction_notes: str | None = None
