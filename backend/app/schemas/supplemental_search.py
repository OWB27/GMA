from pydantic import BaseModel, Field


class SupplementalSource(BaseModel):
    title: str = Field(default="")
    url: str = Field(default="")
    content: str = Field(default="")


class SupplementalSearchResult(BaseModel):
    query: str
    sources: list[SupplementalSource] = Field(default_factory=list)
    skipped_reason: str | None = None
