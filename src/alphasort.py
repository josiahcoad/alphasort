import argparse
import os
from glob import glob
from pathlib import Path

delimiters_comment = {
    "#": [".py", ".sh", ".yaml", ".yml", ".rb", ".pl", ".r"],
    "//": [".js", ".ts", ".c", ".cpp", ".java", ".cs", ".php", ".go", ".swift"],
    "<!--": [".html", ".xml", ".xhtml"],
    "--": [".sql", ".hs", ".lua"],
    "%": [".tex", ".m", ".matlab"],
    "'": [".vb", ".vbs"],
    ";": [".asm"],
    "REM": [".bat"],
}

COMMENT_DELIMITERS = {
    ext: delim for delim, file_exts in delimiters_comment.items() for ext in file_exts
}

COMMENT_DELIMITER_FALLBACK = "#"
KEYWORD = "alphasort"
KEYWORD_BEGIN = "on"
KEYWORD_END = "off"


def sort_alpha_regions(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    comment_delimiter = COMMENT_DELIMITERS.get(
        Path(filepath).suffix, COMMENT_DELIMITER_FALLBACK
    )
    sorted_lines = sort_alpha_regions_in_lines(lines, comment_delimiter)

    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(sorted_lines)


def sort_alpha_regions_in_lines(lines: list[str], comment_delimiter: str) -> list[str]:
    in_sort_block = False
    sorted_lines: list[str] = []
    buffer: list[str] = []

    for line in lines:
        if f"{comment_delimiter} {KEYWORD}: {KEYWORD_BEGIN}" in line:
            in_sort_block = True
            sorted_lines.append(line)
            continue

        if f"{comment_delimiter} {KEYWORD}: {KEYWORD_END}" in line:
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


def process_directory(path: str, verbose: bool) -> None:
    """
    `path` examples:
    - path/to/directory
    - path/to/directory/*/*.py
    - path/to/directory/test.py
    - path/to/directory/**/test.py
    """
    for filepath in glob(path):
        if os.path.isfile(filepath):
            if verbose:
                print(f"Sorting {os.path.relpath(filepath)}")
            sort_alpha_regions(filepath)


def main():
    parser = argparse.ArgumentParser(description="Sort alpha regions.")
    parser.add_argument("glob", default="*", help="glob pattern to match")
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose")
    args = parser.parse_args()
    process_directory(args.glob, args.verbose)


if __name__ == "__main__":
    main()
