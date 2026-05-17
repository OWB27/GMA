from app.chains.source_assessment_chain import SourceAssessmentChain
from app.schemas.source_assessment import SourceAssessment


class FakeRunnable:
    def __init__(self) -> None:
        self.input = None

    def invoke(self, input):
        self.input = input
        return SourceAssessment(
            is_sufficient=True,
            confidence=0.82,
            missing_information=[],
            reason="Official description and Steam tags are enough.",
            recommended_action="continue_modeling",
            recommended_query=None,
        )


def test_source_assessment_chain_passes_source_bundle_to_runnable() -> None:
    fake_runnable = FakeRunnable()
    chain = SourceAssessmentChain(runnable=fake_runnable)

    result = chain.invoke(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
        source_bundle={"short_description": "Mock source."},
    )

    assert result.is_sufficient is True
    assert fake_runnable.input["game_name"] == "Hades"
    assert '"short_description": "Mock source."' in fake_runnable.input["source_bundle"]
