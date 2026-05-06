from app.schemas.source_bundle import SourceBundleData
from app.services.source_collection.source_collection_service import SourceCollectionService


class FakeSteamStoreService:
    def extract_app_id(self, steam_url: str) -> str | None:
        return "1174180"

    def collect_official_sources(self, game_name: str, steam_url: str) -> SourceBundleData:
        return SourceBundleData(
            short_description="Official short description.",
            detailed_description="Official detailed description.",
            official_genres=["Action", "Adventure"],
            official_categories=["Single-player"],
            popular_user_tags=["Open World", "Story Rich"],
            page_text="Official page text.",
            source_urls=[steam_url],
            extraction_notes="Official Steam data.",
        )


class FakeSteamReviewService:
    def collect_review_summary(self, app_id: str) -> str | None:
        return "Steam English review summary: Very Positive, with about 91% positive reviews."


def test_source_collection_returns_steam_official_sources_with_review_summary() -> None:
    service = SourceCollectionService(
        steam_store_service=FakeSteamStoreService(),
        steam_review_service=FakeSteamReviewService(),
    )

    source_bundle = service.collect_sources(
        game_name="Red Dead Redemption 2",
        steam_url="https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/",
    )

    assert source_bundle.short_description == "Official short description."
    assert source_bundle.detailed_description == "Official detailed description."
    assert source_bundle.review_summary == "Steam English review summary: Very Positive, with about 91% positive reviews."
    assert source_bundle.official_genres == ["Action", "Adventure"]
    assert source_bundle.official_categories == ["Single-player"]
    assert source_bundle.popular_user_tags == ["Open World", "Story Rich"]
    assert source_bundle.page_text == (
        "Official page text.\n\n"
        "Steam English review summary: Very Positive, with about 91% positive reviews."
    )
    assert source_bundle.extraction_notes == "Official Steam data."
