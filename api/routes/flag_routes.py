from flask import current_app, request

from db.models.flags.flag_update import FlagStatus
from db.queries import get_metadata_for_fund_round_id
from db.queries.flags.queries import (
    add_flag_for_application,
    add_update_to_assessment_flag,
    get_flag_by_id,
    get_flags_for_application,
)
from db.schemas.schemas import AssessmentFlagSchema


def _fix_country(country):
    country = country.strip().casefold()
    if country == "northernireland":
        country = "northern ireland"
    return country


def get_team_flag_stats(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    funding_type: str = "ALL",
    asset_type: str = "ALL",
    status: str = "ALL",
    search_in: str = "",
    countries: str = "all",
):
    assessment_overview_flags = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
        countries=[_fix_country(c) for c in countries.split(",") if c],
        search_in=search_in,
        funding_type=funding_type,
    )

    def create_team_dict(team_name):
        return {
            "team_name": team_name,
            "raised": 0,
            "resolved": 0,
            "stopped": 0,
        }

    team_flag_stats = []

    for assessment in assessment_overview_flags:
        for flag in assessment.get("flags", []):
            latest_status = flag.get("latest_status")
            allocated_team = flag.get("latest_allocation")

            if allocated_team not in [team["team_name"] for team in team_flag_stats]:
                team_flag_stats.append(create_team_dict(allocated_team))

            for team in team_flag_stats:
                if team["team_name"] == allocated_team:
                    if latest_status == FlagStatus.RAISED:
                        team["raised"] += 1
                    elif latest_status == FlagStatus.STOPPED:
                        team["stopped"] += 1
                    elif latest_status == FlagStatus.RESOLVED:
                        team["resolved"] += 1

    return team_flag_stats


def get_flag(flag_id: str):
    current_app.logger.info("Get flags for id {flag_id}", extra=dict(flag_id=flag_id))
    flags = get_flag_by_id(flag_id)
    flag_schema = AssessmentFlagSchema()
    return flag_schema.dump(flags, many=True)[0]


def get_all_flags_for_application(application_id):
    current_app.logger.info("Get all flags for application {application_id}", extra=dict(application_id=application_id))
    flags = get_flags_for_application(application_id)
    flag_schema = AssessmentFlagSchema()
    return flag_schema.dump(flags, many=True)


def create_flag_for_application():
    create_flag_json = request.json
    current_app.logger.info(
        "Create flag for application {application_id}", extra=dict(application_id=create_flag_json["application_id"])
    )
    created_flag = add_flag_for_application(**create_flag_json)
    return AssessmentFlagSchema().dump(created_flag)


def update_flag_for_application():
    current_app.logger.info("Update flag")
    update_flag_json = request.json
    updated_flag = add_update_to_assessment_flag(**update_flag_json)
    return AssessmentFlagSchema().dump(updated_flag)
