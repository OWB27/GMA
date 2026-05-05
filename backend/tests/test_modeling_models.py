from app.models.modeling import ModelingJob, ModelingJobStatus
from app.schemas.modeling import ModelingJobCreate


def test_modeling_job_defaults_to_created_status() -> None:
    job = ModelingJob(game_name="Hades", steam_url="https://store.steampowered.com/app/1145360/Hades/")

    assert job.status == ModelingJobStatus.CREATED
    assert job.game_name == "Hades"


def test_modeling_job_create_schema_requires_two_inputs() -> None:
    data = ModelingJobCreate(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    assert data.game_name == "Hades"
    assert data.steam_url.startswith("https://store.steampowered.com/")
