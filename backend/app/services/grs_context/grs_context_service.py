from app.schemas.grs_context import RetrievedGRSContext
from app.services.grs_context.rule_pack_loader import RulePackLoader


class GRSContextService:
    def __init__(self, rule_pack_loader: RulePackLoader | None = None) -> None:
        self.rule_pack_loader = rule_pack_loader or RulePackLoader()

    def retrieve_context(self) -> RetrievedGRSContext:
        rule_pack = self.rule_pack_loader.load()
        tag_definitions = rule_pack["tag_definitions"]

        return RetrievedGRSContext(
            allowed_tags=[definition["code"] for definition in tag_definitions],
            tag_definitions=tag_definitions,
            weight_scale=rule_pack["weight_scale"],
            tag_combination_rules=rule_pack["tag_combination_rules"],
            modeling_examples=rule_pack["modeling_examples"],
            context_notes="Loaded from modeling_context/rules with lightweight validation.",
        )
