field_id_schema = {
    "type": ["string", "array"],
    "items": {
        "type": "string"
    }
}

answer_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "field_id": field_id_schema,
            "form_name": {
                "type": "string"
            },
            # TODO
            # the field types have been copid over from the application store payload thus far
            # we might want to look at assessment specific types for display
            "field_type": {
                "type": "string",
                "enum": [
                    "textField", 
                    "yesNoField", 
                    "radiosField", 
                    "datePartsField", 
                    "UkAddressField", 
                    "websiteField", 
                    "multiInputField", 
                    "multilineTextField", 
                    "textArea", 
                    "emailAddressField", 
                    "telephoneNumberField", 
                    "numberField", 
                    "checkboxesField", 
                    "fileUploadField"
                ]
            },
            "question": {
                "type": "string"
            }
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

themes_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "answers": answer_schema,
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

sub_criteria_schema = {
    "id": "sub_criteria_schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "themes": themes_schema,
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

unscored_section_schema = {
    "id": "unscored_section_schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "sub_criteria": sub_criteria_schema,
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

scored_criteria_schema = {
    "id": "scored_criteria_schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "weighting": {
                "type": "number",
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 1,
            },
            "sub_criteria": sub_criteria_schema,
        },
        "additionalProperties": False,
        "minProperties": 4,
    },
}

top_level_assessment_mapping_schema = {
    "id": "top_level_assessment_mapping_schema",
    "type": "object",
    "properties": {
        "schema_id": {"type": "string"},
        "unscored_assessment_sections": unscored_section_schema,
        "scored_assessment_criteria": scored_criteria_schema,
    },
    "additionalProperties": False,
    "minProperties": 3,
}
