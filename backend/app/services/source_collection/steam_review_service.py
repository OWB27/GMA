from typing import Any, Protocol

import requests


class HttpClient(Protocol):
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        pass


class SteamReviewService:
    review_url_template = "https://store.steampowered.com/appreviews/{app_id}"
    max_sample_reviews = 3
    max_review_length = 240
    modeling_keywords = {
        "atmosphere",
        "base",
        "build",
        "building",
        "challenge",
        "choice",
        "choices",
        "class",
        "combat",
        "co-op",
        "coop",
        "craft",
        "crafting",
        "difficulty",
        "exploration",
        "explore",
        "gear",
        "horror",
        "immersion",
        "immersive",
        "loot",
        "map",
        "multiplayer",
        "open world",
        "pacing",
        "progression",
        "puzzle",
        "pvp",
        "replay",
        "resource",
        "sandbox",
        "story",
        "strategy",
        "survival",
        "tactics",
        "world",
    }
    low_value_keywords = {
        "anti-cheat",
        "ban",
        "banned",
        "bug",
        "crash",
        "developer",
        "devs",
        "dlc",
        "microtransaction",
        "patch",
        "price",
        "refund",
        "review bomb",
        "server issue",
    }

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.http_client = http_client or requests

    def collect_review_summary(self, app_id: str) -> str | None:
        payload = self._fetch_reviews(app_id)
        query_summary = payload.get("query_summary", {})
        reviews = payload.get("reviews", [])

        score_text = self._format_score_summary(query_summary)
        sample_text = self._format_sample_review_themes(reviews)

        parts = [part for part in [score_text, sample_text] if part]
        if not parts:
            return None
        return " ".join(parts)

    def _fetch_reviews(self, app_id: str) -> dict[str, Any]:
        response = self.http_client.get(
            self.review_url_template.format(app_id=app_id),
            params={
                "json": 1,
                "language": "english",
                "filter": "summary",
                "review_type": "all",
                "purchase_type": "all",
                "num_per_page": 50,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        return payload if isinstance(payload, dict) else {}

    def _format_score_summary(self, query_summary: dict[str, Any]) -> str | None:
        review_score_desc = query_summary.get("review_score_desc")
        total_positive = query_summary.get("total_positive")
        total_negative = query_summary.get("total_negative")
        total_reviews = query_summary.get("total_reviews")

        if not review_score_desc:
            return None

        if isinstance(total_positive, int) and isinstance(total_reviews, int) and total_reviews > 0:
            positive_ratio = round(total_positive / total_reviews * 100)
            return (
                f"Steam English review summary: {review_score_desc}, "
                f"with about {positive_ratio}% positive reviews "
                f"({total_positive} positive, {total_negative} negative, {total_reviews} total)."
            )

        return f"Steam English review summary: {review_score_desc}."

    def _format_sample_review_themes(self, reviews: list[dict[str, Any]]) -> str | None:
        candidates = self._select_sample_reviews(reviews)
        snippets = [candidate["text"] for candidate in candidates]

        if not snippets:
            return None

        return "Representative English review snippets: " + " | ".join(snippets)

    def _select_sample_reviews(self, reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
        candidates = []
        for review in reviews:
            text = review.get("review")
            if not isinstance(text, str):
                continue

            cleaned = self._clean_review_text(text)
            if not cleaned or self._is_low_value_review(cleaned):
                continue

            candidates.append(
                {
                    "text": cleaned,
                    "score": self._score_review_for_modeling(cleaned),
                    "length": len(cleaned),
                }
            )

        candidates.sort(key=lambda candidate: (candidate["score"], candidate["length"]), reverse=True)
        return candidates[: self.max_sample_reviews]

    def _clean_review_text(self, text: str) -> str | None:
        cleaned = " ".join(text.split())
        if not cleaned:
            return None
        if len(cleaned) > self.max_review_length:
            return cleaned[: self.max_review_length].rstrip() + "..."
        return cleaned

    def _is_low_value_review(self, text: str) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in self.low_value_keywords)

    def _score_review_for_modeling(self, text: str) -> int:
        lowered = text.lower()
        return sum(1 for keyword in self.modeling_keywords if keyword in lowered)
