import pytest
from api.routes._helpers import remove_html_tags


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ({"hello": "<p>world<p>"}, {"hello": "world"}),
        ([{"hello": "<p>world<p>"}], [{"hello": "world"}]),
        ("<p>hello<p>", "hello"),
    ],
)
def test_remove_html_tags(input, expected_output):
    response = remove_html_tags(input)
    assert response == expected_output
