"""LangChain modeling chain for turning evidence and GRS rules into a draft."""

import json
from typing import Any, Protocol

from langchain_core.prompts import ChatPromptTemplate

from app.core.config import get_settings
from app.core.llm import get_chat_model
from app.schemas.modeling_output import ModelingResult


class ModelingChainRunnable(Protocol):
    def invoke(self, input: dict[str, Any]) -> ModelingResult:
        pass


class ModelingChain:
    """Calls the configured chat model and returns a structured modeling result."""

    def __init__(self, runnable: ModelingChainRunnable | None = None) -> None:
        self.runnable = runnable

    def invoke(
        self,
        game_name: str,
        steam_url: str,
        source_bundle: dict[str, Any],
        retrieved_context: dict[str, Any],
    ) -> ModelingResult:
        runnable = self.runnable or self._build_runnable()
        result = runnable.invoke(
            {
                "game_name": game_name,
                "steam_url": steam_url,
                "source_bundle": self._to_json(source_bundle),
                "retrieved_context": self._to_json(retrieved_context),
            }
        )

        if isinstance(result, ModelingResult):
            return result
        return ModelingResult.model_validate(result)

    def _build_runnable(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are GMA, a game modeling agent. "
                    "Your task is to select only existing tags and suggest weights for one Steam game. "
                    "Do not create new tags. Steam user tags are evidence, not final GRS tags. "
                    "Use suggested_weight for tag strength from 1 to 5. "
                    "Use confidence for certainty from 0 to 1. "
                    "Do not be overly confident; if evidence is limited, lower the confidence score. "
                    "Every selected tag must include evidence snippets from the source bundle. "
                    "For each evidence snippet, provide both English and Simplified Chinese text. "
                    "For each reason, provide both English and Simplified Chinese text. "
                    "Keep English evidence faithful to the source. The Chinese evidence can be a concise translation. "
                    "If evidence is insufficient for a tag, do not select it. "
                    "Return valid JSON that matches the requested schema. "
                    "JSON string values must not contain unescaped double quotes. "
                    "When quoting phrases inside Chinese text, use Chinese-style quotation marks instead of English double quotes. "
                    "When quoting phrases inside English text, prefer single quotes like '...' instead of double quotes. "
                    "Do not wrap the JSON in Markdown code fences.",
                ),
                (
                    "human",
                    "Game name: {game_name}\n"
                    "Steam URL: {steam_url}\n\n"
                    "Source bundle JSON:\n{source_bundle}\n\n"
                    "Retrieved GRS context JSON:\n{retrieved_context}\n\n"
                    "Output JSON schema:\n{output_schema}\n\n"
                    "Return a structured modeling draft using only allowed_tags from the retrieved context.",
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
            ModelingResult,
            method=settings.llm_structured_output_method,
        )
        return prompt.partial(output_schema=self._output_schema_json()) | model

    def _to_json(self, value: dict[str, Any]) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2)

    def _output_schema_json(self) -> str:
        return json.dumps(ModelingResult.model_json_schema(), ensure_ascii=False, indent=2)
