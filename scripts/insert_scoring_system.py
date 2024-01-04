#!/usr/bin/env python3
# flake8: noqa
import argparse

from app import app  # noqa: E402
from db.queries.scores.queries import insert_scoring_system_for_round_id

# Update scoring systems when new ones are added
scoring_systems = ["OneToFive"]


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

    parser.add_argument(
        "--scoring_system",
        type=str,
        choices=scoring_systems,
        help="Provide round id of the fund.",
        required=False,
    )
    return parser


def display_scoring_systems():
    BLUE = "\033[94m"
    RESET = "\033[0m"
    print(f"- {BLUE}Available scoring systems:{RESET}")
    for system in scoring_systems:
        print(f"- {BLUE}{system}{RESET}")

    choice = input("Choose a scoring system from the list: ")
    return choice.strip() if choice in scoring_systems else None


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if args.round_id:
        round_id = args.round_id
    else:
        raise Exception("Please provide all the required arguments.")

    with app.app_context():
        selected_scoring_system = display_scoring_systems()
        if selected_scoring_system:
            inserted_scoring_system = insert_scoring_system_for_round_id(
                round_id, selected_scoring_system
            )
            print(inserted_scoring_system)
            print("Scoring system inserted successfully")
            return inserted_scoring_system
        else:
            raise ValueError(
                "Invalid choice for scoring system. Please choose from the list."
            )


if __name__ == "__main__":
    main()
