from fastapi.testclient import TestClient

from app.graph.nodes import retrieve_grs_context_node
from app.graph.state import create_initial_state
from app.graph.workflow import run_mock_workflow
from app.main import create_app


def test_mock_workflow_runs_to_finished_status() -> None:
    result = run_mock_workflow(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    assert result["status"] == "finished"
    assert result["source_bundle"] is not None
    assert result["retrieved_context"] is not None
    assert result["modeling_result"] is not None
    assert result["validation_result"] == {
        "is_valid": True,
        "errors": [],
        "warnings": [],
    }
    assert result["errors"] == []
    assert [entry["node"] for entry in result["trace"]] == [
        "start",
        "collect_sources_mock",
        "retrieve_grs_context_mock",
        "model_game_tags_mock",
        "validate_result_mock",
        "finish",
    ]


def test_mock_workflow_api_route() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/workflow/run-mock",
        json={
            "game_name": "Hades",
            "steam_url": "https://store.steampowered.com/app/1145360/Hades/",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "finished"
    assert body["game_name"] == "Hades"
    assert body["modeling_result"]["selected_existing_tags"][0]["tag_code"] == "combat"


def test_source_collection_workflow_route_exists() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/workflow/run-source-collection",
        json={
            "game_name": "",
            "steam_url": "https://store.steampowered.com/not-an-app/",
        },
    )

    assert response.status_code == 422


def test_retrieve_grs_context_node_loads_real_rule_pack() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    result = retrieve_grs_context_node(state)

    assert result["retrieved_context"]["weight_scale"]["scale"] == "1-5"
    assert len(result["retrieved_context"]["allowed_tags"]) == 20
    assert result["trace"][0]["node"] == "retrieve_grs_context"
