# PYTHON_ARGCOMPLETE_OK
import argparse
import glob
import logging
import re
from pathlib import Path

import argcomplete

delimiters_comment = {
    "#": [".py", ".sh", ".yaml", ".yml", ".rb", ".pl", ".r"],
    "//": [".js", ".ts", ".c", ".cpp", ".java", ".cs", ".php", ".go", ".swift"],
    "<!--": [".html", ".xml", ".xhtml"],
    "--": [".sql", ".hs", ".lua"],
    "%": [".tex", ".m", ".matlab"],
    "'": [".vb", ".vbs"],
    ";": [".asm"],
    "REM": [".bat"],
    '"_comment": "': [".json"],
}

COMMENT_DELIMITERS = {
    ext: delim for delim, file_exts in delimiters_comment.items() for ext in file_exts
}

COMMENT_DELIMITER_FALLBACK = "#"
KEYWORD = "alphasort"
KEYWORD_BEGIN = "on"
KEYWORD_END = "off"


def sort_alpha_regions(filepath: str) -> None:
    try:
        lines = Path(filepath).read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        logging.info("Skipping %s because not utf-8 encoded", filepath)
        return

    comment_delimiter = COMMENT_DELIMITERS.get(
        Path(filepath).suffix, COMMENT_DELIMITER_FALLBACK
    )
    sorted_lines = sort_alpha_regions_in_lines(lines, comment_delimiter)

    with Path(filepath).open("w", encoding="utf-8") as file:
        file.writelines(sorted_lines)


def sort_alpha_regions_in_lines(lines: list[str], comment_delimiter: str) -> list[str]:
    in_sort_block = False
    sorted_lines: list[str] = []
    buffer: list[str] = []

    for line in lines:
        if re.search(
            rf"{re.escape(comment_delimiter)}\s*{KEYWORD}:\s*{KEYWORD_BEGIN}", line
        ):
            in_sort_block = True
            sorted_lines.append(line)
            continue

        if re.search(
            rf"{re.escape(comment_delimiter)}\s*{KEYWORD}:\s*{KEYWORD_END}", line
        ):
            in_sort_block = False
            sorted_lines.extend(sorted(buffer))
            sorted_lines.append(line)
            buffer = []
            continue

        if in_sort_block:
            buffer.append(line)
        else:
            sorted_lines.append(line)

    if in_sort_block:
        sorted_lines.extend(sorted(buffer))

    return sorted_lines


def process_directory(path: str, ignore_path: str, *, verbose: bool) -> None:
    """
    `path` examples:
    - path/to/directory
    - path/to/directory/*/*.py
    - path/to/directory/test.py
    - path/to/directory/**/test.py
    """
    for filepath in glob.glob(path, recursive=True):  # noqa: PTH207
        if Path(filepath).is_file():
            if ignore_path and is_file_in_path(ignore_path, filepath):
                if verbose:
                    logging.info("Ignoring %s", filepath)
                continue
            logging.debug("Sorting %s", filepath)
            sort_alpha_regions(str(filepath))


def is_file_in_path(path: str, filepath: str) -> bool:
    base_path = Path(path).resolve()
    file_path = Path(filepath).resolve()
    return base_path in file_path.parents or base_path == file_path


def setup_logging(verbose: int) -> None:
    log_level = logging.WARNING
    if verbose == 1:
        log_level = logging.INFO
    elif verbose >= 2:  # noqa: PLR2004
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sort alpha regions.")
    parser.add_argument("glob", nargs="?", default="**/*", help="glob pattern to match")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v for INFO, -vv for DEBUG)",
    )
    parser.add_argument("--ignore", "-i", default="", help="path to ignore")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    setup_logging(args.verbose)
    process_directory(args.glob, args.ignore, verbose=args.verbose)


if __name__ == "__main__":
    main()
