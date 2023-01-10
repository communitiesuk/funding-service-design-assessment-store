from typing import Dict
from typing import List

from config.mappings.mapping_parts.scored_criteria import scored_criteria
from db.queries.scores.queries import get_scores_for_app_sub_crit


def get_progress_for_application(application_id: str) -> Dict:
    """get_progress_for_application Function
    used by the get endpoint `/progress.
    :param application_id: The stringified application UUID.
    :return: An object containing the progress of the application
    """

    scored_sub_crit_list = [
        subcrit["id"]
        for crit in scored_criteria
        for subcrit in crit["sub_criteria"]
        if subcrit["id"] != "themes"
    ]

    # count how many of the application's scored subcrits are scored
    # (get latest score per subcrit)
    scored_sub_crit_list_for_application = [
        score
        for sub_crit in scored_sub_crit_list
        for score in get_scores_for_app_sub_crit(application_id, sub_crit)
    ]

    # calculate percentage and return the int as the progress value
    progress = int(
        len(scored_sub_crit_list_for_application)
        / len(scored_sub_crit_list)
        * 100
    )
    return_dict = {
        "application_id": application_id,
        "progress": progress,
    }
    return return_dict


def get_bulk_progress_for_applications(
    application_ids: List[str],
) -> List[Dict]:
    """get_progress_for_application Function
    used by the get endpoint `/bulk_progress.
    :param application_ids: List of stringified applications' UUIDs.
    :return: List of objects containing the progress of the application
    """
    progress_list = []
    for application_id in application_ids:
        progress = get_progress_for_application(application_id)
        progress_list.append(progress)
    return progress_list
