import copy

from config import Config
from db.queries.assessment_records.queries import get_application_jsonb_blob
from flask import abort
from flask import current_app


def get_all_subcriteria(fund_id, round_id):
    sub_criterias = []
    display_config = copy.deepcopy(
        Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"]
    )
    for section in (
        display_config["scored_criteria"] + display_config["unscored_sections"]
    ):
        for sub_criteria in section["sub_criteria"]:
            sub_criterias.append(sub_criteria)
    return sub_criterias


def return_subcriteria_from_mapping(sub_criteria_id, fund_id, round_id):
    current_app.logger.info(
        f"Finding sub criteria data in config for: {sub_criteria_id}"
    )
    display_config = copy.deepcopy(
        Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"]
    )
    sub_criterias = get_all_subcriteria(fund_id, round_id)
    matching_sub_criteria = list(
        filter(
            lambda sub_criteria: sub_criteria["id"] == sub_criteria_id,
            sub_criterias,
        )
    )
    if len(matching_sub_criteria) == 1:
        sub_crit = matching_sub_criteria[0]

        is_scored = False
        for criteria in display_config["scored_criteria"]:
            for sub_criteria in criteria["sub_criteria"]:
                if sub_criteria_id == sub_criteria["id"]:
                    is_scored = True
        sub_crit["is_scored"] = is_scored

        return sub_crit
    elif len(matching_sub_criteria) > 1:
        msg = "sub_criteria: '{sub_criteria_id}' duplicated."
        current_app.logger.error(msg)
        raise ValueError(msg)
    else:
        msg = f"sub_criteria: '{sub_criteria_id}' not found."
        current_app.logger.warn(msg)
        abort(404, description=msg)


def get_themes_fields(
    theme_id: str, fund_id: str, round_id: str
) -> list[dict]:
    """function takes a theme_id arg & returns a list
    of answers with given theme_id.
    """
    sub_criterias = get_all_subcriteria(fund_id, round_id)
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


def get_application_form(app_json_blob):
    """function return list of all questions from application form"""

    return [
        questions
        for forms in app_json_blob["jsonb_blob"]["forms"]
        for questions in forms["questions"]
    ]


def convert_boolean_values(themes_fields: list[dict]) -> list[dict]:
    """function checks boolean values in themes_answers & replace
    boolean values to string. (False -> "No", True -> "Yes")
    Args:
        themes_fields (_type_): array of dict
    """
    current_app.logger.info("Converting boolean values to strings")
    for field in themes_fields:
        if "answer" in field.keys():
            if field["answer"] is False:
                field.update(answer="No")
            if field["answer"] is True:
                field.update(answer="Yes")
            else:
                continue


def sort_add_another_component_contents(
    themes_fields: list[dict],
) -> list[dict]:
    """function checks for special presentation_type "heading"
    in array of themes fields, if exists, adds question-value
    to an answer key for presentation_type "heading" theme and
    looks for presentation_type of "description" and "amount" with
    same presentation_type "heading"s field_id, retrieve words
    onlyproject-costs from strings of answers for
    presentation_type "description" theme& numbers only
    for presentation_type "amount" theme.

    Args:
        themes_answers (_type_): array of dict
    """
    for field in themes_fields:
        try:
            if field["presentation_type"] == "heading":
                current_app.logger.info(
                    "mapping add-another component contents"
                )
                field["answer"] = field["question"]
                # match each add-another answer
                for theme in themes_fields:
                    if (
                        field["field_id"] in theme.values()
                        and theme["presentation_type"] == "description"
                    ):
                        description_answer = [
                            description.rsplit(": ", 1)[0]
                            for description in theme["answer"]
                        ]
                        theme["answer"] = description_answer

                    if (
                        field["field_id"] in theme.values()
                        and theme["presentation_type"] == "amount"
                    ):
                        amount_answer = [
                            amount.rsplit(": ", 1)[1]
                            for amount in theme["answer"]
                        ]

                        theme["answer"] = amount_answer

            else:
                continue

        except (KeyError, IndexError):
            current_app.logger.debug(
                f"Answer not provided for field_id: {field['field_id']}"
            )


def map_grouped_fields_answers(theme: dict, questions: dict) -> tuple:
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


def map_single_field_answer(theme: list, questions: dict) -> str:
    """function looks for a field_id, maps it with question keys
    and returns an answer for given field id"""
    for question in questions:
        for app_fields in question["fields"]:
            if (
                theme["field_id"] == app_fields["key"]
                and "answer" in app_fields.keys()
            ):
                # TODO: Refactor this work-around for the
                # temporary state of the add-another component
                # we check if this is of type "add-another"
                # and convert into a consumable format
                if (
                    isinstance(app_fields["answer"], list)
                    and "type-of-revenue-cost" in app_fields["answer"][0]
                ):
                    theme["answer"] = [
                        f"{item['type-of-revenue-cost']} : £{item['value']}"
                        for item in app_fields["answer"]
                    ]
                else:
                    theme["answer"] = app_fields["answer"]


def map_application_with_sub_criteria_themes(
    application_id: str, theme_id: str, fund_id: str, round_id: str
):
    """function maps answers from application with assessor task list
    themes through field ids.
    Args: application_id, theme_id, fund_id, round_id
    Exceptions: returning custom exception along with openapi
    validation detail.
    """

    themes_fields = get_themes_fields(theme_id, fund_id, round_id)
    application_json_blob = get_application_jsonb_blob(application_id)
    questions = get_application_form(application_json_blob)

    current_app.logger.info("mapping subcriteria theme contents")
    for theme in themes_fields:
        try:
            if isinstance(theme["field_id"], list):
                map_grouped_fields_answers(theme, questions)
            else:
                map_single_field_answer(theme, questions)
        except TypeError:
            current_app.logger.error(f"Incorrect theme id -> {theme_id}")
            return f"Incorrect theme id -> {theme_id}"

    convert_boolean_values(themes_fields)
    sort_add_another_component_contents(themes_fields)
    current_app.logger.info("Successfully mapped subcriteria theme contents")
    return themes_fields
