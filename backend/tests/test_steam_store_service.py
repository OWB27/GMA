from app.services.source_collection.steam_store_service import SteamStoreService


class FakeResponse:
    def __init__(self, json_payload=None, text="") -> None:
        self.json_payload = json_payload
        self.text = text

    def raise_for_status(self) -> None:
        return None

    def json(self):
        return self.json_payload


class FakeHttpClient:
    def __init__(self) -> None:
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if "api/appdetails" in url:
            return FakeResponse(
                json_payload={
                    "1174180": {
                        "success": True,
                        "data": {
                            "short_description": "Winner of over 175 Game of the Year Awards.",
                            "detailed_description": "<p>America, 1899.</p><br>The gang is on the run.",
                            "genres": [
                                {"description": "Action"},
                                {"description": "Adventure"},
                            ],
                            "categories": [
                                {"description": "Single-player"},
                                {"description": "Online PvP"},
                                {"description": "Steam Achievements"},
                            ],
                        },
                    }
                }
            )
        return FakeResponse(
            text="""
            <a class="app_tag" href="#">Open World</a>
            <a class="app_tag" href="#">Story Rich</a>
            <a class="app_tag" href="#">Western</a>
            """
        )


def test_collect_official_sources_from_steam_appdetails_and_page_tags() -> None:
    service = SteamStoreService(http_client=FakeHttpClient())

    source_bundle = service.collect_official_sources(
        game_name="Red Dead Redemption 2",
        steam_url="https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/?l=schinese",
    )

    assert source_bundle.short_description == "Winner of over 175 Game of the Year Awards."
    assert source_bundle.detailed_description == "America, 1899.\nThe gang is on the run."
    assert source_bundle.official_genres == ["Action", "Adventure"]
    assert source_bundle.official_categories == ["Single-player", "Online PvP"]
    assert source_bundle.popular_user_tags == ["Open World", "Story Rich", "Western"]
    assert source_bundle.page_text is not None
    assert "Popular user-defined tags: Open World, Story Rich, Western" in source_bundle.page_text
    assert "Steam Achievements" not in source_bundle.page_text


def test_clean_description_prefers_about_the_game_section() -> None:
    service = SteamStoreService()

    cleaned = service.clean_html(
        "<h2>Ultimate Edition</h2>Bonus online items.<h2>About the Game</h2>Core game description."
    )

    assert service._prefer_about_game_section(cleaned) == "Core game description."


def test_extract_app_id_from_steam_url() -> None:
    service = SteamStoreService()

    app_id = service.extract_app_id(
        "https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/?l=schinese"
    )

    assert app_id == "1174180"
