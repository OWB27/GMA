"""create modeling tables

Revision ID: 202605060001
Revises:
Create Date: 2026-05-06 00:01:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "202605060001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "modeling_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_name", sa.String(length=255), nullable=False),
        sa.Column("steam_url", sa.String(length=2048), nullable=False),
        sa.Column("status", sa.Enum(
            "created",
            "collecting_sources",
            "modeling",
            "validating",
            "needs_review",
            "approved",
            "rejected",
            "exported",
            "failed",
            name="modeling_job_status",
        ), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_modeling_jobs_game_name", "modeling_jobs", ["game_name"])
    op.create_index("ix_modeling_jobs_status", "modeling_jobs", ["status"])

    op.create_table(
        "source_bundles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.Uuid(), nullable=False),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["modeling_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_source_bundles_job_id", "source_bundles", ["job_id"], unique=True)

    op.create_table(
        "modeling_drafts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.Uuid(), nullable=False),
        sa.Column("raw_model_output", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("validation_result", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["modeling_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_modeling_drafts_job_id", "modeling_drafts", ["job_id"], unique=True)

    op.create_table(
        "reviewed_modeling_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.Uuid(), nullable=False),
        sa.Column("reviewed_tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("review_status", sa.Enum(
            "draft",
            "needs_review",
            "approved",
            "rejected",
            "exported",
            name="review_status",
        ), nullable=False),
        sa.Column("reviewer_notes", sa.String(length=5000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["modeling_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reviewed_modeling_results_job_id", "reviewed_modeling_results", ["job_id"], unique=True)
    op.create_index("ix_reviewed_modeling_results_review_status", "reviewed_modeling_results", ["review_status"])

    op.create_table(
        "workflow_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("message", sa.String(length=2000), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["modeling_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_events_event_type", "workflow_events", ["event_type"])
    op.create_index("ix_workflow_events_job_id", "workflow_events", ["job_id"])


def downgrade() -> None:
    op.drop_index("ix_workflow_events_job_id", table_name="workflow_events")
    op.drop_index("ix_workflow_events_event_type", table_name="workflow_events")
    op.drop_table("workflow_events")

    op.drop_index("ix_reviewed_modeling_results_review_status", table_name="reviewed_modeling_results")
    op.drop_index("ix_reviewed_modeling_results_job_id", table_name="reviewed_modeling_results")
    op.drop_table("reviewed_modeling_results")

    op.drop_index("ix_modeling_drafts_job_id", table_name="modeling_drafts")
    op.drop_table("modeling_drafts")

    op.drop_index("ix_source_bundles_job_id", table_name="source_bundles")
    op.drop_table("source_bundles")

    op.drop_index("ix_modeling_jobs_status", table_name="modeling_jobs")
    op.drop_index("ix_modeling_jobs_game_name", table_name="modeling_jobs")
    op.drop_table("modeling_jobs")

    op.execute("DROP TYPE IF EXISTS review_status")
    op.execute("DROP TYPE IF EXISTS modeling_job_status")
