from contextlib import contextmanager

from db import db
from db.models.assessment_record import AssessmentRecord
from sqlalchemy import event
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import defer


@contextmanager
def no_gather_sql():
    @event.listens_for(Engine, "before_cursor_execute", retval=True)
    def mark_as_ignore(
        conn, cursor, statement, parameters, context, executemany
    ):
        statement = statement + " --IGNORE"
        return statement, parameters

    yield

    event.remove(Engine, "before_cursor_execute", mark_as_ignore)


@no_gather_sql()
def get_random_row(table):
    """get_random_row Uses a database-side select to get a random row. Does
    this by using a random offset with range (1, number of rows)

    :param table: Sqlalchemy mapper object
    :return: A random row from the given mapper.
    """

    primary_key_name = inspect(table).primary_key[0].name
    primary_key_column = getattr(table, primary_key_name)
    return (
        db.session.query(table)
        .offset(
            func.floor(
                func.random()
                * db.session.query(func.count(primary_key_column))
            )
        )
        .limit(1)
        .one()
    )


@no_gather_sql()
def get_rows_by_filters(fund_id, round_id, filters):
    """get_rows_by_asset_type Uses a database-side where to get rows
    for provided asset type

    :param table: fund_id, round_id, asset_type
    :return: rows for given assest type.
    """
    stmt = (
        select(AssessmentRecord)
        # Dont load json into memory
        .options(defer(AssessmentRecord.jsonb_blob)).where(
            AssessmentRecord.fund_id == fund_id,
            AssessmentRecord.round_id == round_id,
            *filters,
        )
    )
    return db.session.scalars(stmt).all()


@no_gather_sql()
def get_assessment_record(application_id):
    """get_rows_by_asset_type Uses a database-side where to get rows
    for provided asset type

    :param table: fund_id, round_id, asset_type
    :return: rows for given assest type.
    """
    stmt = (
        select(AssessmentRecord)
        # Dont load json into memory
        .options(defer(AssessmentRecord.jsonb_blob)).where(
            AssessmentRecord.application_id == application_id,
        )
    )
    return db.session.scalars(stmt).one()
