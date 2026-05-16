from app.graph import nodes
from app.graph.state import create_initial_state
from app.schemas.modeling_output import ModelingResult
from app.schemas.source_assessment import SourceAssessment


class FakeModelingChain:
    def invoke(self, game_name, steam_url, source_bundle, retrieved_context):
        return ModelingResult(
            overall_summary=f"Modeled {game_name}.",
            selected_existing_tags=[
                {
                    "tag_code": "combat",
                    "suggested_weight": 4,
                    "confidence": 0.8,
                    "evidence_snippets": [{"en": "Mock evidence.", "zh": "Mock evidence zh."}],
                    "reason": {"en": "Mock reason.", "zh": "Mock reason zh."},
                }
            ],
            warnings=[],
        )


class FailingModelingChain:
    def invoke(self, game_name, steam_url, source_bundle, retrieved_context):
        raise ValueError("LLM provider rejected the structured output request.")


class FakeSourceAssessmentChain:
    def invoke(self, game_name, steam_url, source_bundle):
        return SourceAssessment(
            is_sufficient=True,
            confidence=0.86,
            missing_information=[],
            reason="Official Steam evidence is enough.",
            recommended_action="continue_modeling",
        )


class FailingSourceAssessmentChain:
    def invoke(self, game_name, steam_url, source_bundle):
        raise ValueError("LLM provider failed.")


def test_assess_source_sufficiency_node_uses_structured_assessment_chain(monkeypatch) -> None:
    monkeypatch.setattr(nodes, "SourceAssessmentChain", lambda: FakeSourceAssessmentChain())
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["source_bundle"] = {"short_description": "Mock source."}

    result = nodes.assess_source_sufficiency_node(state)

    assert result["status"] == "source_assessed"
    assert result["source_assessment"]["is_sufficient"] is True
    assert result["source_assessment"]["recommended_action"] == "continue_modeling"
    assert result["trace"][0]["node"] == "assess_source_sufficiency"


def test_assess_source_sufficiency_node_falls_back_when_llm_call_fails(monkeypatch) -> None:
    monkeypatch.setattr(nodes, "SourceAssessmentChain", lambda: FailingSourceAssessmentChain())
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["source_bundle"] = {"short_description": "Mock source."}

    result = nodes.assess_source_sufficiency_node(state)

    assert result["status"] == "source_assessed"
    assert result["source_assessment"]["is_sufficient"] is True
    assert result["source_assessment"]["confidence"] == 0.5
    assert result["source_assessment"]["recommended_action"] == "continue_modeling"


def test_assess_source_sufficiency_node_fails_without_source_bundle() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    result = nodes.assess_source_sufficiency_node(state)

    assert result["status"] == "failed"
    assert "source_bundle is required before source assessment." in result["errors"]


def test_model_game_tags_node_uses_structured_modeling_chain(monkeypatch) -> None:
    monkeypatch.setattr(nodes, "ModelingChain", lambda: FakeModelingChain())
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["source_bundle"] = {"short_description": "Mock source."}
    state["retrieved_context"] = {"allowed_tags": ["combat"]}

    result = nodes.model_game_tags_node(state)

    assert result["status"] == "modeled"
    assert result["modeling_result"]["selected_existing_tags"][0]["tag_code"] == "combat"
    assert result["trace"][0]["node"] == "model_game_tags"


def test_model_game_tags_node_fails_without_required_inputs() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    result = nodes.model_game_tags_node(state)

    assert result["status"] == "failed"
    assert "source_bundle is required before modeling." in result["errors"]


def test_model_game_tags_node_returns_failed_state_when_llm_call_fails(monkeypatch) -> None:
    monkeypatch.setattr(nodes, "ModelingChain", lambda: FailingModelingChain())
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["source_bundle"] = {"short_description": "Mock source."}
    state["retrieved_context"] = {"allowed_tags": ["combat"]}

    result = nodes.model_game_tags_node(state)

    assert result["status"] == "failed"
    assert "model_game_tags failed:" in result["errors"][0]
    assert result["trace"][0]["node"] == "model_game_tags"


def test_validate_result_node_marks_invalid_result_for_review() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["modeling_result"] = {
        "overall_summary": "Invalid draft.",
        "selected_existing_tags": [
            {
                "tag_code": "not_allowed",
                "suggested_weight": 3,
                "confidence": 0.8,
                "evidence_snippets": [{"en": "Mock evidence.", "zh": "Mock evidence zh."}],
                "reason": {"en": "Mock reason.", "zh": "Mock reason zh."},
            }
        ],
        "warnings": [],
    }
    state["retrieved_context"] = {
        "allowed_tags": ["combat"],
        "tag_combination_rules": {"rules": []},
    }

    result = nodes.validate_result_node(state)

    assert result["status"] == "validation_failed"
    assert result["validation_result"]["is_valid"] is False
    assert "Unknown tag_code: not_allowed." in result["errors"]
