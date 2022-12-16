APPLICATION_METADATA_RESPONSE = {
    "criterias": [
        {
            "name": "Strategic case",
            "sub_criterias": [
                {
                    "id": "benefits",
                    "name": "Benefits",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 2
                },
                {
                    "id": "engagement",
                    "name": "Engagement",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 2
                },
                {
                    "id": "environmental_sustainability",
                    "name": "Environmental Sustainability",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 1
                }
            ],
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.3
        },
        {
            "name": "Management case",
            "sub_criterias": [
                {
                    "id": "funding_breakdown",
                    "name": "Funding breakdown",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 1
                },
                {
                    "id": "financial_and_risk_forecasts",
                    "name": "Financial and risk forecasts",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 3
                },
                {
                    "id": "skills_and_resources",
                    "name": "Skills and resources",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 3
                },
                {
                    "id": "representation_inclusiveness_and_integration",
                    "name": "Representation, inclusiveness and integration",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 2
                },
                {
                    "id": "business_plan",
                    "name": "Business plan",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 1
                }
            ],
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.3
        },
        {
            "name": "Potential to deliver community benefit",
            "sub_criterias": [
                {
                    "id": "community-benefits",
                    "name": "How the community benefits\t",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 2
                }
            ],
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.3
        },
        {
            "name": "Added value of the community asset",
            "sub_criterias": [
                {
                    "id": "value-to-the-community",
                    "name": "Value to the community",
                    "score": -1,
                    "status": "Not started",
                    "theme_count": 1
                }
            ],
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.1
        }
    ],
    "date_submitted": "2022-10-27T08:32:13.383999",
    "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
    "project_name": "Mock that is used to test Assessors Task List",
    "short_id": "COF-R2W2-JWBTLN",
    "sections": [
        {
            "name": "Organisation information",
            "sub_criterias": [
                {
                    "id": "org_info",
                    "name": "Organisation information"
                },
                {
                    "id": "applicant_info",
                    "name": "Applicant information"
                }
            ]
        },
        {
            "name": "Project information",
            "sub_criterias": [
                {
                    "id": "project_info",
                    "name": "Project information"
                },
                {
                    "id": "asset_info",
                    "name": "Asset information"
                }
            ]
        },
        {
            "name": "Check declarations",
            "sub_criterias": [
                {
                    "id": "declarations",
                    "name": "Declarations"
                },
                {
                    "id": "subsidy_control_and_state_aid",
                    "name": "Subsidy control and state aid"
                }
            ]
        }
    ],
    "workflow_status": "NOT_STARTED"
}

subcriteria_themes_and_expected_response = {
    "community_use": "Test",
    "risk_loss_impact": "Test",
    "engaging-the-community": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
    "local-support": "Tell us how your project supports any wider local plans",
    "environmental-considerations": "Test",
    "funding_requested": (
        ('Capital funding', '2300'), ('Revenue funding (optional)', '2300')
    ),
    "risk": "sample1.doc",
    "income_and_running_costs": "Test",
    "previous_experience": "No",
    "governance_and_structures": "Test",
    "recruitment": "No",
    "representing_community_views": "Test",
    "accessibility_and_inclusivity": "Test",
}
