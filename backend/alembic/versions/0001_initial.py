from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "booking_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reference_number", sa.String(32), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("phone", sa.String(32), nullable=False),
        sa.Column("email", sa.String(254)),
        sa.Column("test", sa.String(160), nullable=False),
        sa.Column("collection_type", sa.String(40), nullable=False),
        sa.Column("preferred_date", sa.Date()),
        sa.Column("preferred_time", sa.String(20)),
        sa.Column("address", sa.String(300)),
        sa.Column("city", sa.String(100)),
        sa.Column("notes", sa.Text()),
        sa.Column("status", sa.String(20), server_default="new", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("reference_number"),
    )
    op.create_index("ix_booking_requests_reference_number", "booking_requests", ["reference_number"])
    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reference_number", sa.String(32), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("phone", sa.String(32), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("subject", sa.String(160), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), server_default="new", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("reference_number"),
    )
    op.create_index("ix_contact_messages_reference_number", "contact_messages", ["reference_number"])


def downgrade():
    op.drop_index("ix_contact_messages_reference_number", table_name="contact_messages")
    op.drop_table("contact_messages")
    op.drop_index("ix_booking_requests_reference_number", table_name="booking_requests")
    op.drop_table("booking_requests")
