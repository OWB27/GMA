from app.graph import nodes
from app.graph.state import create_initial_state
from app.schemas.modeling_output import ModelingResult


class FakeModelingChain:
    def invoke(self, game_name, steam_url, source_bundle, retrieved_context):
        return ModelingResult(
            overall_summary=f"Modeled {game_name}.",
            selected_existing_tags=[
                {
                    "tag_code": "combat",
                    "suggested_weight": 4,
                    "confidence": 0.8,
                    "evidence_snippets": [{"en": "Mock evidence.", "zh": "模拟证据。"}],
                    "reason": {"en": "Mock reason.", "zh": "模拟理由。"},
                }
            ],
            warnings=[],
        )


class FailingModelingChain:
    def invoke(self, game_name, steam_url, source_bundle, retrieved_context):
        raise ValueError("LLM provider rejected the structured output request.")


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
