import tempfile
import textwrap
from contextlib import contextmanager
from pathlib import Path

from src.alphasort import sort_alpha_regions, sort_alpha_regions_in_lines


def test_alphasort_in_lines() -> None:
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


@contextmanager
def make_temp_file(file_ext: str):  # noqa: ANN201
    with tempfile.NamedTemporaryFile(mode="w", suffix=f".{file_ext}") as file:
        yield file.name


def alphasort_python() -> None:
    with make_temp_file("py") as temp_file:
        # Given...
        with Path(temp_file).open("w") as f:
            f.write(
                textwrap.dedent(
                    """
                    # alphasort: on

                    bat
                    cat
                    # alphasort: off
                    ant
                    """
                ).strip()
            )

        # When...
        sort_alpha_regions(temp_file)

        # Then...
        result = Path(temp_file).read_text()

    assert (
        result
        == textwrap.dedent(
            """
        # alphasort: on

        bat
        cat
        # alphasort: off
        ant
        """
        ).strip()
    )


def alphasort_json() -> None:
    with make_temp_file("json") as temp_file:
        # Given...
        with Path(temp_file).open("w") as f:
            f.write(
                textwrap.dedent(
                    """
                    {
                        "_comment": "alphasort: on",
                        "carrot": 2,
                        "banana": 1,
                        "_comment": "alphasort: off",
                        "apple": 2,
                    }
                    """
                ).strip()
            )

        # When...
        sort_alpha_regions(temp_file)

        # Then...
        result = Path(temp_file).read_text()

    assert (
        result
        == textwrap.dedent(
            """
        # alphasort: on

        banana
        carrot
        # alphasort: off
        apple
        """
        ).strip()
    )
