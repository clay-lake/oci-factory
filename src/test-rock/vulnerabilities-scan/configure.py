#! /bin/env python3

from pathlib import Path
import os
import logging
import argparse



def set_report_name(archive_name: str, report_suffix:str = "json") -> dict:
    """Format a report-name output using a specified report_suffix."""
    outputs = {"report-name": f"{archive_name}.{report_suffix}"}
    return outputs


def set_trivyignore(archive_dir: str):
    """Set the trivyignore-path output. Touch the trivyignore-path if non existant."""

    trivyignore_path = Path(archive_dir) / ".trivyignore"
    
    # TODO: confirm that this is a required behaviors, then add a test for it
    if not trivyignore_path.exists():
        logging.info(f"No {trivyignore_path.name} found at {trivyignore_path.parent}. Writing empty {trivyignore_path.name}")
        trivyignore_path.touch()

    outputs = {"trivyignore-path": str(trivyignore_path)}
    return outputs


def set_github_output(outputs: dict, output_file = None):
    """Generically convert a dictionary to Github step outputs."""

    if output_file is None:
        output_file = os.environ["GITHUB_OUTPUT"]

    # TODO: move to generic helper module for oci-factory
    # Note: currently only handles setting strings in GITHUB_OUTPUT
    with open(output_file, "a") as fh:
        for key, value in outputs.items():
            print(f"{key}={value}", file=fh)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--archive-name",
        help="Name of archive to configure scan for.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--archive-dir",
        help="Directory of archive to configure scan for.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--report-suffix",
        help="Suffix of Vulnerability report.",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    outputs = dict()

    outputs.update(
        set_report_name(args.archive_name, args.report_suffix)
        )
    
    outputs.update(
        set_trivyignore(args.archive_dir)
        )
    
    set_github_output(outputs)

