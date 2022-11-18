# flake8: noqa
# Ignore line length
cof_r2w2_assessment = {
    "schema_id": "cof_r2w2_assessment",
    "unscored_assessment_sections": [
        {
            "id": "organisation_info",
            "name": "Organisation information",
            "sub_criteria": [
                {
                    "id": "org_info",
                    "name": "Organisation information",
                    "themes": [
                        {
                            "id": "general_info",
                            "name": "General information",
                            "answers": [
                                {
                                    "field_id": "WWWWxy",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Your unique tracker number",
                                },
                                {
                                    "field_id": "YdtlQZ",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Organisation name",
                                },
                                {
                                    "field_id": "iBCGxY",
                                    "form_name": "organisation-information",
                                    "field_type": "YesNoField",
                                    "question": "Does your organisation use any other names",
                                },
                                {
                                    "field_id": ["PHFkCs", "QgNhXX", "XCcqae"],
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Alternative names of your organisation",
                                },
                                {
                                    "field_id": ["lajFtB", "plmwJv"],
                                    "form_name": "organisation-information",
                                    "field_type": "RadiosField",
                                    "question": "Type of organisation",
                                },
                                {
                                    "field_id": "GlPmCX",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Company registration number",
                                },
                                {
                                    "field_id": ["GvPSna", "zsbmRx"],
                                    "form_name": "organisation-information",
                                    "field_type": "RadiosField",
                                    "question": "Which regulatory body is your company registered with?",
                                },
                                {
                                    "field_id": "aHIGbK",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Charity number",
                                },
                                {
                                    "field_id": "DwfHtk",
                                    "form_name": "organisation-information",
                                    "field_type": "YesNoField",
                                    "question": "Is your organisation a trading subsidiary of a parent company?",
                                },
                                {
                                    "field_id": "MPNlZx",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Name of parent organisation",
                                },
                                {
                                    "field_id": "MyiYMw",
                                    "form_name": "organisation-information",
                                    "field_type": "DatePartsField",
                                    "question": "Date parent organisation was established",
                                },
                                {
                                    "field_id": "ZQolYb",
                                    "form_name": "organisation-information",
                                    "field_type": "UkAddressField",
                                    "question": "Organisation address",
                                },
                                {
                                    "field_id": "zsoLdf",
                                    "form_name": "organisation-information",
                                    "field_type": "YesNoField",
                                    "question": "Is your correspondence address different to the organisation address?",
                                },
                                {
                                    "field_id": "VhkCbM",
                                    "form_name": "organisation-information",
                                    "field_type": "UkAddressField",
                                    "question": "Correspondence address",
                                },
                                {
                                    "field_id": ["FhbaEy", "FcdKlB", "BzxgDA"],
                                    "form_name": "organisation-information",
                                    "field_type": "WebsiteField",
                                    "question": "Website and social media",
                                },
                            ],
                        },
                        {
                            "id": "activities",
                            "name": "Activities",
                            "answers": [
                                {
                                    "field_id": "emVGxS",
                                    "form_name": "organisation-information",
                                    "field_type": "MultilineTextField",
                                    "question": "What is your organisation's main purpose?"
                                },
                                {
                                    "field_id": ["btTtIb", "SkocDi", "CNeeiC"],
                                    "form_name": "organisation-information",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us about your organisation's main activities",
                                },
                            ],
                        },
                        {
                            "id": "partnerships",
                            "name": "Partnerships",
                            "answers": [
                                {
                                    "field_id": "hnLurH",
                                    "form_name": "organisation-information",
                                    "field_type": "YesNoField",
                                    "question": "Is your application a joint bid in partnership with other organisations?"
                                },
                                {
                                    "field_id": "APSjeB",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Partner organisation name"
                                },
                                {
                                    "field_id": "biTJjF",
                                    "form_name": "organisation-information",
                                    "field_type": "UkAddressField",
                                    "question": "Partner organisation address"
                                },
                                {
                                    "field_id": "IkmvEt",
                                    "form_name": "organisation-information",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us about your partnership and how you plan to work together"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": "applicant_info",
                    "name": "Applicant information",
                    "themes": [
                        {
                            "id": "contact_information",
                            "name": "Contact information",
                            "answers": [
                                {
                                    "field_id": "ZBjDTn",
                                    "form_name": "applicant-information",
                                    "field_type": "TextField",
                                    "question": "Name of lead contact"
                                },
                                {
                                    "field_id": "LZBrEj",
                                    "form_name": "applicant-information",
                                    "field_type": "EmailAddressField",
                                    "question": "Lead contact email address"
                                },
                                {
                                    "field_id": "lRfhGB",
                                    "form_name": "applicant-information",
                                    "field_type": "TelephoneNumberField",
                                    "question": "Lead contact telephone number"
                                }
                            ]
                        },
                        {
                            "id": "partnerships",
                            "name": "Partnerships",
                            "answers": [
                                {
                                    "field_id": "hnLurH",
                                    "form_name": "organisation-information",
                                    "field_type": "YesNoField",
                                    "question": "Is your application a joint bid in partnership with other organisations?"
                                },
                                {
                                    "field_id": "APSjeB",
                                    "form_name": "organisation-information",
                                    "field_type": "TextField",
                                    "question": "Partner organisation name"
                                },
                                {
                                    "field_id": "biTJjF",
                                    "form_name": "organisation-information",
                                    "field_type": "UkAddressField",
                                    "question": "Partner organisation address",
                                },
                                {
                                    "field_id": "IkmvEt",
                                    "form_name": "organisation-information",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us about your partnership and how you plan to work together"
                                },
                            ],
                        },
                    ],
                },
            ],
        }
    ],
    "scored_assessment_criteria": [
        {
            "id": "strategic_case",
            "name": "Strategic case",
            "weighting": 0.30,
            "sub_criteria": [
                {
                    "id": "benefits",
                    "name": "Benefits",
                    "themes": [
                        {
                            "id": "community_use",
                            "name": "Community use",
                            "answers": [
                                {
                                    "field_id": "kxgWTy",
                                    "form_name": "community-use",
                                    "field_type": "MultilineTextField",
                                    "question": "Who in the community uses the asset, or has used it in the past, and who benefits from it?",
                                },
                                {
                                    "field_id": "wudRxx",
                                    "form_name": "project-information",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                                },
                            ],
                        },
                        {
                            "id": "risk_loss_mpact",
                            "name": "Risk and impact of loss",
                            "answers": [
                                {
                                    "field_id": "TlGjXb",
                                    "form_name": "project-information",
                                    "field_type": "MultilineTextField",
                                    "question": "Explain why the asset is at risk of being lost to the community, or why it has already been lost",
                                },
                                {
                                    "field_id": "UDTxqC",
                                    "form_name": "asset-information",
                                    "field_type": "CheckboxesField",
                                    "question": "Why is the asset at risk of closure?",
                                },
                                {
                                    "field_id": "GNhrIs",
                                    "form_name": "community-use",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us how losing the asset would affect, or has already affected, people in the community",
                                },
                                {
                                    "field_id": "qsZLjZ",
                                    "form_name": "community-use",
                                    "field_type": "MultilineTextField",
                                    "question": "Why will the asset be lost without community intervention?",
                                },
                            ],
                        },
                    ],
                },
                {
                    "id": "engagement",
                    "name": "Engagement",
                    "themes": [
                        {
                            "id": "engaging-the-community",
                            "name": "Engaging the community",
                            "answers": [
                                {
                                    "field_id": "HJBgvw",
                                    "form_name": "community-engagement",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us how you have engaged with the community about your intention to take ownership of the asset, and explain how this has shaped your project plans",
                                },
                                {
                                    "field_id": "JCACTy",
                                    "form_name": "community-engagement",
                                    "field_type": "YesNoField",
                                    "question": "Have you done any fundraising in the community?",
                                    # Yes-No determines dpLyQh
                                },
                                {
                                    "field_id": "dpLyQh",
                                    "form_name": "community-engagement",
                                    "field_type": "MultilineTextField",
                                    "question": "[if y] Describe your fundraising activities",
                                    # Determined by Yes-No JCACTy
                                },
                            ],
                        },
                        {
                            "id": "local-support",
                            "name": "Local support",
                            "answers": [
                                {
                                    "field_id": "NZKHOp",
                                    "form_name": "community-engagement",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us how your project supports any wider local plans",
                                },
                                {
                                    "field_id": "KqoaJL",
                                    "form_name": "local-support",
                                    "field_type": "YesNoField",
                                    "question": "Are you confident there is local support for your project?",
                                    # Yes-No determines KqoaJL
                                },
                                {
                                    "field_id": "BFbzux",
                                    "form_name": "local-support",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us more about the local support for your project",
                                    # Determined by Yes-No KqoaJL
                                },
                                {
                                    "field_id": "EEBFao",
                                    "form_name": "local-support",
                                    "field_type": "FileUploadField",
                                    "question": "Upload supporting evidence (optional)",
                                },
                            ],
                        },
                    ],
                },
                {
                    "id": "environmental_sustainability",
                    "name": "Environmental Sustainability",
                    "themes": [
                        {
                            "id": "environmental-considerations",
                            "name": "Environmental considerations",
                            "answers": [
                                {
                                    "field_id": "CvVZJv",
                                    "form_name": "environmental-sustainability",
                                    "field_type": "MultilineTextField",
                                    "question": "Tell us how you have considered the environmental sustainability of your project",
                                }
                            ],
                        }
                    ],
                },
            ],
        },
        {
            "id": "management_case",
            "name": "Management case",
            "weighting": 0.30,
            "sub_criteria": [
                {
                    "id": "funding_breakdown",
                    "name": "Funding breakdown",
                    "themes": [
                        {
                            "id": "",
                            "name": "",
                            "answers": [
                                {
                                    # These 2 fields are capital and revenue funding respectively
                                    "field_id": "[JzWvhj, jLIgoi]",
                                    "form_name": "",
                                    "field_type": "numberField",
                                    "question": "Total funding request",
                                },
                                {
                                    "field_id": "NdFwgy",
                                    "form_name": "funding-required",
                                    "field_type": "MultiInputField",
                                    "question": "Capital costs",
                                },
                                {
                                    "field_id": "NdFwgy",
                                    "form_name": "funding-required",
                                    "field_type": "textField",
                                    "question": "Describe the cost",
                                },
                                {
                                    "field_id": "NdFwgy",
                                    "form_name": "funding-required",
                                    "field_type": "numberField",
                                    "question": "Amount",
                                },
                                {
                                    "field_id": "NWTKzQ",
                                    "form_name": "funding-required",
                                    "field_type": "YesNoField",
                                    "question": "Are you applying for revenue funding from the Community Ownership Fund?",
                                },
                                {
                                    "field_id": "NyudvF",
                                    "form_name": "funding-required",
                                    "field_type": "MultiInputField",
                                    "question": "Revenue costs",
                                },
                                {
                                    "field_id": "NyudvF",
                                    "form_name": "funding-required",
                                    "field_type": "textField",
                                    "question": "Describe the cost",
                                },
                                {
                                    "field_id": "NyudvF",
                                    "form_name": "funding-required",
                                    "field_type": "numberField",
                                    "question": "Amount",
                                },
                                {
                                    "field_id": "DIZZOC",
                                    "form_name": "funding-required",
                                    "field_type": "YesNoField",
                                    "question": "Have you secured any match funding yet?",
                                },
                                {
                                    "field_id": "abkrwo",
                                    "form_name": "funding-required",
                                    "field_type": "MultiInputField",
                                    "question": "Secured match funding",
                                },
                                {
                                    "field_id": "abkrwo",
                                    "form_name": "funding-required",
                                    "field_type": "textField",
                                    "question": "Source of funding",
                                },
                                {
                                    "field_id": "abkrwo",
                                    "form_name": "funding-required",
                                    "field_type": "numberField",
                                    "question": "Amount",
                                },
                                {
                                    "field_id": "RvbwSX",
                                    "form_name": "funding-required",
                                    "field_type": "YesNoField",
                                    "question": "Do you have any match funding identified but not yet secured?",
                                },
                                {
                                    "field_id": "AOLYnV",
                                    "form_name": "funding-required",
                                    "field_type": "MultiInputField",
                                    "question": "Unsecured match funding",
                                },
                                {
                                    "field_id": "AOLYnV",
                                    "form_name": "funding-required",
                                    "field_type": "textField",
                                    "question": "Source of funding",
                                },
                                {
                                    "field_id": "AOLYnV",
                                    "form_name": "funding-required",
                                    "field_type": "numberField",
                                    "question": "Amount",
                                },
                                {
                                    "field_id": "fnIdkJ",
                                    "form_name": "funding-required",
                                    "field_type": "numberField",
                                    "question": "Asset value",
                                },
                                {
                                    "field_id": "oaIntA",
                                    "form_name": "funding-required",
                                    "field_type": "YesNoField",
                                    "question": "If successful, will you use your funding in the next 12 months? (Y/N)",
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "",
                    "name": "",
                    "themes": [
                        {
                            "id": "",
                            "name": "",
                            "answers": [
                                {
                                    "field_id": "acbdef",
                                    "form_name": "",
                                    "field_type": "textarea",
                                    "question": "",
                                },
                            ],
                        }
                    ],
                },
            ],
        },
    ],
}

# Template Sub Criteria

#                 {
#                     "id": "environmental_sustainability",
#                     "name": "Environmental Sustainability",
#                     "themes": [
#                         {
#                             "id": "",
#                             "name": "",
#                             "answers": [
#                                 {
#                                     "field_id": "acbdef",
#                                     "form_name": "",
#                                     "field_type": "textarea",
#                                     "question": "",
#                                 },
#                             ],
#                         }
#                     ],
#                 }
