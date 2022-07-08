from api.responses import compliance_response
from api.responses import error_response
from db.models.compliance import ComplianceError
from db.models.compliance import ComplianceMethods
from flask.views import MethodView


class ComplianceView(ComplianceMethods, MethodView):
    def get(self, sub_criteria_id: str, assessment_id: str):
        """
        GET /assessments/{assessment_id}/sub_criterias/
                {sub_criteria_id}/compliance endpoint
        return the compliance page for the sub_criteria of the assessment
        If no matching valid link is found returns a 404 error message
        :param assessment_id: id of the assessment
        :param sub_criteria_id: id of the sub_criteria
        :return: 200 assessment JSON / 404 Error
        """
        try:
            compliance_record = self.get_compliance(
                sub_criteria_id, assessment_id, as_json=True
            )
        except ComplianceError as e:
            return error_response(404, e.message)
        except IndexError:
            return error_response(404, "List retunred was dead fam")

        return compliance_response(compliance_record)

    def post(self, sub_criteria_id: str, assessment_id: str, body: dict):
        """
        Registers a score and justification for assessment and subcriteria
        :param sub_criteria_id: ID of sub-criteria
        :param assessment_id: ID of assessment
        :return: a json of the score and justification
                created (or an error if failure)
        """
        is_compliant = body.get("score")

        try:
            new_score_and_justification = self.register_compliance(
                sub_criteria_id, assessment_id, is_compliant
            )
        except ComplianceError as e:
            return error_response(401, e.message)

        return compliance_response(new_score_and_justification, 201)
