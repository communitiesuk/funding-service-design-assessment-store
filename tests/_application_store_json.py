# flake8: noqa
from string import Template

application_store_json_template = Template(
    """
    {
    "account_id": "cbf981cf-5238-4d3e-84e9-b9c183789a91",
    "date_submitted": "2022-10-27T08:32:13.383999",
    "forms": [
        {
            "name": "feasibility",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Tell us about the feasibility studies you have carried out for your project",
                            "key": "ieRCkI",
                            "title": "Tell us about the feasibility studies you have carried out for your project",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "aAeszH",
                            "title": "Do you need to do any further feasibility work?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "risk",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "sample1.doc",
                            "key": "ozgwXq",
                            "title": "Risks to your project (document upload)",
                            "type": "file"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-use",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": [
                                "support-local-community"
                            ],
                            "key": "CDwTrG",
                            "title": "What policy aims will your project deliver against?",
                            "type": "list"
                        },
                        {
                            "answer": "Test",
                            "key": "kxgWTy",
                            "title": "Who in the community uses the asset, or has used it in the past, and who benefits from it?",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "GNhrIs",
                            "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "qsZLjZ",
                            "title": "Why will the asset be lost without community intervention?",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "environmental-sustainability",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "CvVZJv",
                            "title": "Tell us how you have considered the environmental sustainability of your project",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "local-support",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "KqoaJL",
                            "title": "Are you confident there is local support for your project?",
                            "type": "list"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-qualification",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "HvxXPI",
                            "title": "Does your project meet the definition of a subsidy?",
                            "type": "list"
                        }
                    ],
                    "question": "Subsidy control and state aid",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "skills-and-resources",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "CBIWnt",
                            "title": "Do you have experience of managing a community asset?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "vKnMPG",
                            "title": "Do you have any plans to recruit people to help you manage the asset?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "upload-business-plan",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "sample1.doc",
                            "key": "rFXeZo",
                            "title": "Upload business plan",
                            "type": "file"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "gScdbf",
                            "title": "Have you been given funding through the Community Ownership Fund before?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "$project_name",
                            "key": "KAgrBz",
                            "title": "Project name",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "wudRxx",
                            "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "TlGjXb",
                            "title": "Explain why the asset is at risk of being lost to the community, or why it has already been lost",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "GCjCse",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode",
                            "key": "yEmHpp",
                            "title": "Address of the community asset",
                            "type": "text"
                        },
                        {
                            "answer": "Constituency",
                            "key": "iTeLGU",
                            "title": "In which constituency is your asset?",
                            "type": "text"
                        },
                        {
                            "answer": "Local Council",
                            "key": "MGRlEi",
                            "title": "In which local council area is your asset?",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "organisation-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "ANON-###-###-###",
                            "key": "WWWWxy",
                            "title": "Your unique tracker number",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "YdtlQZ",
                            "title": "Organisation name",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "iBCGxY",
                            "title": "Does your organisation use any other names?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "emVGxS",
                            "title": "What is your organisation's main purpose?",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "btTtIb",
                            "title": "Tell us about your organisation's main activities",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "SkocDi",
                            "title": "Tell us about your organisation's main activities - Activity 2 ",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "CNeeiC",
                            "title": "Tell us about your organisation's main activities - Activity 3 ",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "BBlCko",
                            "title": "Have you delivered projects like this before?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "CIO",
                            "key": "lajFtB",
                            "title": "Type of organisation",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "aHIGbK",
                            "title": "Charity number ",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "DwfHtk",
                            "title": "Is your organisation a trading subsidiary of a parent company?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode",
                            "key": "ZQolYb",
                            "title": "Organisation address",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "zsoLdf",
                            "title": "Is your correspondence address different to the organisation address?",
                            "type": "list"
                        },
                        {
                            "answer": "https://twitter.com/luhc",
                            "key": "FhbaEy",
                            "title": "Website and social media ",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "FcdKlB",
                            "title": "Website and social media - Link or username 2",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "BzxgDA",
                            "title": "Website and social media - Link or username 3",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "hnLurH",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "applicant-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test Name",
                            "key": "ZBjDTn",
                            "title": "Name of lead contact",
                            "type": "text"
                        },
                        {
                            "answer": "testemailfundingservice@testemailfundingservice.com",
                            "key": "LZBrEj",
                            "title": "Lead contact email address",
                            "type": "text"
                        },
                        {
                            "answer": "0000000000",
                            "key": "lRfhGB",
                            "title": "Lead contact telephone number",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "asset-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "$asset_type",
                            "key": "yaQoxU",
                            "title": "Asset type",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "buy-the-asset",
                            "key": "VWkLlk",
                            "title": "What do you intend to do with the asset?",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "IRfSZp",
                            "title": "Do you know who currently owns your asset?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Current Owner",
                            "key": "FtDJfK",
                            "title": "Describe the current ownership status",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "gkulUE",
                            "title": "Have you already completed the purchase or lease?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "nvMmGE",
                            "title": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            "type": "text"
                        },
                        {
                            "answer": "2022-12-01",
                            "key": "ghzLRv",
                            "title": "Expected date of sale or lease",
                            "type": "date"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "Wyesgy",
                            "title": "Is your asset currently publicly owned?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "hvzzWB",
                            "title": "Is this a registered Asset of Community Value (ACV)?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "VwxiGn",
                            "title": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "for-sale-or-listed-for-disposal"
                            ],
                            "key": "UDTxqC",
                            "title": "Why is the asset at risk of closure?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-engagement",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            "key": "HJBgvw",
                            "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset, and explain how this has shaped your project plans",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "JCACTy",
                            "title": "Have you done any fundraising in the community?",
                            "type": "list"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Tell us how your project supports any wider local plans",
                            "key": "NZKHOp",
                            "title": "Tell us how your project supports any wider local plans",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "funding-required",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "$capital_funding",
                            "key": "JzWvhj",
                            "title": "Capital funding",
                            "type": "text"
                        },
                        {
                            "answer": "$revenue_funding",
                            "key": "jLIgoi",
                            "title": "Revenue funding (optional)",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Capital Funding : £2300"
                            ],
                            "key": "multiInputField",
                            "title": "Capital costs",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "NWTKzQ",
                            "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                            "type": "list"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "DIZZOC",
                            "title": "Have you secured any match funding yet?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "RvbwSX",
                            "title": "Do you have any match funding identified but not yet secured?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "2300",
                            "key": "fnIdkJ",
                            "title": "Asset value",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-benefits",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": [
                                "community-pride"
                            ],
                            "key": "QjJtbs",
                            "title": "What community benefits do you expect to deliver with this project? ",
                            "type": "list"
                        },
                        {
                            "answer": "Test",
                            "key": "gDTsgG",
                            "title": "Tell us about these benefits in detail, and explain how you'll measure the benefits it'll bring for the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "kYjJFy",
                            "title": "Explain how you plan to sustain, and potentially expand, these benefits over time",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "UbjYqE",
                            "title": "Tell us how you'll make sure the whole community benefits from the asset",
                            "type": "text"
                        }
                    ],
                    "question": "Potential to deliver community benefits",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "inclusiveness-and-integration",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "SrtVAs",
                            "title": "Describe the planned activities or services that will take place at the asset",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "YbfbSC",
                            "title": "Describe anything that might prevent people from using the asset or participating in its running",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "KuhSWw",
                            "title": "Tell us how you'll make your project accessible and inclusive to everyone in the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "bkJsiO",
                            "title": "Describe how the project will bring people together from all over the community",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-costs",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "WDDkVB",
                            "title": "Summarise your cash flow for the running of the asset",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "oaIntA",
                            "title": "If successful, will you use your funding in the next 12 months?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Income Test : £2300"
                            ],
                            "key": "multiInputField",
                            "title": "Sources of income",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Running Cost Test : £2300"
                            ],
                            "key": "multiInputField-2",
                            "title": "Running costs",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-representation",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "JnvsPq",
                            "title": "List the members of your board",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "yMCivI",
                            "title": "Tell us about your governance and membership structures",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "NUZOvS",
                            "title": "Explain how you'll consider the views of the community in the running of the asset",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "value-to-the-community",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "oOPUXI",
                            "title": "Tell us about your local community as a whole",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "NKOmNL",
                            "title": "Describe any specific challenges your community faces, and how the asset will address these",
                            "type": "text"
                        }
                    ],
                    "question": "Added value to the community",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "declarations",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": true,
                            "key": "LlvhYl",
                            "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "wJrJWY",
                            "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            "type": "list"
                        },
                        {
                            "answer": true,
                            "key": "COiwQr",
                            "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "bRPzWU",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "type": "list"
                        }
                    ],
                    "question": "Declarations",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        }
    ],
    "fund_id": "$fund_id",
    "id": "$app_id" ,
    "last_edited": "2022-10-27T08:32:11.843201",
    "project_name": "$project_name" ,
    "reference": "$short_ref" ,
    "round_id": "$round_id",
    "round_name": "Round 2 Window 2",
    "started_at": "2022-10-27T08:28:55.699864",
    "status": "SUBMITTED",
    "location_json_blob": {
        "error": $location_error,
        "county": "$location_county",
        "region": "$location_region",
        "country": "$location_country",
        "postcode": "$location_postcode",
        "constituency": "$location_constituency"
    }

}
"""
)

