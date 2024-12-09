import argparse
from pathlib import Path

import tomllib

with open("config.toml", "rb") as f:
    CONFIG = tomllib.load(f)

COMMENT_DELIMITERS = {
    ext: delim
    for delim, file_exts in CONFIG["delimiters"]["comment"].items()
    for ext in file_exts
}
COMMENT_DELIMITER_FALLBACK = "#"
KEYWORD = CONFIG["delimiters"]["keyword"]
KEYWORD_BEGIN = CONFIG["delimiters"]["begin"]
KEYWORD_END = CONFIG["delimiters"]["end"]


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


def process_directory(
    directory: str,
    file_extension: str = "",
    verbose: bool = False,
) -> None:
    for filepath in Path(directory).rglob(f"*{file_extension}"):
        if filepath.is_file():
            if verbose:
                print(f"Sorting {filepath}")
            sort_alpha_regions(str(filepath))


def main():
    parser = argparse.ArgumentParser(description="Sort alpha regions.")
    parser.add_argument("directory", help="The directory to process.")
    parser.add_argument("--suffix", default="", help="filename suffix to match")
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose")
    args = parser.parse_args()
    process_directory(args.directory, args.suffix, args.verbose)


if __name__ == "__main__":
    main()
