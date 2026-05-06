import json
from pathlib import Path
from typing import Any


EXPECTED_TAGS = {
    "story_rich",
    "character_growth",
    "open_world",
    "exploration",
    "fast_paced",
    "combat",
    "challenge",
    "competitive",
    "relaxed",
    "choices_matter",
    "immersive",
    "strategy",
    "resource_management",
    "build_variety",
    "replayable",
    "cozy",
    "puzzle_solving",
    "survival",
    "social_sim",
    "horror_tension",
}


class RulePackValidationError(ValueError):
    pass


class RulePackLoader:
    def __init__(self, rules_dir: Path | None = None) -> None:
        self.rules_dir = rules_dir or self._default_rules_dir()

    def load(self) -> dict[str, Any]:
        rule_pack = {
            "tag_definitions": self._read_json("tag_definitions.json"),
            "weight_scale": self._read_json("weight_scale.json"),
            "tag_combination_rules": self._read_json("tag_combination_rules.json"),
            "modeling_examples": self._read_json("modeling_examples.json"),
        }
        self.validate(rule_pack)
        return rule_pack

    def validate(self, rule_pack: dict[str, Any]) -> None:
        tag_definitions = rule_pack["tag_definitions"]
        if not isinstance(tag_definitions, list):
            raise RulePackValidationError("tag_definitions.json must contain a list.")

        tag_codes = {definition.get("code") for definition in tag_definitions}
        if tag_codes != EXPECTED_TAGS:
            missing = sorted(EXPECTED_TAGS - tag_codes)
            extra = sorted(tag_codes - EXPECTED_TAGS)
            raise RulePackValidationError(
                f"Tag definitions do not match expected GRS tags. Missing={missing}, extra={extra}."
            )

        self._validate_weight_scale(rule_pack["weight_scale"])
        self._validate_combination_rules(rule_pack["tag_combination_rules"])
        self._validate_modeling_examples(rule_pack["modeling_examples"])

    def _read_json(self, filename: str) -> Any:
        path = self.rules_dir / filename
        if not path.exists():
            raise RulePackValidationError(f"Missing rule pack file: {path}")

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise RulePackValidationError(f"Invalid JSON in {path}: {error}") from error

    def _validate_weight_scale(self, weight_scale: dict[str, Any]) -> None:
        rules = weight_scale.get("rules")
        if not isinstance(rules, list):
            raise RulePackValidationError("weight_scale.json must contain rules list.")

        weights = {rule.get("weight") for rule in rules}
        if weights != {1, 2, 3, 4, 5}:
            raise RulePackValidationError(f"Weight scale must define weights 1-5. Found={sorted(weights)}.")

    def _validate_combination_rules(self, tag_combination_rules: dict[str, Any]) -> None:
        for rule in tag_combination_rules.get("rules", []):
            self._validate_tag_references(rule.get("tags", []), source=f"rule {rule.get('rule_id')}")

    def _validate_modeling_examples(self, modeling_examples: list[dict[str, Any]]) -> None:
        if not isinstance(modeling_examples, list):
            raise RulePackValidationError("modeling_examples.json must contain a list.")

        for example in modeling_examples:
            for tag in example.get("tags", []):
                tag_code = tag.get("tag_code")
                if tag_code not in EXPECTED_TAGS:
                    raise RulePackValidationError(
                        f"Unknown tag_code in example {example.get('game_code')}: {tag_code}"
                    )

                weight = tag.get("weight")
                if weight not in {1, 2, 3, 4, 5}:
                    raise RulePackValidationError(
                        f"Invalid weight in example {example.get('game_code')} for {tag_code}: {weight}"
                    )

            for tag in example.get("negative_examples", []):
                tag_code = tag.get("tag_code")
                if tag_code not in EXPECTED_TAGS:
                    raise RulePackValidationError(
                        f"Unknown negative tag_code in example {example.get('game_code')}: {tag_code}"
                    )

    def _validate_tag_references(self, tag_codes: list[str], source: str) -> None:
        for tag_code in tag_codes:
            if tag_code not in EXPECTED_TAGS:
                raise RulePackValidationError(f"Unknown tag reference in {source}: {tag_code}")

    def _default_rules_dir(self) -> Path:
        return Path(__file__).resolve().parents[4] / "modeling_context" / "rules"