cofr3w1_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "status": "SUBMITTED",
    "fund_id": "$fund_id",
    "language": "en",
    "round_id": "$round_id",
    "reference": "$short_ref",
    "account_id": "53433826-95b3-42b1-b56f-aee3405a1b9f",
    "round_name": "Round 3 Window 1",
    "started_at": "2023-06-05T10:52:24.629455",
    "last_edited": "2023-06-06T13:38:48.747499",
    "project_name": "$project_name",
    "date_submitted": "2023-06-06T13:38:51.467199",
    "forms": [
        {
            "name": "declarations-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "vSQKwD",
                            "type": "list",
                            "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            "answer": true
                        },
                        {
                            "key": "CQoLFp",
                            "type": "list",
                            "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            "answer": true
                        },
                        {
                            "key": "jdPkiX",
                            "type": "list",
                            "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            "answer": true
                        },
                        {
                            "key": "qWuSCy",
                            "type": "list",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "answer": true
                        },
                        {
                            "key": "tjZlml",
                            "type": "list",
                            "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LkvizC",
                    "question": "Agree to the final confirmations"
                }
            ]
        },
        {
            "name": "funding-required-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ABROnB",
                            "type": "text",
                            "title": "Capital funding",
                            "answer": "$capital_funding"
                        },
                        {
                            "key": "cLDRvN",
                            "type": "text",
                            "title": "Revenue funding (optional)",
                            "answer": "$revenue_funding"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Total funding request from the Community Ownership Fund"
                },
                {
                    "fields": [
                        {
                            "key": "qQLyXL",
                            "type": "multiInput",
                            "title": "Capital costs",
                            "answer": [
                                {
                                    "GLQlOh": "Capital Funding",
                                    "JtwkMy": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Capital costs for your project"
                },
                {
                    "fields": [
                        {
                            "key": "DOvZvB",
                            "type": "list",
                            "title": "Have you secured any match funding yet?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "If you've secured match funding"
                },
                {
                    "fields": [
                        {
                            "key": "DmgsiG",
                            "type": "list",
                            "title": "Do you have any match funding identified but not yet secured?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "If you’ve identified further match funding"
                },
                {
                    "fields": [
                        {
                            "key": "matkNH",
                            "type": "list",
                            "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Revenue funding"
                }
            ]
        },
        {
            "name": "community-representation-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ReomFo",
                            "type": "freeText",
                            "title": "List the members of your board",
                            "answer": "<p>Test Community Representation Form</p>"
                        },
                        {
                            "key": "fjVmOt",
                            "type": "freeText",
                            "title": "Tell us about your governance and membership structures",
                            "answer": "<p>Test Community Representation Form</p>"
                        },
                        {
                            "key": "GETNxN",
                            "type": "freeText",
                            "title": "Explain how you'll consider the views of the community in the running of the asset",
                            "answer": "<p>Test Community Representation Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "KbnmOO",
                    "question": "How you’ll run the asset"
                }
            ]
        },
        {
            "name": "operational-costs-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qXNkfr",
                            "type": "freeText",
                            "title": "Describe your cash flow for the running of the asset",
                            "answer": "<p>Summarise your cash flow for the running of the asset</p>"
                        },
                        {
                            "key": "qQSVEn",
                            "type": "list",
                            "title": "If successful, will you use your funding in the next 12 months?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Cashflow to run the asset"
                },
                {
                    "fields": [
                        {
                            "key": "MSNJQD",
                            "type": "multiInput",
                            "title": "Sources of income",
                            "answer": [
                                {
                                    "AJEWXD": "Income Test 2",
                                    "cHFrIp": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Income to run the asset"
                },
                {
                    "fields": [
                        {
                            "key": "NPgwcH",
                            "type": "multiInput",
                            "title": "Running costs",
                            "answer": [
                                {
                                    "IIdfRj": "Running Cost Test",
                                    "wlGQua": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Running costs of the asset"
                }
            ]
        },
        {
            "name": "skills-and-resources-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "XXGyzn",
                            "type": "freeText",
                            "title": "Describe any relevant experience you have delivering similar projects or running an asset",
                            "answer": "<p>Describe any relevant experience you have delivering similar projects or running an asset</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eLpYFr",
                    "question": "Your experience running similar assets"
                },
                {
                    "fields": [
                        {
                            "key": "Uaeyae",
                            "type": "list",
                            "title": "Do you have plans to recruit people to help you run the asset?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eLpYFr",
                    "question": "Recruitment plans"
                }
            ]
        },
        {
            "name": "inclusiveness-and-integration-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "mgIesb",
                            "type": "freeText",
                            "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
                            "answer": "<p>Test Inclusiveness and Integration Form</p>"
                        },
                        {
                            "key": "lQEkep",
                            "type": "freeText",
                            "title": "Describe anything that might prevent people from using the asset or participating in its running",
                            "answer": "<p>Test Inclusiveness and Integration Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eCZBSV",
                    "question": "How you’ll make the asset inclusive"
                }
            ]
        },
        {
            "name": "applicant-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "SnLGJE",
                            "type": "text",
                            "title": "Name of lead contact",
                            "answer": "Joe Bloggs"
                        },
                        {
                            "key": "qRDTUc",
                            "type": "text",
                            "title": "Lead contact job title",
                            "answer": "Mr"
                        },
                        {
                            "key": "NlHSBg",
                            "type": "text",
                            "title": "Lead contact email address",
                            "answer": "testemailfundingservice@testemailfundingservice.com"
                        },
                        {
                            "key": "FhBkJQ",
                            "type": "text",
                            "title": "Lead contact telephone number",
                            "answer": "0000000000"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ZuHuGk",
                    "question": "Lead contact details"
                }
            ]
        },
        {
            "name": "environmental-sustainability-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "dypuJs",
                            "type": "freeText",
                            "title": "Tell us how you have considered the environmental sustainability of your project",
                            "answer": "<p>Test Environmental Sustainability Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ljcxPd",
                    "question": "How you've considered the environment"
                }
            ]
        },
        {
            "name": "feasibility-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "iSbwDM",
                            "type": "freeText",
                            "title": "Tell us about the feasibility studies you have carried out for your project",
                            "answer": "<p>Tell us about the feasibility studies you have carried out for your project</p>"
                        },
                        {
                            "key": "jFPlEJ",
                            "type": "list",
                            "title": "Do you need to do any further feasibility work?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bBGnkL",
                    "question": "Feasiblity studies you've carried out"
                }
            ]
        },
        {
            "name": "local-support-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "tDVPnl",
                            "type": "freeText",
                            "title": "Tell us about the local support for your project",
                            "answer": "<p>Tell us about the local support for your project</p>"
                        },
                        {
                            "key": "bDWjTN",
                            "type": "text",
                            "title": "Upload supporting evidence",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "apkBSm",
                    "question": "Your support for the project"
                }
            ]
        },
        {
            "name": "project-qualifications-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ZEKMQd",
                            "type": "list",
                            "title": "Does your project meet the definition of a subsidy?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "WsFJts",
                    "question": "If your project meets the definition"
                }
            ]
        },
        {
            "name": "risk-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "EODncR",
                            "type": "text",
                            "title": "Risks to your project (document upload)",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "HKdODf",
                    "question": "Your project risk register"
                }
            ]
        },
        {
            "name": "upload-business-plan-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ndpQJk",
                            "type": "text",
                            "title": "Upload business plan",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xtwqlH",
                    "question": "Your business plan"
                }
            ]
        },
        {
            "name": "project-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pWwCRM",
                            "type": "list",
                            "title": "Have you applied to the Community Ownership Fund before?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Previous Community Ownership Fund applications"
                },
                {
                    "fields": [
                        {
                            "key": "apGjFS",
                            "type": "text",
                            "title": "Project name",
                            "answer": "$project_name"
                        },
                        {
                            "key": "bEWpAj",
                            "type": "freeText",
                            "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            "answer": "<p>Test Project Information Form</p>"
                        },
                        {
                            "key": "uypCNM",
                            "type": "freeText",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "answer": "<p>Test Project Information Form</p>"
                        },
                        {
                            "key": "AgeRbd",
                            "type": "freeText",
                            "title": "Tell us about the planned activities and/or services that will take place in the asset",
                            "answer": "<p>Test Project Information Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Project name and summary"
                },
                {
                    "fields": [
                        {
                            "key": "EfdliG",
                            "type": "text",
                            "title": "Address of the community asset",
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode"
                        },
                        {
                            "key": "fIEUcb",
                            "type": "text",
                            "title": " In which constituency is your asset?",
                            "answer": "Constituency"
                        },
                        {
                            "key": "SWfcTo",
                            "type": "text",
                            "title": "In which local council area is your asset?",
                            "answer": "Local Council"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Address of the asset"
                }
            ]
        },
        {
            "name": "community-benefits-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pqYxJO",
                            "type": "list",
                            "title": "What community benefits do you expect to deliver with this project?",
                            "answer": [
                                "community-pride"
                            ]
                        },
                        {
                            "key": "lgfiGB",
                            "type": "freeText",
                            "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                            "answer": "<p>Test Community Benefits Form</p>"
                        },
                        {
                            "key": "zKKouR",
                            "type": "freeText",
                            "title": "Explain how you plan to deliver and sustain these benefits over time",
                            "answer": "<p>Test Community Benefits Form</p>"
                        },
                        {
                            "key": "ZyIQGI",
                            "type": "freeText",
                            "title": "Tell us how you'll make sure the whole community benefits from the asset",
                            "answer": "<p>Test Community Benefits Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "PTOBPV",
                    "question": "Benefits you'll deliver"
                }
            ]
        },
        {
            "name": "organisation-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "WWWWxy",
                            "type": "text",
                            "title": "Your unique tracker number",
                            "answer": "ANON-###-###-###"
                        },
                        {
                            "key": "YdtlQZ",
                            "type": "text",
                            "title": "Organisation name",
                            "answer": "Test Change Answers"
                        },
                        {
                            "key": "iBCGxY",
                            "type": "list",
                            "title": "Does your organisation use any other names?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Organisation names"
                },
                {
                    "fields": [
                        {
                            "key": "emVGxS",
                            "type": "freeText",
                            "title": "What is your organisation's main purpose?",
                            "answer": "<p>Test Org Form</p>"
                        },
                        {
                            "key": "btTtIb",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities",
                            "answer": "<p>Test Org Form</p>"
                        },
                        {
                            "key": "SkocDi",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities - Activity 2 ",
                            "answer": null
                        },
                        {
                            "key": "CNeeiC",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities - Activity 3 ",
                            "answer": null
                        },
                        {
                            "key": "BBlCko",
                            "type": "list",
                            "title": "Have you delivered projects like this before?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Purpose and activities"
                },
                {
                    "fields": [
                        {
                            "key": "lajFtB",
                            "type": "list",
                            "title": "Type of organisation",
                            "answer": "CIO"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "How your organisation is classified"
                },
                {
                    "fields": [
                        {
                            "key": "aHIGbK",
                            "type": "text",
                            "title": "Charity number ",
                            "answer": "234388322"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Charity registration details"
                },
                {
                    "fields": [
                        {
                            "key": "DwfHtk",
                            "type": "list",
                            "title": "Is your organisation a trading subsidiary of a parent company?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Trading subsidiaries"
                },
                {
                    "fields": [
                        {
                            "key": "ZQolYb",
                            "type": "text",
                            "title": "Organisation address",
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode"
                        },
                        {
                            "key": "zsoLdf",
                            "type": "list",
                            "title": "Is your correspondence address different to the organisation address?",
                            "answer": false
                        },
                        {
                            "key": "FhbaEy",
                            "type": "text",
                            "title": "Website and social media",
                            "answer": "https://twitter.com/luhc"
                        },
                        {
                            "key": "FcdKlB",
                            "type": "text",
                            "title": "Website and social media - Link or username 2",
                            "answer": null
                        },
                        {
                            "key": "BzxgDA",
                            "type": "text",
                            "title": "Website and social media - Link or username 3",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Organisation address"
                },
                {
                    "fields": [
                        {
                            "key": "hnLurH",
                            "type": "list",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Joint applications"
                }
            ]
        },
        {
            "name": "community-engagement-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "azCutK",
                            "type": "freeText",
                            "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "How you've engaged with the community"
                },
                {
                    "fields": [
                        {
                            "key": "jAhuWN",
                            "type": "freeText",
                            "title": "Describe your fundraising activities",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "Your fundraising activities"
                },
                {
                    "fields": [
                        {
                            "key": "HYsezC",
                            "type": "freeText",
                            "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
                            "answer": "<p>Test Community Engagement Form</p>"
                        },
                        {
                            "key": "GGBgBY",
                            "type": "freeText",
                            "title": "Tell us how your project supports any wider local plans",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "Partnerships and local plans"
                }
            ]
        },
        {
            "name": "community-use-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "zTcrYo",
                            "type": "freeText",
                            "title": "Who in the community currently uses the asset, or has used it in the past?",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "whlRYS",
                            "type": "freeText",
                            "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "NGSXHE",
                            "type": "freeText",
                            "title": "Why will the asset be lost without community intervention?",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "Ieudgn",
                            "type": "freeText",
                            "title": "Explain how the community will be better served with the asset under community ownership",
                            "answer": "<p>Test Community Use Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "GMkooI",
                    "question": "Who uses the asset"
                }
            ]
        },
        {
            "name": "asset-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "oXGwlA",
                            "type": "list",
                            "title": "Asset type",
                            "answer": "$asset_type"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "How the asset is used in the community"
                },
                {
                    "fields": [
                        {
                            "key": "LaxeJN",
                            "type": "list",
                            "title": "How do you intend to take community ownership of the asset?",
                            "answer": "buy-the-asset"
                        },
                        {
                            "key": "tTOrEp",
                            "type": "text",
                            "title": "Upload asset valuation or lease agreement",
                            "answer": "sample.txt"
                        },
                        {
                            "key": "hdmYjg",
                            "type": "list",
                            "title": "Do you know who currently owns your asset?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "The asset in community ownership"
                },
                {
                    "fields": [
                        {
                            "key": "CSsbsG",
                            "type": "text",
                            "title": "Describe the current ownership status",
                            "answer": "Current Owner"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Current ownership status"
                },
                {
                    "fields": [
                        {
                            "key": "uPvsqM",
                            "type": "list",
                            "title": "Have you already completed the purchase or lease?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "If you've already taken ownership"
                },
                {
                    "fields": [
                        {
                            "key": "XPcbJx",
                            "type": "freeText",
                            "title": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            "answer": "<p>Test Asset Information Form</p>"
                        },
                        {
                            "key": "jGjScT",
                            "type": "date",
                            "title": "Expected date of sale or lease",
                            "answer": "2022-12-01"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Expected terms of your ownership or lease"
                },
                {
                    "fields": [
                        {
                            "key": "VGXXyq",
                            "type": "list",
                            "title": "Is your asset currently publicly owned?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Public ownership"
                },
                {
                    "fields": [
                        {
                            "key": "wjBFTf",
                            "type": "list",
                            "title": "Is this a registered Asset of Community Value (ACV)?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Assets of community value"
                },
                {
                    "fields": [
                        {
                            "key": "HyWPwE",
                            "type": "list",
                            "title": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Assets listed for disposal"
                },
                {
                    "fields": [
                        {
                            "key": "KQlOaJ",
                            "type": "list",
                            "title": "Why is the asset at risk of closure?",
                            "answer": [
                                "for-sale-or-listed-for-disposal"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Risk of closure"
                }
            ]
        }
    ]
}
"""
)

cofr3w2_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2023-09-04T15:54:15.234643",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 3 Window 2",
    "started_at": "2023-09-04T15:48:57.567040",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2023-09-04T15:54:30.373564",
    "forms": [
      {
        "name": "community-use-cof-r3-w2",
        "questions": [
          {
            "category": "GMkooI",
            "fields": [
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "zTcrYo",
                "title": "Who in the community currently uses the asset, or has used it in the past?",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "whlRYS",
                "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "NGSXHE",
                "title": "Why will the asset be lost without community intervention?",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "Ieudgn",
                "title": "Explain how the community will be better served with the asset under community ownership",
                "type": "freeText"
              }
            ],
            "question": "Who uses the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "community-engagement-cof-r3-w2",
        "questions": [
          {
            "category": "lmdhVN",
            "fields": [
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "azCutK",
                "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                "type": "freeText"
              }
            ],
            "question": "How you've engaged with the community",
            "status": "COMPLETED"
          },
          {
            "category": "lmdhVN",
            "fields": [
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "jAhuWN",
                "title": "Describe your fundraising activities",
                "type": "freeText"
              }
            ],
            "question": "Your fundraising activities",
            "status": "COMPLETED"
          },
          {
            "category": "lmdhVN",
            "fields": [
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "HYsezC",
                "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "GGBgBY",
                "title": "Tell us how your project supports any wider local plans",
                "type": "freeText"
              }
            ],
            "question": "Partnerships and local plans",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "asset-information-cof-r3-w2",
        "questions": [
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "$asset_type",
                "key": "oXGwlA",
                "title": "Asset type",
                "type": "list"
              }
            ],
            "question": "How the asset is used in the community",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "buy-the-asset",
                "key": "LaxeJN",
                "title": "How do you intend to take community ownership of the asset?",
                "type": "list"
              }
            ],
            "question": "The asset in community ownership",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "sample.txt",
                "key": "tTOrEp",
                "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
                "type": "text"
              }
            ],
            "question": "Upload asset valuation or lease agreement",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": true,
                "key": "wAUFqr",
                "title": "Do you know who currently owns your asset?",
                "type": "list"
              }
            ],
            "question": "Who owns the asset",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "Mr. Shannon Gorczany",
                "key": "FOURVe",
                "title": "Name of current asset owner",
                "type": "text"
              }
            ],
            "question": "Who currently owns your asset",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "XPcbJx",
                "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
                "type": "freeText"
              },
              {
                "answer": "2022-12-01",
                "key": "jGjScT",
                "title": "Expected date of sale or lease",
                "type": "date"
              }
            ],
            "question": "Expected terms of your ownership or lease",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": false,
                "key": "VGXXyq",
                "title": "Is your asset currently publicly owned?",
                "type": "list"
              }
            ],
            "question": "Public ownership",
            "status": "COMPLETED"
          },
          {
            "fields": [
                {
                    "key": "wjBFTf",
                    "type": "list",
                    "title": "Is this a registered Asset of Community Value (ACV)?",
                    "answer": false
                }
            ],
            "status": "COMPLETED",
            "category": "wxYZcT",
            "question": "Assets of community value"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": [
                  "Sale",
                  "Listed for disposal",
                  "Part of a Community Asset Transfer"
                ],
                "key": "qlqyUq",
                "title": "Why is the asset at risk of closure?",
                "type": "list"
              }
            ],
            "question": "Risk of closure",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "2022-12-01",
                "key": "QPIPjx",
                "title": "When was the asset listed?",
                "type": "date"
              },
              {
                "answer": "https://twitter.com/luhc",
                "key": "OJWGGr",
                "title": "Provide a link to the listing",
                "type": "text"
              }
            ],
            "question": "Asset listing details",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "WKIGQE",
                "title": "Describe the current status of the Community Asset Transfer",
                "type": "freeText"
              }
            ],
            "question": "Community asset transfer",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": false,
                "key": "iqnlTk",
                "title": "Is this a registered Asset of Community Value (ACV)?",
                "type": "list"
              }
            ],
            "question": "Assets of community value",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "funding-required-cof-r3-w2",
        "questions": [
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": "$capital_funding",
                "key": "ABROnB",
                "title": "Capital funding request",
                "type": "text"
              },
              {
                "answer": true,
                "key": "hJkmBS",
                "title": "If successful, will you use your funding in the next 12 months?",
                "type": "list"
              }
            ],
            "question": "Capital funding request",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "GLQlOh": "Capital Funding",
                    "JtwkMy": 571
                  }
                ],
                "key": "qQLyXL",
                "title": "Capital costs",
                "type": "multiInput"
              }
            ],
            "question": "Capital costs for your project",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "DOvZvB",
                "title": "Have you secured any match funding yet?",
                "type": "list"
              }
            ],
            "question": "If you've secured match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "JKqLWU": "Secured Match Funding",
                    "LVJcDC": 571
                  }
                ],
                "key": "MopCmv",
                "title": "Secured match funding",
                "type": "multiInput"
              }
            ],
            "question": "Secured match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "HgpNUe",
                "title": "Have you already spent the match funding you have secured?",
                "type": "list"
              }
            ],
            "question": "Have you already spent the match funding you have secured?",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "DmgsiG",
                "title": "Have you identified, but not yet secured, any additional match funding?",
                "type": "list"
              }
            ],
            "question": "If you’ve identified further match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "THOdae": 571,
                    "iMJdfs": "Unsecured Match Funding"
                  }
                ],
                "key": "vEOdBS",
                "title": "Unsecured match funding",
                "type": "multiInput"
              }
            ],
            "question": "Unsecured match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "matkNH",
                "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                "type": "list"
              }
            ],
            "question": "Revenue funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "UyaAHw": $revenue_funding,
                    "hGsUaZ": "Revenue Costs 1"
                  },
                  {
                    "UyaAHw": $revenue_funding,
                    "hGsUaZ": "Revenue Costs 2"
                  }
                ],
                "key": "tSKhQQ",
                "title": "Revenue costs (optional)",
                "type": "multiInput"
              }
            ],
            "question": "Revenue costs (optional)",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": "<p>Tell us how the revenue funding you've requested will help run the asset</p>",
                "key": "XPDbsl",
                "title": "Tell us how the revenue funding you've requested will help run the asset",
                "type": "freeText"
              }
            ],
            "question": "How you'll use revenue funding",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "skills-and-resources-cof-r3-w2",
        "questions": [
          {
            "category": "eLpYFr",
            "fields": [
              {
                "answer": "<p>Describe any relevant experience you have delivering similar projects or running an asset</p>",
                "key": "XXGyzn",
                "title": "Describe any relevant experience you have delivering similar projects or running an asset",
                "type": "freeText"
              }
            ],
            "question": "Your experience running similar assets",
            "status": "COMPLETED"
          },
          {
            "category": "eLpYFr",
            "fields": [
              {
                "answer": false,
                "key": "Uaeyae",
                "title": "Do you have plans to recruit people to help you run the asset?",
                "type": "list"
              }
            ],
            "question": "Recruitment plans",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "organisation-information-cof-r3-w2",
        "questions": [
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "ANON-###-###-###",
                "key": "WWWWxy",
                "title": "Your unique tracker number",
                "type": "text"
              },
              {
                "answer": "Collier, Heaney and Bosco",
                "key": "YdtlQZ",
                "title": "Organisation name",
                "type": "text"
              },
              {
                "answer": false,
                "key": "iBCGxY",
                "title": "Does your organisation use any other names?",
                "type": "list"
              }
            ],
            "question": "Organisation names",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "<p>Test Org Form</p>",
                "key": "emVGxS",
                "title": "What is your organisation's main purpose?",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Org Form</p>",
                "key": "btTtIb",
                "title": "Tell us about your organisation's main activities",
                "type": "freeText"
              },
              {
                "answer": null,
                "key": "SkocDi",
                "title": "Tell us about your organisation's main activities - Activity 2 ",
                "type": "freeText"
              },
              {
                "answer": null,
                "key": "CNeeiC",
                "title": "Tell us about your organisation's main activities - Activity 3 ",
                "type": "freeText"
              },
              {
                "answer": false,
                "key": "BBlCko",
                "title": "Have you delivered projects like this before?",
                "type": "list"
              }
            ],
            "question": "Purpose and activities",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "CIO",
                "key": "lajFtB",
                "title": "Type of organisation",
                "type": "list"
              }
            ],
            "question": "How your organisation is classified",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "7036286351201658",
                "key": "aHIGbK",
                "title": "Charity number ",
                "type": "text"
              }
            ],
            "question": "Charity registration details",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": false,
                "key": "DwfHtk",
                "title": "Is your organisation a trading subsidiary of a parent company?",
                "type": "list"
              }
            ],
            "question": "Trading subsidiaries",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "4 Laurine Fold, null, St. Nienow, null, $location_postcode",
                "key": "ZQolYb",
                "title": "Organisation address",
                "type": "text"
              },
              {
                "answer": false,
                "key": "zsoLdf",
                "title": "Is your correspondence address different to the organisation address?",
                "type": "list"
              },
              {
                "answer": "https://twitter.com/luhc",
                "key": "FhbaEy",
                "title": "Website and social media",
                "type": "text"
              },
              {
                "answer": null,
                "key": "FcdKlB",
                "title": "Website and social media - Link or username 2",
                "type": "text"
              },
              {
                "answer": null,
                "key": "BzxgDA",
                "title": "Website and social media - Link or username 3",
                "type": "text"
              }
            ],
            "question": "Organisation address",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": false,
                "key": "hnLurH",
                "title": "Is your application a joint bid in partnership with other organisations?",
                "type": "list"
              }
            ],
            "question": "Joint applications",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "feasibility-cof-r3-w2",
        "questions": [
          {
            "category": "bBGnkL",
            "fields": [
              {
                "answer": "<p>Tell us about the feasibility studies you have carried out for your project</p>",
                "key": "iSbwDM",
                "title": "Tell us about the feasibility studies you have carried out for your project",
                "type": "freeText"
              },
              {
                "answer": false,
                "key": "jFPlEJ",
                "title": "Do you need to do any further feasibility work?",
                "type": "list"
              }
            ],
            "question": "Feasiblity studies you've carried out",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "project-information-cof-r3-w2",
        "questions": [
          {
            "category": "qsnIGd",
            "fields": [
              {
                "answer": false,
                "key": "pWwCRM",
                "title": "Have you applied to the Community Ownership Fund before?",
                "type": "list"
              }
            ],
            "question": "Previous Community Ownership Fund applications",
            "status": "COMPLETED"
          },
          {
            "category": "qsnIGd",
            "fields": [
              {
                "answer": "$project_name",
                "key": "apGjFS",
                "title": "Project name",
                "type": "text"
              },
              {
                "answer": "<p>Test Project Information Form</p>",
                "key": "bEWpAj",
                "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Project Information Form</p>",
                "key": "uypCNM",
                "title": "Give a brief summary of your project, including what you hope to achieve",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Project Information Form</p>",
                "key": "AgeRbd",
                "title": "Tell us about the planned activities and/or services that will take place in the asset",
                "type": "freeText"
              }
            ],
            "question": "Project name and summary",
            "status": "COMPLETED"
          },
          {
            "category": "qsnIGd",
            "fields": [
              {
                "answer": "5 Haley-Powlowski End, null, Schmidt Common, null, $location_postcode",
                "key": "EfdliG",
                "title": "Address of the community asset",
                "type": "text"
              },
              {
                "answer": "Constituency",
                "key": "fIEUcb",
                "title": " In which constituency is your asset?",
                "type": "text"
              },
              {
                "answer": "Highlands and Islands",
                "key": "SWfcTo",
                "title": "In which local council area is your asset?",
                "type": "text"
              }
            ],
            "question": "Address of the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "declarations-cof-r3-w2",
        "questions": [
          {
            "category": "LkvizC",
            "fields": [
              {
                "answer": false,
                "key": "vSQKwD",
                "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                "type": "list"
              },
              {
                "answer": false,
                "key": "CQoLFp",
                "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                "type": "list"
              },
              {
                "answer": true,
                "key": "jdPkiX",
                "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                "type": "list"
              },
              {
                "answer": false,
                "key": "qWuSCy",
                "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                "type": "list"
              },
              {
                "answer": true,
                "key": "tjZlml",
                "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                "type": "list"
              }
            ],
            "question": "Agree to the final confirmations",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "applicant-information-cof-r3-w2",
        "questions": [
          {
            "category": "ZuHuGk",
            "fields": [
              {
                "answer": "Damion",
                "key": "SnLGJE",
                "title": "Name of lead contact",
                "type": "text"
              },
              {
                "answer": "National Accounts Strategist",
                "key": "qRDTUc",
                "title": "Lead contact job title",
                "type": "text"
              },
              {
                "answer": "Loraine89@yahoo.com",
                "key": "NlHSBg",
                "title": "Lead contact email address",
                "type": "text"
              },
              {
                "answer": "+44 75506381249",
                "key": "FhBkJQ",
                "title": "Lead contact telephone number",
                "type": "text"
              }
            ],
            "question": "Lead contact details",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "upload-business-plan-cof-r3-w2",
        "questions": [
          {
            "category": "xtwqlH",
            "fields": [
              {
                "answer": "sample.txt",
                "key": "ndpQJk",
                "title": "Upload business plan",
                "type": "text"
              }
            ],
            "question": "Your business plan",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "local-support-cof-r3-w2",
        "questions": [
          {
            "category": "apkBSm",
            "fields": [
              {
                "answer": "<p>Tell us about the local support for your project</p>",
                "key": "tDVPnl",
                "title": "Tell us about the local support for your project",
                "type": "freeText"
              },
              {
                "answer": null,
                "key": "bDWjTN",
                "title": "Upload supporting evidence (optional)",
                "type": "text"
              }
            ],
            "question": "Your support for the project",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "community-representation-cof-r3-w2",
        "questions": [
          {
            "category": "KbnmOO",
            "fields": [
              {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "ReomFo",
                "title": "List the members of your board",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "fjVmOt",
                "title": "Tell us about your governance and membership structures",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "GETNxN",
                "title": "Explain how you'll consider the views of the community in the running of the asset",
                "type": "freeText"
              }
            ],
            "question": "How you’ll run the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "operational-costs-cof-r3-w2",
        "questions": [
          {
            "category": "oSfXFZ",
            "fields": [
              {
                "answer": "<p>Summarise your income and operational costs for the running of the asset</p>",
                "key": "qXNkfr",
                "title": "Summarise your income and operational costs for the running of the asset",
                "type": "freeText"
              }
            ],
            "question": "Forecasted income and operational costs to run the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "inclusiveness-and-integration-cof-r3-w2",
        "questions": [
          {
            "category": "eCZBSV",
            "fields": [
              {
                "answer": "<p>Test Inclusiveness and Integration Form</p>",
                "key": "mgIesb",
                "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Inclusiveness and Integration Form</p>",
                "key": "lQEkep",
                "title": "Describe anything that might prevent people from using the asset or participating in its running",
                "type": "freeText"
              }
            ],
            "question": "How you’ll make the asset inclusive",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "environmental-sustainability-cof-r3-w2",
        "questions": [
          {
            "category": "ljcxPd",
            "fields": [
              {
                "answer": "<p>Test Environmental Sustainability Form</p>",
                "key": "dypuJs",
                "title": "Tell us how you have considered the environmental sustainability of your project",
                "type": "freeText"
              }
            ],
            "question": "How you've considered the environment",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "community-benefits-cof-r3-w2",
        "questions": [
          {
            "category": "PTOBPV",
            "fields": [
              {
                "answer": [
                  "community-pride"
                ],
                "key": "pqYxJO",
                "title": "What community benefits do you expect to deliver with this project?",
                "type": "list"
              },
              {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "lgfiGB",
                "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "zKKouR",
                "title": "Explain how you plan to deliver and sustain these benefits over time",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "ZyIQGI",
                "title": "Tell us how you'll make sure the whole community benefits from the asset",
                "type": "freeText"
              }
            ],
            "question": "Benefits you'll deliver",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "project-qualifications-cof-r3-w2",
        "questions": [
          {
            "category": "WsFJts",
            "fields": [
              {
                "answer": false,
                "key": "ZEKMQd",
                "title": "Does your project meet the definition of a subsidy?",
                "type": "list"
              }
            ],
            "question": "If your project meets the definition",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "risk-cof-r3-w2",
        "questions": [
          {
            "category": "HKdODf",
            "fields": [
              {
                "answer": "sample.txt",
                "key": "EODncR",
                "title": "Risks to your project (document upload)",
                "type": "text"
              }
            ],
            "question": "Your project risk register",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      }
    ]
  }
"""
)

nstfr2_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "status": "SUBMITTED",
    "fund_id": "$fund_id",
    "language": "en",
    "round_id": "$round_id",
    "reference": "$short_ref",
    "account_id": "dd143674-958b-4cb0-8f73-f4ddfddc4578",
    "round_name": "Round 2",
    "started_at": "2023-06-12T13:16:58.555188",
    "last_edited": "2023-06-12T13:19:34.332308",
    "project_name": "$project_name",
    "date_submitted": "2023-06-12T13:19:38.752573",
    "forms": [
        {
            "name": "proposed-services-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "lOliDH",
                            "type": "freeText",
                            "title": "Tell us how your proposal will transform your existing services",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Tell us how your proposal will transform your existing services"
                },
                {
                    "fields": [
                        {
                            "key": "dWxxdq",
                            "type": "list",
                            "title": "Do you plan to use this funding to make any changes to the existing night shelter or emergency accommodation?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Do you plan to use this funding to make any changes to the existing night shelter or emergency accommodation?"
                },
                {
                    "fields": [
                        {
                            "key": "UEndmh",
                            "type": "text",
                            "title": "How many single rooms will you provide with the funding?",
                            "answer": "123"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "How many single rooms will you provide with the funding?"
                },
                {
                    "fields": [
                        {
                            "key": "jzzBDS",
                            "type": "list",
                            "title": "Do you plan to use this funding to make any changes to the existing day provision?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Do you plan to use this funding to make any changes to the existing day provision?"
                },
                {
                    "fields": [
                        {
                            "key": "bGCkPI",
                            "type": "list",
                            "title": "Which additional day provision will your proposal provide?",
                            "answer": [
                                "other"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Which additional day provision will your proposal provide?"
                },
                {
                    "fields": [
                        {
                            "key": "brLcqY",
                            "type": "freeText",
                            "title": "Which other additional day provision will your proposal provide?",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Which other additional day provision will your proposal provide?"
                },
                {
                    "fields": [
                        {
                            "key": "bCQWFN",
                            "type": "list",
                            "title": "Will you provide any other additional services?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Will you provide any other additional services?"
                },
                {
                    "fields": [
                        {
                            "key": "kPvpzG",
                            "type": "freeText",
                            "title": "Which other services will you use the funding to provide?",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Which other services will you use the funding to provide?"
                },
                {
                    "fields": [
                        {
                            "key": "xYNpHc",
                            "type": "list",
                            "title": "Will your proposal provide additional specialist support?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Will your proposal provide additional specialist support?"
                },
                {
                    "fields": [
                        {
                            "key": "RKPpEV",
                            "type": "list",
                            "title": "Who will your proposal provide targeted specialist support to?",
                            "answer": [
                                "disabled-people",
                                "other"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Who will your proposal provide targeted specialist support to?"
                },
                {
                    "fields": [
                        {
                            "key": "HTGgzg",
                            "type": "freeText",
                            "title": "Who will your proposal provide specialist support to?",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Who will your proposal provide specialist support to?"
                }
            ]
        },
        {
            "name": "outputs-and-outcomes-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "cYEiGS",
                            "type": "text",
                            "title": "How many people will the proposal support with the funding in 2023 to 2024?",
                            "answer": "5"
                        },
                        {
                            "key": "ZZisap",
                            "type": "text",
                            "title": "How many people will the proposal support with the funding in 2024 to 2025?",
                            "answer": "10"
                        },
                        {
                            "key": "ZJCVjE",
                            "type": "text",
                            "title": "How many people with restricted eligibility will the proposal support in 2023 to 2024?",
                            "answer": "15"
                        },
                        {
                            "key": "dboegN",
                            "type": "text",
                            "title": "How many people with restricted eligibility will the proposal support in 2024 to 2025?",
                            "answer": "20"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VeHFTz",
                    "question": "Who your proposal will support"
                }
            ]
        },
        {
            "name": "declarations-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "kOTdzu",
                            "type": "list",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "answer": false
                        },
                        {
                            "key": "NBcyAe",
                            "type": "list",
                            "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            "answer": true
                        },
                        {
                            "key": "OKtDsH",
                            "type": "list",
                            "title": "Confirm you have a safeguarding, data protection and health and safety policy",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gkTvmJ",
                    "question": "Agree to the final confirmations"
                }
            ]
        },
        {
            "name": "working-in-partnership-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qMRHPz",
                            "type": "freeText",
                            "title": "Describe your important local partners and how they will support your proposal",
                            "answer": "<p>Test Working In Partnership NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "TsNdVD",
                    "question": "Describe your important local partners and how they will support your proposal"
                }
            ]
        },
        {
            "name": "match-funding-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "nxpXlE",
                            "type": "list",
                            "title": "Will you use match funding for this proposal?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qXObyw",
                    "question": "Will you use match funding for this proposal?"
                },
                {
                    "fields": [
                        {
                            "key": "uuyBff",
                            "type": "multiInput",
                            "title": "Match funding",
                            "answer": [
                                {
                                    "AfAKxk": "Test Match Funding NS Form",
                                    "CrcLtW": 1234,
                                    "ndySbC": "1 April 2023 to 31 March 2024",
                                    "pATWyM": "Capital",
                                    "sIFBGc": true
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qXObyw",
                    "question": "Match funding"
                }
            ]
        },
        {
            "name": "name-your-application-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "YVsPtE",
                            "type": "text",
                            "title": "Application name",
                            "answer": "$project_name"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "pCEnjo",
                    "question": "Name your application"
                }
            ]
        },
        {
            "name": "objectives-and-activities-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pWFwci",
                            "type": "freeText",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "answer": "<p>Test Objectives and Activities NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VCtwUB",
                    "question": "Give a brief summary of your project, including what you hope to achieve"
                },
                {
                    "fields": [
                        {
                            "key": "kRxOHF",
                            "type": "multiInput",
                            "title": "Proposal milestones",
                            "answer": [
                                {
                                    "FbWEBY": "Test Objectives and Activities NS Form",
                                    "RXrpzV": "Test Objectives and Activities NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VCtwUB",
                    "question": "Objectives and activities"
                }
            ]
        },
        {
            "name": "project-milestones-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "sXlkAm",
                            "type": "multiInput",
                            "title": "Milestones",
                            "answer": [
                                {
                                    "PrulfI": {
                                        "PrulfI__year": 2023,
                                        "PrulfI__month": 6
                                    },
                                    "fFIuPP": "Test Project Milestones NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "KdUbsr",
                    "question": "Proposal milestones"
                }
            ]
        },
        {
            "name": "risk-and-deliverability-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "xDpgOK",
                            "type": "multiInput",
                            "title": "Risk",
                            "answer": [
                                {
                                    "GVoNOE": "high",
                                    "SRHsAx": "Test Risk And Deliverability NS Form",
                                    "dmKRCF": "Test Risk And Deliverability NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JOYYbl",
                    "question": "Risks to the proposal"
                }
            ]
        },
        {
            "name": "applicant-information-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "fUMWcd",
                            "type": "text",
                            "title": "Name of lead contact",
                            "answer": "Test Applicant Information Form"
                        },
                        {
                            "key": "lZVkeg",
                            "type": "text",
                            "title": "Lead contact job title",
                            "answer": "Test Applicant Information Form"
                        },
                        {
                            "key": "CDEwxp",
                            "type": "text",
                            "title": "Lead contact email address",
                            "answer": "test@test.com"
                        },
                        {
                            "key": "DvBqCJ",
                            "type": "text",
                            "title": "Lead contact telephone number",
                            "answer": "0000000000"
                        },
                        {
                            "key": "ayzqnK",
                            "type": "list",
                            "title": "Is the lead contact the same person as the authorised signatory?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ZbxIUV",
                    "question": "Lead contact details"
                }
            ]
        },
        {
            "name": "staff-and-volunteers-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "bcJWbJ",
                            "type": "text",
                            "title": "How many staff members are currently employed in your organisation?",
                            "answer": "44"
                        },
                        {
                            "key": "pwPYdF",
                            "type": "text",
                            "title": "How many volunteers are actively involved in your organisation?",
                            "answer": "39"
                        },
                        {
                            "key": "VXKVmM",
                            "type": "text",
                            "title": "What percentage of your employed staff work part-time?",
                            "answer": "10%"
                        },
                        {
                            "key": "wOUNbF",
                            "type": "text",
                            "title": "For part-time employees, what is their average full-time equivalency (FTE)?",
                            "answer": "0.6"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ibsaRz",
                    "question": "Employed staff and volunteers at your organisation"
                }
            ]
        },
        {
            "name": "local-need-and-support-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "nMfGTS",
                            "type": "freeText",
                            "title": "Tell us why your proposal is needed in your area",
                            "answer": "<p>Test Local Need And Support NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "vzkeMY",
                    "question": "Tell us why your proposal is needed in your area"
                },
                {
                    "fields": [
                        {
                            "key": "nURkuc",
                            "type": "text",
                            "title": "What is the name of the local authority where your proposal will be based?",
                            "answer": "$local_authority"
                        },
                        {
                            "key": "lFTgWk",
                            "type": "list",
                            "title": "Do you have the local authority's support and endorsement for your proposal?",
                            "answer": false
                        },
                        {
                            "key": "mIGfuL",
                            "type": "text",
                            "title": "Upload letter of endorsement from your local authority (optional)",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "vzkeMY",
                    "question": "Local authority support"
                }
            ]
        },
        {
            "name": "joint-applications-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "jsUbAI",
                            "type": "list",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "uFLqwl",
                    "question": "Is your application a joint bid in partnership with other organisations?"
                },
                {
                    "fields": [
                        {
                            "key": "oxMLrb",
                            "type": "multiInput",
                            "title": "Your partner organisations",
                            "answer": [
                                {
                                    "EFlBMr": "Test Joint Applications NS Form",
                                    "JFEJVf": "Test Joint Applications NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "uFLqwl",
                    "question": "Partner organisation details"
                }
            ]
        },
        {
            "name": "proposal-sustainability-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "PEMJEy",
                            "type": "freeText",
                            "title": "How will this funding support the longer-term sustainability of your proposal beyond the funding period?",
                            "answer": "<p>Test Proposal Sustainability NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LZWArS",
                    "question": "How will this funding support the longer-term sustainability of your proposal beyond the funding period?"
                }
            ]
        },
        {
            "name": "funding-required-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "NxVqXd",
                            "type": "list",
                            "title": "What funding are you applying for?",
                            "answer": "$funding_type"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "What funding are you applying for?"
                },
                {
                    "fields": [
                        {
                            "key": "GRWtfV",
                            "type": "text",
                            "title": "Both revenue and capital",
                            "answer": "$revenue_funding"
                        },
                        {
                            "key": "zvPzXN",
                            "type": "text",
                            "title": "Revenue for 1 April 2024 to 31 March 2025",
                            "answer": "$revenue_funding"
                        },
                        {
                            "key": "QUCvFy",
                            "type": "text",
                            "title": "Capital for 1 April 2023 to 31 March 2024",
                            "answer": "$capital_funding"
                        },
                        {
                            "key": "pppiYl",
                            "type": "text",
                            "title": "Capital for 1 April 2024 to 31 March 2025",
                            "answer": "$capital_funding"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "How much funding are you applying for?"
                },
                {
                    "fields": [
                        {
                            "key": "mCbbyN",
                            "type": "multiInput",
                            "title": "Revenue costs",
                            "answer": [
                                {
                                    "TrTaZQ": "Test Funding Required NS Form",
                                    "dpDFgB": "Test Funding Required NS Form",
                                    "iZdZrr": 40,
                                    "leIxEX": "1 April 2023 to 31 March 2024"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "Revenue funding"
                },
                {
                    "fields": [
                        {
                            "key": "XsAoTv",
                            "type": "multiInput",
                            "title": "Capital costs",
                            "answer": [
                                {
                                    "JtBjFp": 50,
                                    "cpFthG": "Test Funding Required NS Form",
                                    "mmwzGc": "1 April 2024 to 31 March 2025",
                                    "pMffVz": null
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "Capital funding"
                }
            ]
        },
        {
            "name": "organisation-information-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "opFJRm",
                            "type": "text",
                            "title": "Organisation name",
                            "answer": "$org_name"
                        },
                        {
                            "key": "mhYQzL",
                            "type": "text",
                            "title": "Organisation address",
                            "answer": "Test Organisation Information NS Form, null, Test Organisation Information NS Form, null, $location_postcode"
                        },
                        {
                            "key": "AVShTf",
                            "type": "text",
                            "title": "Which region of England do you work in?",
                            "answer": "Test Organisation Information NS Form"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "Organisation details"
                },
                {
                    "fields": [
                        {
                            "key": "BwbIlM",
                            "type": "freeText",
                            "title": "What is your organisation's main purpose?",
                            "answer": "<p>Test Organisation Information NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "What is your organisation's main purpose?"
                },
                {
                    "fields": [
                        {
                            "key": "RxbebZ",
                            "type": "freeText",
                            "title": "What are your organisation’s charitable objects?",
                            "answer": "<p>Test Organisation Information NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "What are your organisation’s charitable objects?"
                },
                {
                    "fields": [
                        {
                            "key": "YauUjZ",
                            "type": "text",
                            "title": "Annual turnover for 1 April 2022 to 31 March 2023",
                            "answer": "444"
                        },
                        {
                            "key": "zuCRBk",
                            "type": "text",
                            "title": "Annual turnover for 1 April 2021 to 31 March 2022",
                            "answer": "235"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "What is your organisation's annual turnover?"
                },
                {
                    "fields": [
                        {
                            "key": "NENGMj",
                            "type": "list",
                            "title": "Which membership organisations are you a member of?",
                            "answer": "both"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "Which membership organisations are you a member of?"
                }
            ]
        },
        {
            "name": "organisation-type-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ChXWIQ",
                            "type": "list",
                            "title": "How is your organisation classified?",
                            "answer": [
                                "none"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "How is your organisation classified?"
                },
                {
                    "fields": [
                        {
                            "key": "ETJaFn",
                            "type": "text",
                            "title": "How is your organisation classified?",
                            "answer": "Test Organisation Type Form"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "How is your organisation classified?"
                },
                {
                    "fields": [
                        {
                            "key": "ILVEOG",
                            "type": "multiInput",
                            "title": "Your trustees or committee members",
                            "answer": [
                                {
                                    "mrCotx": "Test Organisation Type Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "Names of trustees or committee members"
                },
                {
                    "fields": [
                        {
                            "key": "TgBzyM",
                            "type": "list",
                            "title": "How long has your organisation been operating?",
                            "answer": "more-than-2-years-but-less-than-3"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "How long has your organisation been operating?"
                },
                {
                    "fields": [
                        {
                            "key": "sVlFcN",
                            "type": "text",
                            "title": "Upload your organisation's annual accounts that you have available",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "Upload your organisation's annual accounts that you have available"
                }
            ]
        },
        {
            "name": "current-services-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "QOlbCV",
                            "type": "list",
                            "title": "Have you provided a night shelter or emergency accommodation on or after 1 April 2019?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Have you provided a night shelter or emergency accommodation on or after 1 April 2019?"
                },
                {
                    "fields": [
                        {
                            "key": "affVbH",
                            "type": "list",
                            "title": "Is the night shelter or emergency accommodation communal?",
                            "answer": true
                        },
                        {
                            "key": "ttEOXi",
                            "type": "list",
                            "title": "Is the night shelter or emergency accommodation single room accommodation?",
                            "answer": true
                        },
                        {
                            "key": "dSdeYa",
                            "type": "text",
                            "title": "How many bed spaces did the night shelter or emergency accommodation provide from 1 April 2022 to 31 March 2023?",
                            "answer": "323"
                        },
                        {
                            "key": "gXvnZA",
                            "type": "list",
                            "title": "Is the night shelter or emergency accommodation used for SWEP (severe weather emergency protocol)?",
                            "answer": false
                        },
                        {
                            "key": "vStFMu",
                            "type": "list",
                            "title": "Do you accept referrals from the local authority or other agencies for available bed spaces?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Night shelter or emergency accommodation"
                },
                {
                    "fields": [
                        {
                            "key": "YyMRdP",
                            "type": "text",
                            "title": "How many nights did the night shelter or emergency accommodation open from 1 April 2022 to 31 March 2023?",
                            "answer": "7"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "How many nights did the night shelter or emergency accommodation open from 1 April 2022 to 31 March 2023?"
                },
                {
                    "fields": [
                        {
                            "key": "STfdvD",
                            "type": "list",
                            "title": "Do you currently provide day provision?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Do you currently provide day provision?"
                },
                {
                    "fields": [
                        {
                            "key": "bCXNtj",
                            "type": "monthYear",
                            "title": "When did you start providing day provision?",
                            "answer": "2023-06"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "When did you start providing day provision?"
                },
                {
                    "fields": [
                        {
                            "key": "ULPcAU",
                            "type": "list",
                            "title": "Which day provision services are you currently providing?",
                            "answer": [
                                "other"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Which day provision services are you currently providing?"
                },
                {
                    "fields": [
                        {
                            "key": "zwQHCl",
                            "type": "freeText",
                            "title": "Which other day provision do you currently provide?",
                            "answer": "<p>Test Current Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Which other day provision do you currently provide?"
                },
                {
                    "fields": [
                        {
                            "key": "GBfYfn",
                            "type": "list",
                            "title": "Do you currently provide any other services?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Do you currently provide any other services?"
                },
                {
                    "fields": [
                        {
                            "key": "wViAiU",
                            "type": "freeText",
                            "title": "What other services are you currently providing?",
                            "answer": "<p>Test Current Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "What other services are you currently providing?"
                },
                {
                    "fields": [
                        {
                            "key": "umAyqH",
                            "type": "list",
                            "title": "Do you currently provide specialist support?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Do you currently provide specialist support?"
                },
                {
                    "fields": [
                        {
                            "key": "JCUQcR",
                            "type": "list",
                            "title": "Who do you currently provide targeted specialist support to?",
                            "answer": [
                                "women"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Who do you currently provide targeted specialist support to?"
                }
            ]
        },
        {
            "name": "building-works-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "lifPop",
                            "type": "list",
                            "title": "Will you use the funding to conduct building works?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you use the funding to conduct building works?"
                },
                {
                    "fields": [
                        {
                            "key": "fmcTtE",
                            "type": "text",
                            "title": "Number of new single room units (optional)",
                            "answer": "344"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Number of new single room units (optional)"
                },
                {
                    "fields": [
                        {
                            "key": "xGnWEW",
                            "type": "list",
                            "title": "Do you need planning approval for your proposal?",
                            "answer": "yes"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you need planning approval for your proposal?"
                },
                {
                    "fields": [
                        {
                            "key": "KhISvR",
                            "type": "list",
                            "title": "Have you made an application for planning permission?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Have you made an application for planning permission?"
                },
                {
                    "fields": [
                        {
                            "key": "YFPgTB",
                            "type": "list",
                            "title": "Have you received any pre-application planning advice?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Have you received any pre-application planning advice?"
                },
                {
                    "fields": [
                        {
                            "key": "mADkNz",
                            "type": "text",
                            "title": "Give a brief summary of the advice you received",
                            "answer": "Test Building Works NS Form"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Give a brief summary of the advice you received"
                },
                {
                    "fields": [
                        {
                            "key": "AYDIPX",
                            "type": "list",
                            "title": "Will you procure a construction contract for the building works?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you procure a construction contract for the building works?"
                },
                {
                    "fields": [
                        {
                            "key": "nyusrL",
                            "type": "list",
                            "title": "Will you use any professional advisors for the proposal?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you use any professional advisors for the proposal?"
                },
                {
                    "fields": [
                        {
                            "key": "SQEpBt",
                            "type": "multiInput",
                            "title": "Details of professional advisors",
                            "answer": [
                                {
                                    "cbYcqS": "Test Building Works NS Form",
                                    "muRwiL": "Test Building Works NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Details of professional advisors"
                },
                {
                    "fields": [
                        {
                            "key": "rYAgMN",
                            "type": "list",
                            "title": "Will you be hiring contractors to complete the building works?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you be hiring contractors to complete the building works?"
                },
                {
                    "fields": [
                        {
                            "key": "wUFaUF",
                            "type": "list",
                            "title": "Do you have a cost estimate for the building works?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you have a cost estimate for the building works?"
                },
                {
                    "fields": [
                        {
                            "key": "NOMwBb",
                            "type": "text",
                            "title": "Upload cost estimate",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload cost estimate"
                },
                {
                    "fields": [
                        {
                            "key": "ZmYhgR",
                            "type": "list",
                            "title": "Do you have a condition survey?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you have a condition survey?"
                },
                {
                    "fields": [
                        {
                            "key": "aTxAPP",
                            "type": "text",
                            "title": "Upload a condition survey",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload a condition survey"
                },
                {
                    "fields": [
                        {
                            "key": "SdwIUb",
                            "type": "list",
                            "title": "Do you have a buildings and contents insurance certificate?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you have a buildings and contents insurance certificate?"
                },
                {
                    "fields": [
                        {
                            "key": "NlDVCg",
                            "type": "text",
                            "title": "Upload buildings and contents insurance certificate",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload buildings and contents insurance certificate"
                },
                {
                    "fields": [
                        {
                            "key": "RXIYZY",
                            "type": "list",
                            "title": "Do you own the premises?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you own the premises?"
                },
                {
                    "fields": [
                        {
                            "key": "rMvZDG",
                            "type": "text",
                            "title": "Upload the land owner's consent",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload the land owner's consent"
                },
                {
                    "fields": [
                        {
                            "key": "muhnok",
                            "type": "list",
                            "title": "How long is left on the lease agreement?",
                            "answer": "less-than-4-years"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "How long is left on the lease agreement?"
                },
                {
                    "fields": [
                        {
                            "key": "GLOpmu",
                            "type": "text",
                            "title": "Upload correspondence from your landlord to show that lease renewal discussions have started",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload correspondence from your landlord to show that lease renewal discussions have started"
                },
                {
                    "fields": [
                        {
                            "key": "kQJIbS",
                            "type": "text",
                            "title": "Upload heads of terms outlining new lease agreement",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload heads of terms outlining new lease agreement"
                },
                {
                    "fields": [
                        {
                            "key": "skBfqS",
                            "type": "list",
                            "title": "Is the building listed?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Is the building listed?"
                },
                {
                    "fields": [
                        {
                            "key": "abdbzq",
                            "type": "text",
                            "title": "Upload listed building consent",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload listed building consent"
                }
            ]
        }
    ]
}
"""
)

cypr1_application_store_json_template = Template(
    """
{
  "account_id": "613bacb1-b598-4782-be0e-c9b5a679af37",
  "date_submitted": "2023-10-03T15:52:07.595488",
  "forms": [
    {
      "name": "applicant-information-cyp",
      "questions": [
        {
          "category": "pyQsHV",
          "fields": [
            {
              "answer": "Tester",
              "key": "rKHBnt",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "Data",
              "key": "yWtfkb",
              "title": "Alternative name",
              "type": "text"
            },
            {
              "answer": "Test Engineer",
              "key": "kbOHaM",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "BKOHaM",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "00000111111",
              "key": "CyANDT",
              "title": "Lead contact telephone number",
              "type": "text"
            },
            {
              "answer": true,
              "key": "DbFHbD",
              "title": "Is the lead contact the same person as the authorised signatory?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "name-your-application-cyp",
      "questions": [
        {
          "category": "XDnkqz",
          "fields": [
            {
              "answer": "Seed_Assessment_Test",
              "key": "bsUoNG",
              "title": "Name your application",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Name your application",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "about-your-organisation-cyp",
      "questions": [
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "Seed_assessment",
              "key": "JbmcJE",
              "title": "Organisation name",
              "type": "text"
            },
            {
              "answer": true,
              "key": "KUdOhN",
              "title": "Does your organisation use any other names?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Organisation details",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "Test",
              "key": "NcnYCn",
              "title": "Alternative name 1",
              "type": "text"
            },
            {
              "answer": null,
              "key": "rtFyqT",
              "title": "Alternative name 2",
              "type": "text"
            },
            {
              "answer": null,
              "key": "DYUbGM",
              "title": "Alternative name 3",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative names of your organisation",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "<p>Activity 1</p>",
              "key": "kxgOne",
              "title": "Activity 1",
              "type": "freeText"
            },
            {
              "answer": "<p>Activity 2</p>",
              "key": "kxgTwo",
              "title": "Activity 2 (optional)",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "kxgThr",
              "title": "Activity 3 (optional)",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about your organisation's main activities",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "upper-or-lower-tier-local-authority",
              "key": "jcmcJE",
              "title": "Organisation classification",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How is your organisation classified?",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "12",
              "key": "jencJE",
              "title": "Company registration number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Company registration number",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "35 Happy street, null, Happyville, null, H499YY",
              "key": "rmBPvK",
              "title": "Registered organisation address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Registered organisation address",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "Optional lane, null, Optionskirk, null, O780OO",
              "key": "smBPvK",
              "title": "Alternative organisation address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative organisation address (optional)",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": true,
              "key": "MRdGKt",
              "title": "Is your application a joint bid in partnership with other organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Is your application a joint bid in partnership with other organisations?",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": [
                {
                  "GpLJDu": "Partner",
                  "IXjMWp": {
                    "addressLine1": "Partner address",
                    "addressLine2": "",
                    "county": "",
                    "postcode": "P345RK",
                    "town": "Partnersville"
                  },
                  "MKbOlA": "https://partners233413414r3er23r32r23r23r.com",
                  "OghGGr": null,
                  "RphKTp": null
                }
              ],
              "key": "tZoOKx",
              "title": "Partner organisation details",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Partner organisation details",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "<p>Partners help.</p>",
              "key": "xPcbJX",
              "title": "Tell us about how you plan to work with the partner organisations",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about how you plan to work with the partner organisations",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": true,
              "key": "RUdOhN",
              "title": "Does an agreement currently exist between your organisation and the partnership organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Does an agreement currently exist between your organisation and the partnership organisations?",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": [
                {
                  "EShKlA": "https://mylink"
                }
              ],
              "key": "tYoOqx",
              "title": "Website and social media",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Website and social media",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-cyp",
      "questions": [
        {
          "category": "OEGHno",
          "fields": [
            {
              "answer": true,
              "key": "sdeLyR",
              "title": "Confirm your organisation adheres to the government code of conduct",
              "type": "list"
            },
            {
              "answer": true,
              "key": "SUTxtj",
              "title": "Confirm your organisation has a data handling process in place",
              "type": "list"
            },
            {
              "answer": false,
              "key": "WWHYDI",
              "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
              "type": "list"
            },
            {
              "answer": false,
              "key": "WGmcyu",
              "title": "Confirm that your organisation's safegaurding policies are up to date",
              "type": "list"
            },
            {
              "answer": false,
              "key": "WGmDZu",
              "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "existing-work-cyp",
      "questions": [
        {
          "category": "PPssHV",
          "fields": [
            {
              "answer": "<p>I have no similar ones</p>",
              "key": "MbDkNZ",
              "title": "How will you avoid duplicating existing work or projects in this area?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How will you avoid duplicating existing work or projects in this area?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "skills-and-experience-cyp",
      "questions": [
        {
          "category": "pyQhSV",
          "fields": [
            {
              "answer": true,
              "key": "HrGXKi",
              "title": "Have you delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Have you delivered projects like this before?",
          "status": "COMPLETED"
        },
        {
          "category": "pyQhSV",
          "fields": [
            {
              "answer": "<p>Lots of prior testing</p>",
              "key": "qPcbJQ",
              "title": "Tell us about how you plan to work with the partner organisations",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about how you have worked on similar previous projects",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "working-with-fund-beneficiaries-cyp",
      "questions": [
        {
          "category": "Nyppws",
          "fields": [
            {
              "answer": "<p>ill work alright</p>",
              "key": "XPDbsh",
              "title": "Tell us how you will identify and work with the intended fund beneficiaries",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us how you will identify and work with the intended fund beneficiaries",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "project-milestones-cyp",
      "questions": [
        {
          "category": "zACCPu",
          "fields": [
            {
              "answer": [
                {
                  "HpLJDu": "To do a thing",
                  "LZbOBu": {
                    "LZbOBu__month": 1,
                    "LZbOBu__year": 2022
                  }
                }
              ],
              "key": "tAoOKx",
              "title": "Project milestones",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Project milestones",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "outputs-and-outcomes-cyp",
      "questions": [
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": "<p>output</p>",
              "key": "MADkNZ",
              "title": "Give a brief summary of your project, including what you hope to achieve",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Give a brief summary of your project, including what you hope to achieve",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": "<p>i will measure many things</p>",
              "key": "nbDkNZ",
              "title": "How will you measure the outcome of your project?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How will you measure the outcome of your project?",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": [
                "trauma-support",
                "mental-health-and-wellbeing"
              ],
              "key": "fHodTO",
              "title": "What is the main focus of your project?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "What is the main focus of your project?",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": [
                "ukrainian-schemes"
              ],
              "key": "vYYoAC",
              "title": "Which cohort will your project focus on?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which cohort will your project focus on?",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": "122",
              "key": "tAtJGz",
              "title": "How many fund recipients from the Ukraine schemes do you expect your project to support with the funding?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "How many fund recipients from the Ukraine schemes do you expect your project to support with the funding?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "location-of-activities-cyp",
      "questions": [
        {
          "category": "wxOzRK",
          "fields": [
            {
              "answer": true,
              "key": "iqqqTk",
              "title": "Is the project taking place regionally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Is the project taking place regionally?",
          "status": "COMPLETED"
        },
        {
          "category": "wxOzRK",
          "fields": [
            {
              "answer": [
                {
                  "kaQUSV": "Everywhere"
                }
              ],
              "key": "tApPKx",
              "title": "Which local authority areas will you work across?",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Which local authority areas will you work across?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "objectives-and-activities-cyp",
      "questions": [
        {
          "category": "zzpzem",
          "fields": [
            {
              "answer": [
                {
                  "HpLJCu": "make people smile",
                  "kaQUfV": "Happy "
                },
                {
                  "HpLJCu": "do things",
                  "kaQUfV": "productive"
                }
              ],
              "key": "tAoPKx",
              "title": "Objectives and activities",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Objectives and activities",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "risk-and-deliverability-cyp",
      "questions": [
        {
          "category": "hhbMar",
          "fields": [
            {
              "answer": [
                {
                  "CzoasH": "No risk",
                  "MPHvIr": "Medium",
                  "SKQluJ": "to lessen risk",
                  "eADHGN": "Medium"
                },
                {
                  "CzoasH": "another risk",
                  "MPHvIr": "Low",
                  "SKQluJ": "none",
                  "eADHGN": "High"
                }
              ],
              "key": "qQLYzL",
              "title": "Risks to the project",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Risks to the project",
          "status": "COMPLETED"
        },
        {
          "category": "hhbMar",
          "fields": [
            {
              "answer": "Tester",
              "key": "KHESdE",
              "title": "Who owns the overall risk register?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Who owns the overall risk register?",
          "status": "COMPLETED"
        },
        {
          "category": "hhbMar",
          "fields": [
            {
              "answer": "<p>The boss is in charge</p>",
              "key": "KHESFr",
              "title": "Tell us about your organisation's governance structure",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about your organisation's governance structure",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "value-for-money-cyp",
      "questions": [
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": "3444",
              "key": "JXKUcj",
              "title": "27 September 2023 to 31 March 2024",
              "type": "text"
            },
            {
              "answer": "3444",
              "key": "OnPeeS",
              "title": "1 April 2024 to 31 March 2025",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Funding requested",
          "status": "COMPLETED"
        },
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": [
                {
                  "JizgZP": 2000,
                  "gLQlyJ": "Balloons",
                  "kjuHtl": "27 September 2023 to 31 March 2024"
                }
              ],
              "key": "qwktzL",
              "title": "Item of expenditure",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Item of expenditure",
          "status": "COMPLETED"
        },
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": true,
              "key": "qwktlZ",
              "title": "Will you use additional funding for your project?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Will you use additional funding for your project?",
          "status": "COMPLETED"
        },
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": [
                {
                  "HpLJyL": {
                    "HpLJyL__month": 1,
                    "HpLJyL__year": 2011
                  },
                  "MadvIr": "Capital",
                  "gLqiyJ": "Org X",
                  "yuzbjT": 2
                }
              ],
              "key": "qqktzL",
              "title": "Funding source",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Additional funding",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ],
  "fund_id": "1baa0f68-4e0a-4b02-9dfe-b5646f089e65",
  "id": "$app_id",
  "language": "en",
  "last_edited": "2023-10-03T15:48:23.803396",
  "project_name": "Seed_Assessment_Test",
  "reference": "CYP-R1-ZGEUOJ",
  "round_id": "888aae3d-7e2c-4523-b9c1-95952b3d1644",
  "round_name": "Round 1",
  "started_at": "2023-10-03T11:29:56.283505",
  "status": "SUBMITTED"
}
"""
)
