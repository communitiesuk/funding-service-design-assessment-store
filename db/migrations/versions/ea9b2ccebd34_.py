"""Migration of QA_COMPLETED status from assessment_flags to a newly created
qa_complete table.

Revision ID: ea9b2ccebd34
Revises: 4bdc171458b2
Create Date: 2023-07-14 10:17:05.239734

"""

from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ea9b2ccebd34"
down_revision = "4bdc171458b2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    qa_complete = op.create_table(
        "qa_complete",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["assessment_records.application_id"],
            name=op.f("fk_qa_complete_application_id_assessment_records"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_qa_complete")),
    )

    # Retrive qa completed info from flag_update & assessment_flag tables
    flag_updates = op.get_bind().execute(
        sa.text("SELECT id, assessment_flag_id, user_id, date_created FROM flag_update WHERE status='QA_COMPLETED';")
    )
    flags = op.get_bind().execute(
        sa.text("SELECT id, application_id FROM assessment_flag WHERE latest_status='QA_COMPLETED';")
    )
    qa_complete_dict = {}
    for id, assessment_flag_id, user_id, date_created in flag_updates:
        qa_complete_dict[str(assessment_flag_id)] = {
            "flag_update_id": str(id),
            "user_id": user_id,
            "date_created": date_created,
        }

    for id, application_id in flags:
        qa_complete_dict[str(id)] = qa_complete_dict[str(id)] | {"application_id": application_id}

    # Migrate qa info from existing assessment_flag & flag_update tables to newly created 'qa_complete' table
    if qa_complete_dict:
        qa_complete_records = []
        for key, value in qa_complete_dict.items():
            params = {
                "id": key,
                "application_id": str(value["application_id"]),
                "user_id": value["user_id"],
                "date_created": value["date_created"].isoformat(),
            }
            qa_complete_records.append(params)
        op.bulk_insert(qa_complete, qa_complete_records)

        # delete qa completed info from existing assessment_flag & flag_update tables
        delete_id_list_flag_update = ""
        delete_id_list_assessment_flag = ""
        for key, value in qa_complete_dict.items():
            delete_id_list_flag_update += f"'{value['flag_update_id']}',"
            delete_id_list_assessment_flag += f"'{key}',"

        op.get_bind().execute(sa.text(f"DELETE FROM flag_update WHERE id in ({delete_id_list_flag_update[:-1]});"))
        op.get_bind().execute(
            sa.text(f"DELETE FROM assessment_flag WHERE id in ({delete_id_list_assessment_flag[:-1]});")
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Retrive qa complete info from qa_complete table
    qa_complete_records = op.get_bind().execute(
        sa.text("SELECT id,application_id,user_id,date_created FROM qa_complete;")
    )
    qa_complete_dict = {}
    for id, application_id, user_id, date_created in qa_complete_records:
        qa_complete_dict[str(id)] = {
            "application_id": str(application_id),
            "user_id": user_id,
            "date_created": date_created,
        }

    # Migrate qa info from 'qa_complete' table to assessment_flag & flag_update tables
    for key, value in qa_complete_dict.items():
        op.get_bind().execute(
            f"INSERT INTO assessment_flag(id,application_id,latest_status) "
            f"VALUES ('{key}','{value['application_id']}', 'QA_COMPLETED');"
        )
        op.get_bind().execute(
            f"INSERT INTO flag_update(id,assessment_flag_id,user_id,date_created,status) "
            f"VALUES ('{str(uuid4())}','{key}','{value['user_id']}','{str(value['date_created'].isoformat())}', "
            f"'QA_COMPLETED');"
        )
    op.drop_table("qa_complete")

    # ### end Alembic commands ###
