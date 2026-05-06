from typing import Any

from pydantic import BaseModel, Field


class RetrievedGRSContext(BaseModel):
    allowed_tags: list[str] = Field(default_factory=list)
    tag_definitions: list[dict[str, Any]] = Field(default_factory=list)
    weight_scale: dict[str, Any] = Field(default_factory=dict)
    tag_combination_rules: dict[str, Any] = Field(default_factory=dict)
    modeling_examples: list[dict[str, Any]] = Field(default_factory=list)
    context_notes: str
