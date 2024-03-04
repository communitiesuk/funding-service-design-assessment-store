import copy

from bs4 import BeautifulSoup
from config import Config
from db.models.assessment_record.enums import Status
from flask import current_app


def _derive_status(score_map: dict, comment_map: dict, sub_criteria_id: str) -> str:
    if sub_criteria_id in score_map:
        return Status.COMPLETED.name  # if we've scored, we've completed
    if sub_criteria_id in comment_map:
        return Status.IN_PROGRESS.name  # if we've commented, but not scored, we're in progress

    # if we haven't commented or scored, we're not started
    return Status.NOT_STARTED.name


def transform_to_assessor_task_list_metadata(
    fund_id: str, round_id: str, score_map: dict, comment_map: dict
) -> tuple[dict, dict]:
    current_app.logger.info("Configured fund-rounds:")
    current_app.logger.info(Config.ASSESSMENT_MAPPING_CONFIG.keys())
    mapping = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])

    sections = [
        {
            "name": s["name"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                }
                for sc in s["sub_criteria"]
            ],
        }
        for s in mapping["unscored_sections"]
    ]

    criterias = [
        {
            "name": c["name"],
            "total_criteria_score": sum(score_map.get(sc["id"], 0) for sc in c["sub_criteria"]),
            "number_of_scored_sub_criteria": sum(1 for _ in c["sub_criteria"]),
            "weighting": c["weighting"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                    "score": score_map.get(sc["id"]),
                    "theme_count": len(sc["themes"]),
                    "status": _derive_status(score_map, comment_map, sc["id"]),
                }
                for sc in c["sub_criteria"]
            ],
        }
        for c in mapping["scored_criteria"]
    ]

    return sections, criterias


def strip_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_html_tags(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = remove_html_tags(value)
    elif isinstance(data, list):
        data = [remove_html_tags(item) for item in data]
    if isinstance(data, str):
        data = strip_tags(data)
    return data
