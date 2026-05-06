from app.services.source_collection.steam_review_service import SteamReviewService


class FakeResponse:
    def __init__(self, json_payload) -> None:
        self.json_payload = json_payload

    def raise_for_status(self) -> None:
        return None

    def json(self):
        return self.json_payload


class FakeHttpClient:
    def __init__(self) -> None:
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return FakeResponse(
            {
                "query_summary": {
                    "review_score_desc": "Very Positive",
                    "total_positive": 91,
                    "total_negative": 9,
                    "total_reviews": 100,
                },
                "reviews": [
                    {"review": "Great survival pressure and base building with tense PvP."},
                    {"review": "The developer keeps patching balance and banning people."},
                    {"review": "Harsh learning curve, but cooperation and raids create memorable stories."},
                    {"review": "The open world is brutal and player-driven."},
                    {"review": "Fourth review should not be included."},
                ],
            }
        )


def test_collect_review_summary_from_steam_reviews_api() -> None:
    http_client = FakeHttpClient()
    service = SteamReviewService(http_client=http_client)

    summary = service.collect_review_summary("252490")

    assert summary is not None
    assert "Very Positive" in summary
    assert "about 91% positive reviews" in summary
    assert "survival pressure" in summary
    assert "developer keeps patching" not in summary
    assert "Fourth review" not in summary
    assert http_client.calls[0][1]["params"]["language"] == "english"
    assert http_client.calls[0][1]["params"]["num_per_page"] == 50


def test_review_selection_falls_back_to_long_non_noise_reviews() -> None:
    service = SteamReviewService()

    selected = service._select_sample_reviews(
        [
            {"review": "Bad devs and constant bans."},
            {"review": "A strange but memorable experience with friends over many sessions."},
            {"review": "Short."},
        ]
    )

    assert [review["text"] for review in selected] == [
        "A strange but memorable experience with friends over many sessions.",
        "Short.",
    ]


def test_review_summary_returns_score_only_when_no_useful_samples() -> None:
    class NoiseOnlyHttpClient:
        def get(self, url, **kwargs):
            return FakeResponse(
                {
                    "query_summary": {
                        "review_score_desc": "Mixed",
                        "total_positive": 50,
                        "total_negative": 50,
                        "total_reviews": 100,
                    },
                    "reviews": [
                        {"review": "Developers patch bans refund crash."},
                    ],
                }
            )

    service = SteamReviewService(http_client=NoiseOnlyHttpClient())

    summary = service.collect_review_summary("123")

    assert summary == (
        "Steam English review summary: Mixed, with about 50% positive reviews "
        "(50 positive, 50 negative, 100 total)."
    )
