"""LangChain node for deciding whether collected source evidence is enough."""

import json
from typing import Any, Protocol

from langchain_core.prompts import ChatPromptTemplate

from app.core.config import get_settings
from app.core.llm import get_chat_model
from app.schemas.source_assessment import SourceAssessment


class SourceAssessmentRunnable(Protocol):
    def invoke(self, input: dict[str, Any]) -> SourceAssessment:
        pass


class SourceAssessmentChain:
    """Asks the configured chat model to judge source sufficiency before modeling."""

    def __init__(self, runnable: SourceAssessmentRunnable | None = None) -> None:
        self.runnable = runnable

    def invoke(
        self,
        game_name: str,
        steam_url: str,
        source_bundle: dict[str, Any],
    ) -> SourceAssessment:
        runnable = self.runnable or self._build_runnable()
        result = runnable.invoke(
            {
                "game_name": game_name,
                "steam_url": steam_url,
                "source_bundle": self._to_json(source_bundle),
            }
        )

        if isinstance(result, SourceAssessment):
            return result
        return SourceAssessment.model_validate(result)

    def _build_runnable(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are GMA's evidence sufficiency agent. "
                    "Your job is not to model tags yet. "
                    "Only decide whether the current Steam source bundle is sufficient for GRS tag modeling. "
                    "A source bundle is usually sufficient when it includes official description plus at least some "
                    "combination of official genres, Steam user tags, categories, or review summary. "
                    "Mark it insufficient only when the core gameplay loop, player experience, or genre context is unclear. "
                    "Do not ask for more sources just because more information could be nice. "
                    "Do not create tags. Do not assign weights. "
                    "Return valid JSON that matches the requested schema. "
                    "recommended_action must be continue_modeling when is_sufficient is true. "
                    "recommended_action must be fetch_supplemental_sources when is_sufficient is false. "
                    "Do not wrap the JSON in Markdown code fences.",
                ),
                (
                    "human",
                    "Game name: {game_name}\n"
                    "Steam URL: {steam_url}\n\n"
                    "Source bundle JSON:\n{source_bundle}\n\n"
                    "Output JSON schema:\n{output_schema}\n\n"
                    "Decide if this evidence is sufficient before GRS tag modeling.",
                ),
            ]
        )
        settings = get_settings()
        if settings.llm_structured_output_method not in {
            "function_calling",
            "json_mode",
            "json_schema",
        }:
            raise ValueError(
                "LLM_STRUCTURED_OUTPUT_METHOD must be one of: "
                "function_calling, json_mode, json_schema."
            )

        model = get_chat_model().with_structured_output(
            SourceAssessment,
            method=settings.llm_structured_output_method,
        )
        return prompt.partial(output_schema=self._output_schema_json()) | model

    def _to_json(self, value: dict[str, Any]) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2)

    def _output_schema_json(self) -> str:
        return json.dumps(SourceAssessment.model_json_schema(), ensure_ascii=False, indent=2)
