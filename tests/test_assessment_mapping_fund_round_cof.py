from uuid import UUID

import pytest
from config import Config
from config.mappings.assessment_mapping_fund_round import applicant_info_mapping
from config.mappings.assessment_mapping_fund_round import COF25_EOI_FUND_ID
from config.mappings.assessment_mapping_fund_round import COF25_EOI_ROUND_ID
from config.mappings.assessment_mapping_fund_round import COF25_FUND_ID
from config.mappings.assessment_mapping_fund_round import COF25_ROUND_ID
from config.mappings.assessment_mapping_fund_round import COF_EOI_FUND_ID
from config.mappings.assessment_mapping_fund_round import COF_EOI_ROUND_ID


def test_fund_round_ids_are_valid_uuids():
    """Test that fund and round IDs are valid UUIDs."""
    # Test COF EOI IDs
    assert isinstance(UUID(COF_EOI_FUND_ID), UUID)
    assert isinstance(UUID(COF_EOI_ROUND_ID), UUID)

    # Test COF25 EOI IDs
    assert isinstance(UUID(COF25_EOI_FUND_ID), UUID)
    assert isinstance(UUID(COF25_EOI_ROUND_ID), UUID)

    # Test COF25 IDs
    assert isinstance(UUID(COF25_FUND_ID), UUID)
    assert isinstance(UUID(COF25_ROUND_ID), UUID)


def test_fund_round_to_assessment_mapping_structure():
    """Test the structure and content of fund_round_to_assessment_mapping."""
    # Test COF EOI mapping
    cof_key = f"{COF_EOI_FUND_ID}:{COF_EOI_ROUND_ID}"
    assert cof_key in Config.ASSESSMENT_MAPPING_CONFIG
    assert Config.ASSESSMENT_MAPPING_CONFIG[cof_key]["schema_id"] == "cof_eoi_assessment"
    assert isinstance(Config.ASSESSMENT_MAPPING_CONFIG[cof_key]["unscored_sections"], list)
    assert isinstance(Config.ASSESSMENT_MAPPING_CONFIG[cof_key]["scored_criteria"], list)

    # Test COF25 EOI mapping
    cof25eoi_key = f"{COF25_EOI_FUND_ID}:{COF25_EOI_ROUND_ID}"
    assert cof25eoi_key in Config.ASSESSMENT_MAPPING_CONFIG
    assert Config.ASSESSMENT_MAPPING_CONFIG[cof25eoi_key]["schema_id"] == "cof25_eoi_assessment"
    assert isinstance(Config.ASSESSMENT_MAPPING_CONFIG[cof25eoi_key]["unscored_sections"], list)
    assert isinstance(Config.ASSESSMENT_MAPPING_CONFIG[cof25eoi_key]["scored_criteria"], list)

    # Test COF25 mapping
    cof25_key = f"{COF25_FUND_ID}:{COF25_ROUND_ID}"
    assert cof25_key in Config.ASSESSMENT_MAPPING_CONFIG
    assert Config.ASSESSMENT_MAPPING_CONFIG[cof25_key]["schema_id"] == "cof25_r1_assessment"
    assert isinstance(Config.ASSESSMENT_MAPPING_CONFIG[cof25_key]["unscored_sections"], list)
    assert isinstance(Config.ASSESSMENT_MAPPING_CONFIG[cof25_key]["scored_criteria"], list)


def test_fund_round_data_key_mappings_structure():
    """Test the structure of fund_round_data_key_mappings."""
    expected_keys_eoi = ["location", "asset_type", "funding_one", "funding_two"]
    expected_keys_cof = ["location", "asset_type", "funding_one", "funding_two", "funding_field_type"]

    assert "COFEOI" in Config.DATA_KEY_MAPPING_CONFIG
    assert "COF25EOI" in Config.DATA_KEY_MAPPING_CONFIG
    assert "COF25R1" in Config.DATA_KEY_MAPPING_CONFIG

    for fund_type in ["COFEOI", "COF25EOI"]:
        for key in expected_keys_eoi:
            assert key in Config.DATA_KEY_MAPPING_CONFIG[fund_type]
            assert Config.DATA_KEY_MAPPING_CONFIG[fund_type][key] is None

    for fund_type in ["COF25R1"]:
        for key in expected_keys_cof:
            assert key in Config.DATA_KEY_MAPPING_CONFIG[fund_type]
            assert Config.DATA_KEY_MAPPING_CONFIG[fund_type][key] is not None


