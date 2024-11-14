from db.models.assessment_record.assessment_records import AssessmentRecord
from db.queries.assessment_records.queries import insert_application_record
from flask import current_app


def import_from_apply_to_assess(application_data: dict):
    imported: AssessmentRecord = insert_application_record(
        application_json_string=application_data, application_type=None, is_json=True
    )
    current_app.logger.info(
        f"Imported application with reference {application_data['reference']} to assessment "
        f"with name {imported['project_name']}"
    )
