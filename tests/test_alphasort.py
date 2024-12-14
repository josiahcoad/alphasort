import os
import tempfile
import textwrap

import pytest

from src.alphasort import sort_alpha_regions, sort_alpha_regions_in_lines


def test_alphasort_in_lines():
    lines = [
        "# alphasort: on",
        "b",
        "c",
        "d",
        "# alphasort: off",
        "a",
    ]

    comment_delimiter = "#"
    result = sort_alpha_regions_in_lines(lines, comment_delimiter)

    assert result == [
        "# alphasort: on",
        "b",
        "c",
        "d",
        "# alphasort: off",
        "a",
    ]


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as file:
        file_name = file.name
    yield file_name
    os.remove(file_name)


def test_alphasort_file(temp_file: str):
    # Given...
    with open(temp_file, "w") as f:
        f.write(
            textwrap.dedent(
                """
                # alphasort: on

                b
                c
                # alphasort: off
                a
                """
            ).strip()
        )

    # When...
    sort_alpha_regions(temp_file)

    # Then...
    with open(temp_file, "r") as f:
        result = f.read()

    assert (
        result
        == textwrap.dedent(
            """
        # alphasort: on

        b
        c
        # alphasort: off
        a
        """
        ).strip()
    )
