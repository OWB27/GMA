from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


def test_review_route_validates_request_body_before_database_lookup() -> None:
    client = TestClient(create_app())

    response = client.post(
        f"/modeling-jobs/{uuid4()}/review",
        json={
            "reviewed_tags": [
                {
                    "tag_code": "combat",
                    "weight": 9,
                }
            ],
            "review_status": "approved",
        },
    )

    assert response.status_code == 422


def test_create_and_run_modeling_job_route_validates_request_body() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/modeling-jobs/run",
        json={
            "game_name": "",
            "steam_url": "https://store.steampowered.com/app/1145360/Hades/",
        },
    )

    assert response.status_code == 422


def test_review_route_rejects_needs_review_status() -> None:
    client = TestClient(create_app())

    response = client.post(
        f"/modeling-jobs/{uuid4()}/review",
        json={
            "reviewed_tags": [
                {
                    "tag_code": "combat",
                    "weight": 4,
                }
            ],
            "review_status": "needs_review",
        },
    )

    assert response.status_code == 422
