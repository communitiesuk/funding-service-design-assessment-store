# flake8: noqa
from config.mappings.cof_mapping_parts.cof_r2_scored_criteria import (
    scored_criteria as cof_scored_criteria,
)
from config.mappings.cof_mapping_parts.cof_r2_unscored_sections import (
    unscored_sections as cof_unscored_sections,
)
from config.mappings.nstf_mapping_parts.nstf_r2_scored_criteria import (
    scored_criteria as nstf_scored_criteria,
)
from config.mappings.nstf_mapping_parts.nstf_r2_unscored_sections import (
    unscored_sections as nstf_unscored_sections,
)

cof_r2w2_assessment_mapping = {
    "schema_id": "cof_r2w2_assessment",
    "unscored_sections": cof_unscored_sections,
    "scored_criteria": cof_scored_criteria,
}

cof_r2w3_assessment_mapping = {
    "schema_id": "cof_r2w3_assessment",
    "unscored_sections": cof_unscored_sections,
    "scored_criteria": cof_scored_criteria,
}

nstf_r2_assessment_mapping = {
    "schema_id": "nstf_r2_assessment",
    "unscored_sections": nstf_unscored_sections,
    "scored_criteria": nstf_scored_criteria,
}

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
NIGHT_SHELTER_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NIGHT_SHELTER_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"

fund_round_to_assessment_mapping = {
    f"{COF_FUND_ID}:{COF_ROUND_2_ID}": cof_r2w2_assessment_mapping,
    f"{COF_FUND_ID}:{COF_ROUND_2_W3_ID}": cof_r2w3_assessment_mapping,
    f"{NIGHT_SHELTER_FUND_ID}:{NIGHT_SHELTER_ROUND_2_ID}": nstf_r2_assessment_mapping,
}
