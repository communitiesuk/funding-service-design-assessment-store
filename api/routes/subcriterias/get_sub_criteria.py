import copy

from config import Config
from flask import abort
from flask import current_app


def get_all_subcriteria(fund_id, round_id, language):
    sub_criterias = []
    display_config = copy.deepcopy(
        Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"]
    )
    for section in (
        display_config["scored_criteria"] + display_config["unscored_sections"]
    ):
        for sub_criteria in section["sub_criteria"]:
            for theme in sub_criteria["themes"]:
                for answer in theme["answers"]:
                    answer["form_name"] = (
                        answer["form_name"][language]
                        if isinstance(answer["form_name"], dict)
                        else answer["form_name"]
                    )
                    if "path" in answer:
                        answer["path"] = (
                            answer["path"][language]
                            if isinstance(answer["path"], dict)
                            else answer["path"]
                        )
            sub_criterias.append(sub_criteria)
    return sub_criterias


def return_subcriteria_from_mapping(
    sub_criteria_id, fund_id, round_id, language
):
    current_app.logger.info(
        f"Finding sub criteria data in config for: {sub_criteria_id}"
    )
    display_config = copy.deepcopy(
        Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"]
    )
    sub_criterias = get_all_subcriteria(fund_id, round_id, language)
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
        current_app.logger.warning(msg)
        abort(404, description=msg)
