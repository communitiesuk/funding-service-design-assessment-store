from alembic_utils.pg_extension import PGExtension
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from db.models.comment import Comment
from db.models.score import Score
from sqlalchemy import event
from sqlalchemy import text

# A method of imposing a database level block to mutating application json.

block_json_func = PGFunction(
    schema="public",
    signature="block_blob_mutate()",
    definition="""RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
        IF NEW.jsonb_blob <> OLD.jsonb_blob THEN
        RAISE EXCEPTION 'Cannot mutate application json.';
        END IF;
        RETURN NEW;
    END;
    $$""",
)

block_json_updates_trig = PGTrigger(
    schema="public",
    signature="block_updates_on_app_blob",
    definition="""
    BEFORE UPDATE
    ON assessment_records
    FOR EACH ROW
    EXECUTE PROCEDURE block_blob_mutate();""",
    on_entity="assessment_records",
)

extension = PGExtension(
    schema="public",
    signature="pg_trgm",
)


@event.listens_for(Score, "after_insert", propagate=True)
@event.listens_for(Comment, "after_insert", propagate=True)
def update_workflow_status(_, connection, target):
    connection.execute(
        text(
            "UPDATE assessment_records SET workflow_status = 'IN_PROGRESS' "
            "WHERE application_id = :application_id "
            "AND workflow_status = 'NOT_STARTED'"
        ),
        {"application_id": target.application_id},
    )
