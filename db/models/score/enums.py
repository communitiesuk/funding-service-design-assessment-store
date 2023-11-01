from enum import Enum


class ScoringSysyem(Enum):
    """The ENUM used by `db.models.ScoringSystem` to validate the
    possible values for the `scoring_system` column."""

    OneToFive = 0
    ZeroToThree = 1
