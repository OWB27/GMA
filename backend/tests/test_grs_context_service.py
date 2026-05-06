from app.services.grs_context.grs_context_service import GRSContextService
from app.services.grs_context.rule_pack_loader import EXPECTED_TAGS


def test_grs_context_service_returns_retrieved_context() -> None:
    context = GRSContextService().retrieve_context()

    assert set(context.allowed_tags) == EXPECTED_TAGS
    assert len(context.tag_definitions) == 20
    assert context.weight_scale["scale"] == "1-5"
    assert "rules" in context.tag_combination_rules
    assert len(context.modeling_examples) > 0
    assert context.context_notes == "Loaded from modeling_context/rules with lightweight validation."
