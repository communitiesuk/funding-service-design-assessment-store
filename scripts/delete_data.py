#!/usr/bin/env python3
import click
from db import db
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record import TagAssociation
from db.models.comment import Comment
from db.models.comment import CommentsUpdate
from db.models.flags import AssessmentFlag
from db.models.flags import FlagUpdate
from db.models.score import Score


def delete_single_assessment(application_id: str):
    assessment_record = AssessmentRecord.query.get(application_id)
    if assessment_record:
        db.session.query(TagAssociation).filter(TagAssociation.application_id == application_id).delete()
        db.session.query(Score).filter(Score.application_id == application_id).delete()

        associated_flags = db.session.query(AssessmentFlag).filter(AssessmentFlag.application_id == application_id)
        if associated_flags.count() > 0:
            db.session.query(FlagUpdate).filter(
                FlagUpdate.assessment_flag_id.in_(
                    db.session.query(AssessmentFlag.id).filter(AssessmentFlag.application_id == application_id)
                )
            ).delete()
            associated_flags.delete()

        comments = db.session.query(Comment).filter(Comment.application_id == application_id)
        if comments.count() > 0:
            db.session.query(CommentsUpdate).filter(
                CommentsUpdate.comment_id.in_(
                    db.session.query(Comment.id).filter(Comment.application_id == application_id)
                )
            ).delete()
            comments.delete()
        db.session.delete(assessment_record)
        db.session.commit()
        print(f"Deleted assessment record with application id {application_id}")


@click.group()
@click.pass_context
def cli(ctx):
    # Ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)


@cli.command()
@click.option("-id", prompt=True)
def delete_assessment_record(id):
    delete_single_assessment(id)


@cli.command()
@click.option("-r", "--round-id", prompt=True)
def delete_all_assessments_in_round(round_id):
    results = db.session.query(AssessmentRecord.application_id).filter(AssessmentRecord.round_id == round_id)
    if results.count() > 0:
        for r in results.all():
            delete_single_assessment(str(r[0]))
    else:
        print(f"No assessments found for round {round_id}")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        cli()
