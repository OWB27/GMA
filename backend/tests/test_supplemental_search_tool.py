from types import SimpleNamespace

from app.services.source_collection import supplemental_search_tool as tool_module
from app.services.source_collection.supplemental_search_tool import SupplementalSearchTool


def test_supplemental_search_tool_skips_without_api_key(monkeypatch) -> None:
    monkeypatch.setattr(
        tool_module,
        "get_settings",
        lambda: SimpleNamespace(tavily_api_key=None, tavily_search_url="https://example.com/search"),
    )

    result = SupplementalSearchTool().invoke(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
        query=None,
    )

    assert result.sources == []
    assert result.skipped_reason == "TAVILY_API_KEY is not configured."
    assert result.query == "Hades gameplay features official description player experience"


def test_supplemental_search_tool_parses_and_deduplicates_results() -> None:
    tool = SupplementalSearchTool()

    sources = tool._parse_sources(
        results=[
            {
                "title": "Steam page duplicate",
                "url": "https://store.steampowered.com/app/1145360/Hades/",
                "content": "Duplicate Steam content.",
            },
            {
                "title": "Gameplay overview",
                "url": "https://example.com/hades",
                "content": "Fast roguelike combat with repeated runs and build variety.",
            },
        ],
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    assert len(sources) == 1
    assert sources[0].url == "https://example.com/hades"
