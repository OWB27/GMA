import json
from pathlib import Path

import pytest

from app.services.grs_context.rule_pack_loader import (
    EXPECTED_TAGS,
    RulePackLoader,
    RulePackValidationError,
)


def test_rule_pack_loader_loads_project_rules() -> None:
    rule_pack = RulePackLoader().load()

    assert {definition["code"] for definition in rule_pack["tag_definitions"]} == EXPECTED_TAGS
    assert len(rule_pack["tag_definitions"]) == 20
    assert {rule["weight"] for rule in rule_pack["weight_scale"]["rules"]} == {1, 2, 3, 4, 5}


def test_rule_pack_loader_rejects_unknown_example_tag(tmp_path: Path) -> None:
    source_rule_pack = RulePackLoader().load()
    source_rule_pack["modeling_examples"][0]["tags"][0]["tag_code"] = "unknown_tag"

    _write_rule_pack(tmp_path, source_rule_pack)
    loader = RulePackLoader(rules_dir=tmp_path)

    with pytest.raises(RulePackValidationError, match="Unknown tag_code"):
        loader.load()


def _write_rule_pack(rules_dir: Path, rule_pack: dict) -> None:
    (rules_dir / "tag_definitions.json").write_text(
        json.dumps(rule_pack["tag_definitions"]),
        encoding="utf-8",
    )
    (rules_dir / "weight_scale.json").write_text(
        json.dumps(rule_pack["weight_scale"]),
        encoding="utf-8",
    )
    (rules_dir / "tag_combination_rules.json").write_text(
        json.dumps(rule_pack["tag_combination_rules"]),
        encoding="utf-8",
    )
    (rules_dir / "modeling_examples.json").write_text(
        json.dumps(rule_pack["modeling_examples"]),
        encoding="utf-8",
    )
