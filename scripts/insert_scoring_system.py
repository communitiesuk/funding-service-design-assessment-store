#!/usr/bin/env python3
# flake8: noqa
import argparse

from app import app  # noqa: E402
from db.queries.scores.queries import insert_scoring_system_for_round_id


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import applications from application store."
    )
    parser.add_argument(
        "--round_id",
        type=str,
        help="Provide round id of the fund.",
        required=False,
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if args.round_id:
        roundid = args.round_id
    else:
        raise Exception("Please provide all the required arguments.")

    with app.app_context():
        inserted_scoring_system = insert_scoring_system_for_round_id(
            roundid, "OneToFive"
        )
        return inserted_scoring_system


if __name__ == "__main__":
    main()
