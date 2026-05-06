import html
import re
from typing import Any, Protocol
from urllib.parse import urlparse

import requests

from app.schemas.source_bundle import SourceBundleData


class HttpClient(Protocol):
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        pass


class SteamStoreService:
    appdetails_url = "https://store.steampowered.com/api/appdetails"
    modeling_relevant_categories = {
        "Single-player",
        "Multi-player",
        "PvP",
        "Online PvP",
        "LAN PvP",
        "Shared/Split Screen PvP",
        "Co-op",
        "Online Co-op",
        "LAN Co-op",
        "Shared/Split Screen Co-op",
        "MMO",
        "Cross-Platform Multiplayer",
    }

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.http_client = http_client or requests

    def collect_official_sources(self, game_name: str, steam_url: str) -> SourceBundleData:
        app_id = self.extract_app_id(steam_url)
        if not app_id:
            return SourceBundleData(
                source_urls=[steam_url],
                extraction_notes=f"Could not extract Steam app id for {game_name}.",
            )

        appdetails = self._fetch_appdetails(app_id)
        store_html = self._fetch_store_page_html(app_id)
        popular_tags = self.extract_popular_user_tags(store_html)

        short_description = appdetails.get("short_description")
        detailed_description = self.clean_html(appdetails.get("detailed_description"))
        detailed_description = self._prefer_about_game_section(detailed_description)
        genres = self._extract_descriptions(appdetails.get("genres", []))
        categories = self._filter_modeling_categories(
            self._extract_descriptions(appdetails.get("categories", []))
        )
        page_text = self._join_text(
            [
                short_description,
                detailed_description,
                self._format_list("Official genres", genres),
                self._format_list("Official categories", categories),
                self._format_list("Popular user-defined tags", popular_tags),
            ]
        )

        return SourceBundleData(
            short_description=short_description,
            detailed_description=detailed_description,
            review_summary=None,
            official_genres=genres,
            official_categories=categories,
            popular_user_tags=popular_tags,
            page_text=page_text,
            source_urls=[steam_url, self._canonical_store_url(app_id)],
            extraction_notes=f"Collected official Steam appdetails and store page tags for {game_name}.",
        )

    def extract_app_id(self, steam_url: str) -> str | None:
        path_parts = [part for part in urlparse(steam_url).path.split("/") if part]
        for index, part in enumerate(path_parts):
            if part == "app" and index + 1 < len(path_parts):
                app_id = path_parts[index + 1]
                return app_id if app_id.isdigit() else None
        return None

    def extract_popular_user_tags(self, store_html: str | None) -> list[str]:
        if not store_html:
            return []

        tags = []
        for match in re.finditer(r'class="app_tag[^"]*"[^>]*>\s*([^<]+)\s*</a>', store_html):
            tag = html.unescape(" ".join(match.group(1).split()))
            if tag and tag not in tags:
                tags.append(tag)
        return tags

    def clean_html(self, value: str | None) -> str | None:
        if not value:
            return None
        text = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
        text = re.sub(r"</p\s*>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
        lines = [" ".join(line.split()) for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)
        return cleaned or None

    def _fetch_appdetails(self, app_id: str) -> dict[str, Any]:
        response = self.http_client.get(
            self.appdetails_url,
            params={
                "appids": app_id,
                "filters": "basic,genres,categories",
                "l": "english",
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        app_payload = payload.get(app_id, {})
        if not app_payload.get("success"):
            return {}
        return app_payload.get("data", {})

    def _fetch_store_page_html(self, app_id: str) -> str | None:
        response = self.http_client.get(
            f"{self._canonical_store_url(app_id)}?l=english",
            headers={"Accept-Language": "en-US,en;q=0.9"},
            timeout=20,
        )
        response.raise_for_status()
        return response.text

    def _extract_descriptions(self, items: list[dict[str, Any]]) -> list[str]:
        descriptions = []
        for item in items:
            description = item.get("description")
            if isinstance(description, str) and description not in descriptions:
                descriptions.append(description)
        return descriptions

    def _filter_modeling_categories(self, categories: list[str]) -> list[str]:
        return [
            category
            for category in categories
            if category in self.modeling_relevant_categories
        ]

    def _prefer_about_game_section(self, detailed_description: str | None) -> str | None:
        if not detailed_description:
            return None

        marker = "About the Game"
        if marker not in detailed_description:
            return detailed_description

        _, about_text = detailed_description.split(marker, 1)
        cleaned = about_text.strip()
        return cleaned or detailed_description

    def _format_list(self, label: str, values: list[str]) -> str | None:
        if not values:
            return None
        return f"{label}: {', '.join(values)}"

    def _join_text(self, values: list[str | None]) -> str | None:
        parts = [value for value in values if value]
        if not parts:
            return None
        return "\n\n".join(parts)

    def _canonical_store_url(self, app_id: str) -> str:
        return f"https://store.steampowered.com/app/{app_id}/"
