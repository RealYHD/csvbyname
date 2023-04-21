import argparse
import os
import re


def matcher(path: str, regex_groups: list[str]):
    matches = []
    for regex in regex_groups:
        matches[path]


def collect_files(
    dir_path: str,
    include_folders: bool,
    entire_path: bool,
    recursive: bool,
    regex_groups: list[str],
):
    collected = {}

    def matcher(full_path, use_full_path):
        return [
            re.match(
                regex, full_path if use_full_path else os.path.basename(full_path)
            ).groups(1)
            for regex in regex_groups
        ]

    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            if include_folders:
                if full_path not in collected:
                    collected[full_path] = set()
                collected = collected[full_path] | matcher(full_path, entire_path)
            collected = collected | collect_files(
                full_path, include_folders, entire_path, recursive, regex_groups
            )
        elif os.path.isfile(full_path):
            if full_path not in collected:
                collected[full_path] = set()
            collected = collected[full_path] | matcher(full_path, entire_path)


def write_collected_to_csv(output_path: str, collected: dict[str, dict[str, str]]):
    # TODO Finish writing collected files/paths to CSV.
    pass


def run(args):
    collect_files(
        args.directory,
        args.include_folders,
        args.entire_path,
        args.recursive,
        args.add_regex_property,
    )


def main():
    argparser = argparse.ArgumentParser(
        "csvbyname",
        description="Catalogue a directory of files by patterns in their names into a "
        "CSV.",
    )
    argparser.add_argument(
        "directory",
        type=str,
        help="The directory containing the files to obtain catalogue names of",
        metavar="i",
    )
    argparser.add_argument(
        "output", type=str, help="The path to the catalogued CSVs.", metavar="o"
    )
    argparser.add_argument(
        "-l",
        "--include-folder",
        help="Include folders in the cataloguing process",
        action="store_true",
        required=False,
        default=False,
    )
    argparser.add_argument(
        "-e",
        "--entire-path",
        help="Include the full path when applying the groupings to find properties",
        action="store_true",
        required=False,
        default=False,
    )
    argparser.add_argument(
        "-r",
        "--recursive",
        help="Catalogue recursively",
        action="store_true",
        required=False,
        default=False,
    )
    argparser.add_argument(
        "-p",
        "--add-regex-property",
        help="Add a property in the resulting CSV obtained from the first capture "
        "group of the given REGEX in the following format:\n property-name:regex",
        nargs="+",
    )

    args = argparser.parse_args()
    run(args)
