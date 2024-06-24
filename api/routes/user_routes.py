from db.queries.assessment_records.queries import create_user_application_association
from db.queries.assessment_records.queries import get_user_application_associations
from db.queries.assessment_records.queries import (
    update_user_application_association as update_user_application_association_db,
)
from db.schemas.schemas import AllocationAssociationSchema
from flask import abort
from flask import current_app
from flask import request


def get_all_users_associated_with_application(application_id, active=None):
    associations = get_user_application_associations(application_id=application_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(f"Could not find any users associated with application {application_id}")
    abort(404)


def get_user_application_association(application_id, user_id):
    association = get_user_application_associations(application_id=application_id, user_id=user_id)

    if association:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association[0])

    current_app.logger.error(f"Could not find association between {user_id} and application {application_id}")
    abort(404)


def add_user_application_association(application_id, user_id):
    association = create_user_application_association(application_id=application_id, user_id=user_id)

    if association:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association), 201

    current_app.logger.error(f"Could not create association between {user_id} and application {application_id}")
    abort(404)


def update_user_application_association(application_id, user_id):
    args = request.get_json()
    if "active" not in args:
        abort(400)

    active = True if args.get("active").lower() == "true" else False
    association = update_user_application_association_db(application_id=application_id, user_id=user_id, active=active)

    if association:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association)

    current_app.logger.error(f"Could not update association between {user_id} and application {application_id}")
    abort(404)


def get_all_applications_associated_with_user(user_id, active=None):
    associations = get_user_application_associations(user_id=user_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(f"Could not find any applications associated with user {user_id}")
    abort(404)
