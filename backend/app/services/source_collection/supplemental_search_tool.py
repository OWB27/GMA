"""Read-only supplemental search tool for the source sufficiency agent."""

from typing import Any

import requests

from app.core.config import get_settings
from app.schemas.supplemental_search import SupplementalSearchResult, SupplementalSource


class SupplementalSearchTool:
    """Small Tavily-backed search tool used only inside source assessment."""

    max_results = 3
    timeout_seconds = 10

    def invoke(
        self,
        game_name: str,
        steam_url: str,
        query: str | None,
    ) -> SupplementalSearchResult:
        search_query = query or f"{game_name} gameplay features official description player experience"
        settings = get_settings()
        if not settings.tavily_api_key:
            return SupplementalSearchResult(
                query=search_query,
                sources=[],
                skipped_reason="TAVILY_API_KEY is not configured.",
            )

        try:
            response = requests.post(
                settings.tavily_search_url,
                json={
                    "api_key": settings.tavily_api_key,
                    "query": search_query,
                    "max_results": self.max_results,
                    "search_depth": "basic",
                    "include_answer": False,
                    "include_raw_content": False,
                    "include_domains": [
                        "store.steampowered.com",
                        "steamcommunity.com",
                        "pcgamer.com",
                        "ign.com",
                        "gamespot.com",
                        "rockpapershotgun.com",
                    ],
                },
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            return SupplementalSearchResult(
                query=search_query,
                sources=[],
                skipped_reason=f"Supplemental search failed: {error}",
            )

        payload = response.json()
        return SupplementalSearchResult(
            query=search_query,
            sources=self._parse_sources(payload.get("results", []), steam_url),
        )

    def _parse_sources(self, results: list[dict[str, Any]], steam_url: str) -> list[SupplementalSource]:
        sources: list[SupplementalSource] = []
        seen_urls = {steam_url.rstrip("/")}
        for result in results:
            url = str(result.get("url") or "").strip()
            normalized_url = url.rstrip("/")
            if not url or normalized_url in seen_urls:
                continue
            content = self._clean_text(str(result.get("content") or ""))
            if not content:
                continue
            seen_urls.add(normalized_url)
            sources.append(
                SupplementalSource(
                    title=str(result.get("title") or "").strip(),
                    url=url,
                    content=content,
                )
            )
        return sources[: self.max_results]

    def _clean_text(self, text: str) -> str:
        cleaned = " ".join(text.split())
        if len(cleaned) > 700:
            return cleaned[:700].rstrip() + "..."
        return cleaned
