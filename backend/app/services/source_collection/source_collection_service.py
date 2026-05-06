from app.schemas.source_bundle import SourceBundleData
from app.services.source_collection.steam_review_service import SteamReviewService
from app.services.source_collection.steam_store_service import SteamStoreService


class SourceCollectionService:
    def __init__(
        self,
        steam_store_service: SteamStoreService | None = None,
        steam_review_service: SteamReviewService | None = None,
    ) -> None:
        self.steam_store_service = steam_store_service or SteamStoreService()
        self.steam_review_service = steam_review_service or SteamReviewService()

    def collect_sources(self, game_name: str, steam_url: str) -> SourceBundleData:
        source_bundle = self.steam_store_service.collect_official_sources(
            game_name=game_name,
            steam_url=steam_url,
        )
        app_id = self.steam_store_service.extract_app_id(steam_url)
        if not app_id:
            return source_bundle

        review_summary = self.steam_review_service.collect_review_summary(app_id)
        if review_summary:
            source_bundle.review_summary = review_summary
            source_bundle.page_text = self._join_text([source_bundle.page_text, review_summary])
        return source_bundle

    def _join_text(self, values: list[str | None]) -> str | None:
        parts = [value for value in values if value]
        if not parts:
            return None
        return "\n\n".join(parts)
