from app import app
from db.models.assessment_record.assessment_records import AssessmentRecord


def question_answer_dict(assessment_record: AssessmentRecord):
    jsonb_blob = assessment_record.jsonb_blob
    return jsonb_blob


with app.app_context():
    x = AssessmentRecord.query.all()
    mapped = map(question_answer_dict, x)
    breakpoint()
