import argparse


def collect_files(
    path: str,
    include_folders: bool,
    entire_path: bool,
    recursive: bool,
    regex_groups: list[str],
):
    # TODO Finish collecting all files
    pass


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
