import tempfile
import textwrap

from src.alphasort import sort_alpha_regions, sort_alpha_regions_in_lines


def test_alphasort_in_lines():
    lines = [
        "# alphasort: on",
        "d",
        "c",
        "b",
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


def test_alphasort_file():
    # make a temporary file with tempfile (call it temp.py)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as file:
        file.write(
            textwrap.dedent(
                """
                # alphasort: on
                d

                c
                b
                # alphasort: off
                a
                """
            ).strip()
        )

    sort_alpha_regions(file.name)

    with open(file.name, "r") as f:
        result = f.read()

    assert (
        result
        == textwrap.dedent(
            """
        # alphasort: on

        b
        c
        d
        # alphasort: off
        a
        """
        ).strip()
    )
