"""Flask Dev Pipeline Environment Configuration."""
from config.envs.default import DefaultConfig
from config.mappings.assessment_mapping_fund_round import fund_round_data_key_mappings
from config.mappings.assessment_mapping_fund_round import fund_round_mapping_config
from config.mappings.assessment_mapping_fund_round import fund_round_to_assessment_mapping
from config.mappings.sf_mapping_parts.r1_unscored_sections import (
    unscored_sections as sf_unscored_sections,
)
from fsd_utils import configclass


@configclass
class DevConfig(DefaultConfig):
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SF_FUND_ID = "91504db1-2f21-4177-ac1b-05c9246d5b55"
    SF_ROUND_1_ID = "f54d5cfa-79b5-4706-9c55-37cc927af66f"

    fund_round_to_assessment_mapping.update(
        {
            f"{SF_FUND_ID}:{SF_ROUND_1_ID}": {
                "schema_id": "sf_r1_assessment",
                "unscored_sections": sf_unscored_sections,
                "scored_criteria": [],
            }
        }
    )

    ASSESSMENT_MAPPING_CONFIG = fund_round_to_assessment_mapping

    fund_round_data_key_mappings.update(
        {
            "SFR1": {
                "location": None,
                "asset_type": None,
                "funding_one": None,
                "funding_two": None,
            },
        }
    )

    DATA_KEY_MAPPING_CONFIG = fund_round_data_key_mappings

    fund_round_mapping_config.update(
        {
            "SFR1": {
                "fund_id": SF_FUND_ID,
                "round_id": SF_ROUND_1_ID,
                "type_of_application": "SF",
            }
        }
    )

    FUND_ROUND_MAPPING_CONFIG = fund_round_mapping_config
