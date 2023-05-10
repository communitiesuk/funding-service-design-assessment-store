from unittest.mock import Mock

import pytest
from api.routes.subcriterias.get_sub_criteria import (
    deprecated_sort_add_another_component_contents,
)
from api.routes.subcriterias.get_sub_criteria import (
    format_add_another_component_contents,
)


@pytest.mark.parametrize(
    "answer_from_form_runner, expected_description, expected_amount",
    [
        (
            ["An Answer : £1"],
            ["An Answer "],
            ["£1"],
        ),
        (
            ["An Answer : with colon : £1"],
            ["An Answer : with colon "],
            ["£1"],
        ),
        (
            ["An : Answer : with : lots: of :colons : £1"],
            ["An : Answer : with : lots: of :colons "],
            ["£1"],
        ),
        (
            ["An Answer : £1", "Another Answer : £2"],
            ["An Answer ", "Another Answer "],
            ["£1", "£2"],
        ),
    ],
)
def test_deprecated_sort_add_another_component_contents(
    answer_from_form_runner, expected_description, expected_amount, app
):
    themes_answers = [
        {
            "presentation_type": "heading",
            "question": "Test Heading",
            "field_id": "123",
            "answer": "Test Heading",
        },
        {
            "presentation_type": "description",
            "question": "Test Description",
            "field_id": "123",
            "answer": answer_from_form_runner,
        },
        {
            "presentation_type": "amount",
            "question": "Test Amount",
            "field_id": "123",
            "answer": answer_from_form_runner,
        },
    ]

    deprecated_sort_add_another_component_contents(themes_answers)

    assert themes_answers[0]["answer"] == "Test Heading"
    assert themes_answers[1]["answer"] == expected_description
    assert themes_answers[2]["answer"] == expected_amount


@pytest.mark.parametrize(
    "answer_from_form_runner, expected_nested_table_tuple",
    [
        (
            [
                {"FwPOFx": "test", "SPGORz": 12},
                {"FwPOFx": "323", "SPGORz": 42442},
            ],
            [
                ["Description", ["test", "323"]],
                ["Amount", [12, 42442]],
            ],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_format_add_another_component_contents(
    answer_from_form_runner, expected_nested_table_tuple, app
):
    themes_answer = {
        "field_id": "NdFwgy",
        "field_type": "multiInputField",
        "presentation_type": "table",
        "question": [
            "Capital costs",
            {
                "FwPOFx": "Description",
                "SPGORz": "Amount",
            },
        ],
        "answer": answer_from_form_runner,
    }

    (theme_answer,) = format_add_another_component_contents([themes_answer])

    assert theme_answer["question"] == "Capital costs"
    assert theme_answer["answer"] == expected_nested_table_tuple


def test_deprecated_sort_add_another_component_contents_log_when_no_answer(
    monkeypatch,
):
    current_app = Mock()
    monkeypatch.setattr(
        "api.routes.subcriterias.get_sub_criteria.current_app", current_app
    )

    themes_answers = [
        {
            "presentation_type": "heading",
            "question": "Test Heading",
            "field_id": "123",
        },
        {
            "presentation_type": "description",
            "question": "Test Description",
            "field_id": "123",
        },
        {
            "presentation_type": "amount",
            "question": "Test Amount",
            "field_id": "123",
        },
    ]

    deprecated_sort_add_another_component_contents(themes_answers)

    current_app.logger.debug.assert_called_with(
        "Answer not provided for field_id: 123"
    )