def test_applicant_info_mapping_structure():
    """Test the structure and content of applicant_info_mapping."""
    for fund_id in [COF_EOI_FUND_ID, COF25_EOI_FUND_ID, COF25_FUND_ID]:
        assert fund_id in applicant_info_mapping
        assert "ASSESSOR_EXPORT" in applicant_info_mapping[fund_id]
        assert "OUTPUT_TRACKER" in applicant_info_mapping[fund_id]
        assert "form_fields" in applicant_info_mapping[fund_id]["ASSESSOR_EXPORT"]


def test_form_fields_structure():
    """Test the structure of form fields in applicant_info_mapping."""

    def check_field_structure(field_data):
        assert "en" in field_data
        assert "cy" in field_data
        assert "title" in field_data["en"]
        assert "title" in field_data["cy"]
        # Only check for field_type if it exists in both en and cy
        if "field_type" in field_data["en"] and "field_type" in field_data["cy"]:
            assert "field_type" in field_data["cy"]

    # Define the fund IDs separately
    fund_ids = {
        "COF_EOI_FUND_ID": COF_EOI_FUND_ID,
        "COF25_EOI_FUND_ID": COF25_EOI_FUND_ID,
        "COF25_FUND_ID": COF25_FUND_ID,
    }

    for fund_name, fund_id in fund_ids.items():
        form_fields = applicant_info_mapping[fund_id]["ASSESSOR_EXPORT"]["form_fields"]
        for field_id, field_data in form_fields.items():
            check_field_structure(field_data)


def test_fund_round_mapping_config_structure():
    """Test the structure and content of fund_round_mapping_config."""
    expected_keys = ["fund_id", "round_id", "type_of_application"]

    assert "COFEOI" in Config.FUND_ROUND_MAPPING_CONFIG
    assert "COF25EOI" in Config.FUND_ROUND_MAPPING_CONFIG
    assert "COF25R1" in Config.FUND_ROUND_MAPPING_CONFIG
    assert "RANDOM_FUND_ROUND" in Config.FUND_ROUND_MAPPING_CONFIG

    for config_type in Config.FUND_ROUND_MAPPING_CONFIG.values():
        for key in expected_keys:
            assert key in config_type


def test_field_types_consistency():
    """Test that field types are consistent across all form fields."""
    valid_field_types = {
        "yesNoField",
        "radiosField",
        "ukAddressField",
        "checkboxesField",
        "textField",
        "details",
        "numberField",
        "emailAddressField",
        "telephoneNumberField",
        "freeTextField",
        "sum_list",
        "uk_postcode",
    }

    for fund_id in [COF_EOI_FUND_ID, COF25_EOI_FUND_ID, COF25_FUND_ID]:
        form_fields = applicant_info_mapping[fund_id]["ASSESSOR_EXPORT"]["form_fields"]
        for field_data in form_fields.values():
            if "field_type" in field_data["en"]:
                assert field_data["en"]["field_type"] in valid_field_types


@pytest.mark.skip(reason="Welsh missing for some questions in the forms")
def test_bilingual_content():
    """Test that all content has both English and Welsh translations."""
    for fund_id in [COF_EOI_FUND_ID, COF25_EOI_FUND_ID, COF25_FUND_ID]:
        form_fields = applicant_info_mapping[fund_id]["ASSESSOR_EXPORT"]["form_fields"]
        for field_data in form_fields.values():
            assert field_data["en"]["title"] != ""
            assert field_data["cy"]["title"] != ""
            # Check that Welsh and English titles are different
            assert field_data["en"]["title"] != field_data["cy"]["title"]
