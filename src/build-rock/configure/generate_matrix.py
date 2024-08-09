#!/usr/bin/env python3

import yaml
import os
import argparse
import json
from enum import Enum
from typing import Optional

# TODO:
# - rename to something more descriptive
# - add support for compiling. i.e. build-on and build-for
# - do we have a rockcraft files validator?
# - make data classes for building matrices


class MATRIX_NAMES(Enum):
    RUNNER = "runner_build_matrix"
    LPCI = "lpci_build_matrix"


class MissingArchSupport(Exception):
    pass


def get_target_archs(rockcraft: dict) -> list:
    """get list of target architectures from rockcraft project definition"""

    rock_platforms = rockcraft["platforms"]

    target_archs = set()

    for platf, values in rock_platforms.items():
        
        if isinstance(values, dict) and "build-for" in values:
            if isinstance(arches := values["build-for"], list):
                target_archs.update(arches)
            elif isinstance(values, str):
                target_archs.add(arches)
        else:
            target_archs.add(platf)

    return target_archs


def configure_matrices(
    target_archs: list, runner_config: dict, lp_fallback: bool
) -> dict:
    """Sort build into appropriate build matrices"""

    # map configuration to individual job matrices
    build_matrices = {name.value: {"include": []} for name in MATRIX_NAMES}

    # Check if we have runners for all supported architectures
    if missing_archs := set(target_archs) - set(runner_config.keys()):

        # raise exception if we cannot fallback to LP builds
        if not lp_fallback:
            raise MissingArchSupport(
                f"Missing support for runner arches: {missing_archs}"
            )

        # configure LP build
        build_matrices[MATRIX_NAMES.LPCI.value]["include"].append(
            {"architecture": "-".join(set(target_archs))}
        )

    else:
        # configure runner matrix for list of supported runners
        for runner_arch, runner_name in runner_config.items():
            if runner_arch in target_archs:
                build_matrices[MATRIX_NAMES.RUNNER.value]["include"].append(
                    {"architecture": runner_arch, "runner": runner_name}
                )

    return build_matrices


def set_build_config_outputs(rock_name: str, build_matrices: dict, output_file: Optional[str] = None):
    """Update GITHUB_OUTPUT with build configuration"""

    # set default when not testing
    if output_file is None:
        output_file = os.environ["GITHUB_OUTPUT"]

    with open(output_file, "a") as fh:

        print(f"rock-name={rock_name}", file=fh)

        for name, matrix in build_matrices.items():
            print(f"{name}={json.dumps(matrix)}", file=fh)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--rockfile-directory",
        help="Path where to directory containing rockcraft.yaml",
        required=True,
    )

    parser.add_argument(
        "--lpci-fallback",
        help="revert to lpci if architectures are not supported",
        action="store_true",
        required=True,
    )

    parser.add_argument(
        "--runner-config",
        help="revert to lpci if architectures are not supported",
        default='{"amd64": "ubuntu-latest"}',
    )

    args = parser.parse_args()

    # get configuration form rockcraft yaml
    with open(f"{args.rockfile_directory}/rockcraft.yaml") as rf:
        rockcraft_yaml = yaml.safe_load(rf)

    # load runner config
    runner_config = json.loads(args.runner_config)

    rock_name = rockcraft_yaml["name"]

    target_archs = get_target_archs(runner_config)

    build_matrices = configure_matrices(target_archs)

    set_build_config_outputs(rockcraft_yaml["name"], build_matrices)
