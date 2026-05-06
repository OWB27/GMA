from app.services.modeling_validation.modeling_result_validator import ModelingResultValidator


def _context():
    return {
        "allowed_tags": [
            "combat",
            "challenge",
            "relaxed",
            "horror_tension",
            "story_rich",
        ],
        "tag_combination_rules": {
            "rules": [
                {
                    "rule_id": "relaxed_vs_horror_tension",
                    "type": "soft_conflict",
                    "tags": ["relaxed", "horror_tension"],
                }
            ]
        },
    }


def _tag(tag_code: str, weight: int = 3, confidence: float = 0.8):
    return {
        "tag_code": tag_code,
        "suggested_weight": weight,
        "confidence": confidence,
        "evidence_snippets": [{"en": "Mock evidence.", "zh": "Mock evidence zh."}],
        "reason": {"en": "Mock reason.", "zh": "Mock reason zh."},
    }


def test_validator_accepts_valid_modeling_result() -> None:
    result = ModelingResultValidator().validate(
        modeling_result={
            "overall_summary": "A valid draft.",
            "selected_existing_tags": [
                _tag("combat"),
                _tag("challenge"),
                _tag("story_rich"),
            ],
            "warnings": [],
        },
        retrieved_context=_context(),
    )

    assert result.is_valid is True
    assert result.errors == []


def test_validator_rejects_unknown_and_duplicate_tags() -> None:
    result = ModelingResultValidator().validate(
        modeling_result={
            "overall_summary": "An invalid draft.",
            "selected_existing_tags": [
                _tag("combat"),
                _tag("combat"),
                _tag("new_tag"),
            ],
            "warnings": [],
        },
        retrieved_context=_context(),
    )

    assert result.is_valid is False
    assert "Duplicate tag_code: combat." in result.errors
    assert "Unknown tag_code: new_tag." in result.errors


def test_validator_warns_about_soft_conflicts_and_low_confidence() -> None:
    result = ModelingResultValidator().validate(
        modeling_result={
            "overall_summary": "A reviewable draft.",
            "selected_existing_tags": [
                _tag("relaxed", weight=4, confidence=0.9),
                _tag("horror_tension", weight=4, confidence=0.9),
                _tag("combat", weight=3, confidence=0.4),
            ],
            "warnings": [],
        },
        retrieved_context=_context(),
    )

    assert result.is_valid is True
    assert any("Soft conflict relaxed_vs_horror_tension" in warning for warning in result.warnings)
    assert "Low confidence for tag_code combat: 0.4." in result.warnings


def test_validator_rejects_schema_invalid_result() -> None:
    result = ModelingResultValidator().validate(
        modeling_result={
            "overall_summary": "Invalid schema.",
            "selected_existing_tags": [
                {
                    "tag_code": "combat",
                    "suggested_weight": 9,
                    "confidence": 2,
                    "evidence_snippets": [],
                    "reason": {"en": "", "zh": ""},
                }
            ],
            "warnings": [],
        },
        retrieved_context=_context(),
    )

    assert result.is_valid is False
    assert result.errors[0].startswith("modeling_result schema validation failed:")
