"""Business validation for LLM-generated modeling drafts."""

from typing import Any

from pydantic import ValidationError

from app.schemas.modeling_output import ModelingResult
from app.schemas.validation_result import ValidationResult


class ModelingResultValidator:
    """Checks whether a structured model output is legal and reviewable for GMA."""

    def validate(
        self,
        modeling_result: dict[str, Any] | None,
        retrieved_context: dict[str, Any] | None,
    ) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if modeling_result is None:
            return ValidationResult(
                is_valid=False,
                errors=["modeling_result is required before validation."],
                warnings=[],
            )

        if retrieved_context is None:
            return ValidationResult(
                is_valid=False,
                errors=["retrieved_context is required before validation."],
                warnings=[],
            )

        try:
            parsed_result = ModelingResult.model_validate(modeling_result)
        except ValidationError as error:
            return ValidationResult(
                is_valid=False,
                errors=[f"modeling_result schema validation failed: {error}"],
                warnings=[],
            )

        allowed_tags = set(retrieved_context.get("allowed_tags", []))
        selected_tags = parsed_result.selected_existing_tags
        selected_tag_codes = [tag.tag_code for tag in selected_tags]

        errors.extend(self._validate_existing_tags(selected_tag_codes, allowed_tags))
        errors.extend(self._validate_duplicate_tags(selected_tag_codes))

        warnings.extend(self._validate_tag_count(len(selected_tags)))
        warnings.extend(self._validate_core_tag_count(selected_tags))
        warnings.extend(self._validate_low_confidence_tags(selected_tags))
        warnings.extend(
            self._validate_soft_conflicts(
                selected_tags=selected_tags,
                tag_combination_rules=retrieved_context.get("tag_combination_rules", {}),
            )
        )

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _validate_existing_tags(self, tag_codes: list[str], allowed_tags: set[str]) -> list[str]:
        if not allowed_tags:
            return ["retrieved_context.allowed_tags is required for validation."]

        return [
            f"Unknown tag_code: {tag_code}."
            for tag_code in tag_codes
            if tag_code not in allowed_tags
        ]

    def _validate_duplicate_tags(self, tag_codes: list[str]) -> list[str]:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for tag_code in tag_codes:
            if tag_code in seen:
                duplicates.add(tag_code)
            seen.add(tag_code)

        return [f"Duplicate tag_code: {tag_code}." for tag_code in sorted(duplicates)]

    def _validate_tag_count(self, tag_count: int) -> list[str]:
        if tag_count < 3:
            return ["Selected tag count is low; expected at least 3 tags for reviewable modeling."]
        if tag_count > 7:
            return ["Selected tag count is high; expected at most 7 tags for reviewable modeling."]
        return []

    def _validate_core_tag_count(self, selected_tags) -> list[str]:
        core_tag_count = sum(1 for tag in selected_tags if tag.suggested_weight == 5)
        if core_tag_count > 3:
            return ["Too many weight-5 core tags; expected no more than 3."]
        return []

    def _validate_low_confidence_tags(self, selected_tags) -> list[str]:
        return [
            f"Low confidence for tag_code {tag.tag_code}: {tag.confidence}."
            for tag in selected_tags
            if tag.confidence < 0.5
        ]

    def _validate_soft_conflicts(
        self,
        selected_tags,
        tag_combination_rules: dict[str, Any],
    ) -> list[str]:
        weights_by_tag = {tag.tag_code: tag.suggested_weight for tag in selected_tags}
        warnings: list[str] = []

        for rule in tag_combination_rules.get("rules", []):
            if rule.get("type") != "soft_conflict":
                continue

            rule_tags = rule.get("tags", [])
            if len(rule_tags) < 2:
                continue

            if all(weights_by_tag.get(tag_code, 0) >= 4 for tag_code in rule_tags):
                warnings.append(
                    f"Soft conflict {rule.get('rule_id')} should be reviewed: "
                    f"{', '.join(rule_tags)} all have high weights."
                )

        return warnings
