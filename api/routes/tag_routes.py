# flake8: noqa
from db.queries.tags.queries import insert_tags_ignore_duplicates
from db.queries.tags.queries import select_tags_for_fund_round
from db.schemas.schemas import TagSchema
from flask import abort
from flask import request


def get_tags_for_fund_round(fund_id, round_id):

    tags = select_tags_for_fund_round(fund_id, round_id)

    if tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in tags]
        return serialised_tags

    abort(404)


def add_tags_for_fund_round(fund_id, round_id):
    args = request.get_json()
    tag_value = args["value"]
    tag_colour = args["colour"]
    tag_creator = args["user"]

    tags = [{"value": tag_value, "colour": tag_colour, "user": tag_creator}]

    tags = insert_tags_ignore_duplicates(tags, fund_id, round_id)

    if tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in tags]
        return serialised_tags

    abort(404)
