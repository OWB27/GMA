from app.chains.modeling_chain import ModelingChain
from app.schemas.modeling_output import ModelingResult


class FakeRunnable:
    def __init__(self) -> None:
        self.input = None

    def invoke(self, input):
        self.input = input
        return ModelingResult(
            overall_summary="Mock structured modeling result.",
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


def test_modeling_chain_passes_source_and_context_to_runnable() -> None:
    fake_runnable = FakeRunnable()
    chain = ModelingChain(runnable=fake_runnable)

    result = chain.invoke(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
        source_bundle={"short_description": "Mock source."},
        retrieved_context={"allowed_tags": ["combat"]},
    )

    assert result.overall_summary == "Mock structured modeling result."
    assert fake_runnable.input["game_name"] == "Hades"
    assert '"short_description": "Mock source."' in fake_runnable.input["source_bundle"]
    assert '"allowed_tags": [' in fake_runnable.input["retrieved_context"]
