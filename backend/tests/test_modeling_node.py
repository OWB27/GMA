from app.graph import nodes
from app.graph.state import create_initial_state
from app.schemas.modeling_output import ModelingResult
from app.schemas.source_assessment import SourceAssessment
from app.schemas.supplemental_search import SupplementalSearchResult, SupplementalSource


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
            recommended_query=None,
        )


class FailingSourceAssessmentChain:
    def invoke(self, game_name, steam_url, source_bundle):
        raise ValueError("LLM provider failed.")


class SearchThenSufficientAssessmentChain:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, game_name, steam_url, source_bundle):
        self.calls += 1
        if self.calls == 1:
            return SourceAssessment(
                is_sufficient=False,
                confidence=0.52,
                missing_information=["Core gameplay loop is unclear."],
                reason="Steam evidence is too thin.",
                recommended_action="fetch_supplemental_sources",
                recommended_query="Hades gameplay features official sources",
            )
        return SourceAssessment(
            is_sufficient=True,
            confidence=0.78,
            missing_information=[],
            reason="Supplemental source clarified the gameplay loop.",
            recommended_action="continue_modeling",
            recommended_query=None,
        )


class FakeSupplementalSearchTool:
    def invoke(self, game_name, steam_url, query):
        return SupplementalSearchResult(
            query=query or "fallback query",
            sources=[
                SupplementalSource(
                    title="Gameplay overview",
                    url="https://example.com/hades",
                    content="Fast combat, repeated runs, and build variety.",
                )
            ],
        )


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


def test_assess_source_sufficiency_node_can_call_supplemental_search_tool_once(monkeypatch) -> None:
    fake_assessment_chain = SearchThenSufficientAssessmentChain()
    monkeypatch.setattr(nodes, "SourceAssessmentChain", lambda: fake_assessment_chain)
    monkeypatch.setattr(nodes, "SupplementalSearchTool", lambda: FakeSupplementalSearchTool())
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["source_bundle"] = {
        "page_text": "Official Steam text.",
        "source_urls": ["https://store.steampowered.com/app/1145360/Hades/"],
        "extraction_notes": "Official Steam data.",
    }

    result = nodes.assess_source_sufficiency_node(state)

    assert fake_assessment_chain.calls == 2
    assert result["status"] == "source_assessed"
    assert result["source_assessment"]["is_sufficient"] is True
    assert result["source_bundle"]["supplemental_sources"][0]["url"] == "https://example.com/hades"
    assert "Fast combat" in result["source_bundle"]["page_text"]
    assert [event["node"] for event in result["trace"]] == [
        "assess_source_sufficiency",
        "assess_source_sufficiency",
    ]


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
