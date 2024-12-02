from flask import Response, abort, current_app, request

from db.queries.assessment_records.queries import (
    associate_assessment_tags,
    select_active_tags_associated_with_assessment,
    select_all_tags_associated_with_application,
)
from db.queries.tags.queries import (
    get_tag_by_id,
    insert_tags,
    select_tags_for_fund_round,
    select_tags_types,
    update_tags,
)
from db.schemas.schemas import (
    JoinedTagAssociationSchema,
    JoinedTagSchema,
    TagAssociationSchema,
    TagSchema,
    TagTypeSchema,
)


def get_tags_for_fund_round(
    fund_id,
    round_id,
    tag_purpose: str = "ALL",
    tag_status: bool = None,
    search_term: str = "",
    search_in: str = None,
):
    tags = select_tags_for_fund_round(fund_id, round_id, tag_purpose, tag_status, search_term, search_in)

    if tags:
        serialiser = JoinedTagSchema()
        serialised_tags = [serialiser.dump(r) for r in tags]
        return serialised_tags

    return Response(
        response=[],
        status=204,
        headers={"Content-Type": "application/json"},
    )


def get_tag_types():
    tag_types = select_tags_types()

    if tag_types:
        serialiser = TagTypeSchema()
        serialised_tag_types = [serialiser.dump(r) for r in tag_types]
        return serialised_tag_types

    return Response(response="No tags types.", status=204)


def add_tag_for_fund_round(fund_id, round_id):
    args = request.get_json()
    tag_value = args["value"]
    tag_type_id = args["tag_type_id"]
    creator_user_id = args["creator_user_id"]

    tags = [
        {
            "value": tag_value,
            "tag_type_id": tag_type_id,
            "creator_user_id": creator_user_id,
        }
    ]

    inserted_tags = insert_tags(tags, fund_id, round_id)

    if inserted_tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in inserted_tags]
        return serialised_tags
    current_app.logger.error("Add tags attempt failed for tags: {tags}.", extra=dict(tags=tags))
    abort(404)


def update_tags_for_fund_round(fund_id, round_id):
    args = request.get_json()

    tags = [
        {
            "id": arg.get("id"),
            "value": arg.get("value"),
            "tag_type_id": arg.get("tag_type_id"),
            "creator_user_id": arg.get("creator_user_id"),
            "active": arg.get("active"),
        }
        for arg in args
    ]

    updated_tags = update_tags(tags, fund_id, round_id)

    if updated_tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in updated_tags]
        return serialised_tags
    current_app.logger.error("Update tags attempt failed for tags: {tags}.", extra=dict(tags=tags))
    abort(404)


def get_tag(fund_id, round_id, tag_id):
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    if not tag:
        return abort(404)
    return JoinedTagSchema().dump(tag)


def associate_tags_with_assessment(application_id):
    args = request.get_json()
    tags = args
    current_app.logger.info("Associating tag with assessment")
    associated_tags = associate_assessment_tags(application_id, tags)

    if associated_tags:
        serialiser = TagAssociationSchema()
        serialised_associated_tags = [serialiser.dump(r) for r in associated_tags]
        return serialised_associated_tags


def get_active_tags_associated_with_assessment(application_id):
    current_app.logger.info(
        "Getting tags associated with assessment with application_id: {application_id}.",
        extra=dict(application_id=application_id),
    )
    associated_tags = select_active_tags_associated_with_assessment(application_id)
    if associated_tags:
        serialiser = JoinedTagAssociationSchema()
        serialised_associated_tags = [serialiser.dump(r) for r in associated_tags]
        return serialised_associated_tags
    return []


def get_all_tags_associated_with_application(application_id):
    current_app.logger.info(
        "Getting tags associated with with application_id: {application_id}.", extra=dict(application_id=application_id)
    )
    associated_tags = select_all_tags_associated_with_application(application_id)
    if associated_tags:
        serialiser = JoinedTagAssociationSchema()
        serialised_associated_tags = [serialiser.dump(r) for r in associated_tags]
        return serialised_associated_tags
    return []
