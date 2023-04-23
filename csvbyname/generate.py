import csv
import os
import re
from typing import Iterable
from csvbyname import exceptions
import logging

logger = logging.getLogger(__name__)


def matcher(full_path: str, use_full_path: bool, regex_groups: list[str]):
    captured_properties = {}
    for regex_and_group in regex_groups:
        match_assume_named = re.match(
            regex_and_group, full_path if use_full_path else os.path.basename(full_path)
        )
        if match_assume_named and len(match_assume_named.groupdict()) > 0:
            for group, val in match_assume_named.groupdict().items():
                if group not in captured_properties:
                    captured_properties[group] = val
                else:
                    raise exceptions.InvalidPropertiesException(
                        f'Duplicate capture group names found: "{group}"'
                    )
        else:
            unnamed_split = regex_and_group.split(":", 1)
            if len(unnamed_split) < 2:
                logger.debug(
                    'File at "%s" could not be matched by regex "%s" '
                    "and will be skipped",
                    full_path,
                    regex_and_group,
                )
                continue
            group, regex = unnamed_split
            unnamed_match = re.match(
                regex, full_path if use_full_path else os.path.basename(full_path)
            )
            if unnamed_match:
                if group not in captured_properties:
                    captured_properties[group] = unnamed_match.group(1)
                else:
                    raise exceptions.InvalidPropertiesException(
                        f'Duplicate capture group names found: "{group}"'
                    )
    return captured_properties


def collect_files(
    dir_path: str,
    include_folders: bool,
    entire_path: bool,
    recursive: bool,
    regex_groups: list[str],
):
    collected = {}
    pkeys = set()
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            if include_folders:
                collected[full_path] = matcher(full_path, entire_path, regex_groups)
                pkeys.update(collected[full_path])
            if recursive:
                collected = collected | collect_files(
                    full_path, include_folders, entire_path, recursive, regex_groups
                )
        elif os.path.isfile(full_path):
            collected[full_path] = matcher(full_path, entire_path, regex_groups)
            pkeys.update(collected[full_path])
    return collected, pkeys


def write_collected_to_csv(
    output_path: str,
    collected: dict[str, dict[str, str]],
    property_keys: Iterable[str],
    output_basename: bool,
):
    with open(output_path, "w") as output_fd:
        s_property_keys = sorted(property_keys)
        header = ["path"]
        if output_basename:
            header.append("basename")
        header.extend(s_property_keys)
        writer = csv.writer(output_fd)
        writer.writerow(header)
        for full_path, properties in collected.items():
            row = [full_path]
            if output_basename:
                row.append(os.path.basename(full_path))
            row.extend(
                (properties[k] if k in properties else "N/A" for k in s_property_keys)
            )
            writer.writerow(row)
