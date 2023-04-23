import argparse
import logging

from csvbyname.generate import collect_files, write_collected_to_csv


def run(args):
    logger.info('Collecting files from "%s"', args.directory)
    collected, pkeys = collect_files(
        args.directory,
        args.include_folders,
        args.entire_path,
        args.recursive,
        args.add_re_property,
    )
    write_collected_to_csv(args.output, collected, pkeys, args.output_basename)


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
        "--include-folders",
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
        "--add-re-property",
        help="Add a property in the resulting CSV obtained from the first capture "
        "group of the given REGEX in the following format:\n property-name:regex.\n"
        "Alternatively, use named REGEX groups.",
        nargs="+",
        type=str,
        required=True
    )
    argparser.add_argument(
        "-n",
        "--output-basename",
        help='Adds a column called "basename" to the resulting CSV where it is just '
        "The base name of the path instead of the entire path. This is not guaranteed "
        "to be unique.",
        default=False,
        required=False,
        action="store_true",
    )
    argparser.add_argument(
        "-V",
        "--verbosity",
        help="Set the verbosity of the logging",
        type=str,
        required=False,
        default="INFO",
    )

    args = argparser.parse_args()
    logging.basicConfig(level=args.verbosity.upper())
    global logger
    logger = logging.getLogger(__name__)
    run(args)


if __name__ == "__main__":
    main()
