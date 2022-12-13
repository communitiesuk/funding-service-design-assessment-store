from api.models.sub_criteria import SubCriteria
from config import Config
from db.queries.assessment_records.queries import get_application_jsonb_blob
from flask import abort
from flask import current_app


def get_all_subcriteria():
    sub_criterias = []
    for section in (
        Config.COF_R2W2_ASSESSMENT_MAPPING["scored_criteria"]
        + Config.COF_R2W2_ASSESSMENT_MAPPING["unscored_sections"]
    ):
        for sub_criteria in section["sub_criteria"]:
            sub_criterias.append(sub_criteria)
    return sub_criterias


def get_matching_sub_criteria(sub_criteria_id):
    current_app.logger.info(
        f"Finding sub criteria data in config for: {sub_criteria_id}"
    )
    sub_criterias = get_all_subcriteria()
    matching_sub_criteria = list(
        filter(
            lambda sub_criteria: sub_criteria["id"] == sub_criteria_id,
            sub_criterias,
        )
    )
    if len(matching_sub_criteria) == 1:
        return matching_sub_criteria[0]
    elif len(matching_sub_criteria) > 1:
        msg = "sub_criteria: '{sub_criteria_id}' duplicated."
        current_app.logger.error(msg)
        raise ValueError(msg)
    else:
        msg = f"sub_criteria: '{sub_criteria_id}' not found."
        current_app.logger.warn(msg)
        abort(404, description=msg)


def return_subcriteria_from_config(sub_criteria_id):
    sub_criteria = get_matching_sub_criteria(sub_criteria_id)
    # TODO get actual score submitted status when score table available
    score_submitted = False

    return SubCriteria.from_filtered_dict(
        {"score_submitted": score_submitted, **sub_criteria}
    )


class SubCriteriaThemes:
    @classmethod
    def get_themes_answers(cls, theme_id: str) -> list[dict]:
        """function takes a theme_id arg & returns a list
        of answers with given theme_id.
        """
        sub_criterias = get_all_subcriteria()
        try:
            return [
                theme.get("answers")
                for themes in sub_criterias
                for theme in themes.get("themes")
                if theme_id == theme.get("id")
            ][0]
        except IndexError:
            current_app.logger.error(f"Incorrect theme id -> {theme_id}")
            return f"Incorrect theme id -> {theme_id}"

    @classmethod
    def get_application_form(cls, app_json_blob):
        """function return list of all questions from application form"""

        return [
            questions
            for forms in app_json_blob["jsonb_blob"]["forms"]
            for questions in forms["questions"]
        ]

    @classmethod
    def convert_boolean_values(cls, themes_answers: list[dict]) -> list[dict]:
        """function checks boolean values in themes_answers & replace
        boolean values to string. (False -> "No", True -> "Yes")
        Args:
            themes_answers (_type_): array of dict
        """
        current_app.logger.info("Converting boolean values to strings")
        for answers in themes_answers:
            if "answer" in answers.keys():
                if answers["answer"] == False:
                    answers.update(answer="No")
                if answers["answer"] == True:
                    answers.update(answer="Yes")

    @classmethod
    def sort_add_another_component_contents(
        cls, themes_answers: list[dict]
    ) -> list[dict]:
        """function checks for special presentation_type "heading"
        in array of themes answers, if exists, adds question-value
        to an answer key for presentation_type "heading" theme and
        looks for presentation_type of "description" and "amount" with
        same presentation_type "heading"s field_id, retrieve words only
        from strings of answers for presentation_type "description" theme
        & numbers only for presentation_type "amount" theme.

        Args:
            themes_answers (_type_): array of dict
        """
        for heading in themes_answers:
            try:
                if heading["presentation_type"] == "heading":
                    current_app.logger.info(
                        "mapping add-another component contents"
                    )
                    heading["answer"] = heading["question"]
                    for theme in themes_answers:
                        if (
                            heading["field_id"] in theme.values()
                            and theme["presentation_type"] == "description"
                        ):
                            description_answer = [
                                description.rsplit(": ", 1)[0]
                                for description in theme["answer"]
                            ]
                            theme["answer"] = description_answer

                        if (
                            heading["field_id"] in theme.values()
                            and theme["presentation_type"] == "amount"
                        ):
                            amount_answer = [
                                amount.split(": ")[1]
                                for amount in theme["answer"]
                            ]

                            theme["answer"] = amount_answer

                        else:
                            continue

            except (KeyError, IndexError):
                current_app.logger.error("Incorrect field key")

    @classmethod
    def map_grouped_fields_answers(cls, theme: dict, questions: dict) -> tuple:
        """function looks for list of grouped field_ids such as ["JzWvhj", "jLIgoi"],
        maps them  with question keys and returns a list of answers
        for given field ids"""

        for question in questions:
            answer_list = tuple(
                (
                    (app["title"], app["answer"])
                    for app in question["fields"]
                    for field_id in theme["field_id"]
                    if "answer" in app.keys() and app["key"] == field_id
                )
            )
            if answer_list:
                theme["answer"] = answer_list

    @classmethod
    def map_single_field_answer(cls, theme: list, questions: dict) -> str:
        """function looks for a field_id, maps it with question keys
        and returns an answer for given field id"""
        for question in questions:
            for app_fields in question["fields"]:
                if (
                    theme["field_id"] == app_fields["key"]
                    and "answer" in app_fields.keys()
                ):
                    theme["answer"] = app_fields["answer"]

    @classmethod
    def map_application_with_sub_criteria_themes(
        cls, application_id: str, theme_id: str
    ):
        """function maps answers from application with assessor task list
        themes through field ids.
        Args: application_id, theme_id
        Exceptions: returning custom exception along with openapi
        validation detail.
        """

        themes_answers = cls.get_themes_answers(theme_id)
        application_json_blob = get_application_jsonb_blob(application_id)
        questions = cls.get_application_form(application_json_blob)

        current_app.logger.info("mapping subcriteria theme contents")
        for theme in themes_answers:
            try:
                if isinstance(theme["field_id"], list):
                    cls.map_grouped_fields_answers(theme, questions)
                else:
                    cls.map_single_field_answer(theme, questions)
            except TypeError:
                current_app.logger.error(f"Incorrect theme id -> {theme_id}")
                return f"Incorrect theme id -> {theme_id}"

        cls.convert_boolean_values(themes_answers)
        cls.sort_add_another_component_contents(themes_answers)
        current_app.logger.info(
            "Successfully mapped subcriteria theme contents"
        )
        return themes_answers
