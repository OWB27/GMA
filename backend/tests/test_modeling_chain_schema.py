import pytest
from pydantic import ValidationError

from app.schemas.modeling_output import ModelingResult


def test_modeling_result_schema_accepts_valid_output() -> None:
    result = ModelingResult.model_validate(
        {
            "overall_summary": "A fast action game with strong combat evidence.",
            "selected_existing_tags": [
                {
                    "tag_code": "combat",
                    "suggested_weight": 4,
                    "confidence": 0.82,
                    "evidence_snippets": [
                        {
                            "en": "Steam description mentions responsive combat.",
                            "zh": "Steam 描述提到了响应迅速的战斗。",
                        }
                    ],
                    "reason": {
                        "en": "Combat is a major repeated gameplay activity.",
                        "zh": "战斗是主要且反复出现的游玩活动。",
                    },
                }
            ],
            "warnings": [],
        }
    )

    assert result.selected_existing_tags[0].tag_code == "combat"


def test_modeling_result_schema_rejects_invalid_weight_and_confidence() -> None:
    with pytest.raises(ValidationError):
        ModelingResult.model_validate(
            {
                "overall_summary": "Invalid result.",
                "selected_existing_tags": [
                    {
                        "tag_code": "combat",
                        "suggested_weight": 6,
                        "confidence": 1.5,
                        "evidence_snippets": [],
                        "reason": {"en": "", "zh": ""},
                    }
                ],
                "warnings": [],
            }
        )
