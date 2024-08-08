#!/usr/bin/env python3

import yaml
import os
import argparse
import json

# TODO: 
# - rename to something more descriptive
# - refactor and add testing

GH_SUPPORTED_ARCHS = {"amd64": "ubuntu-22.04", "arm64": "Ubuntu_ARM64_4C_16G_01"}

parser = argparse.ArgumentParser()

parser.add_argument(
    "--rockfile-directory",
    help="Path where to directory containing rockcraft.yaml",
    required=True,
)
args = parser.parse_args()

with open(f"{args.rockfile_directory}/rockcraft.yaml") as rf:
    rockcraft_yaml = yaml.safe_load(rf)

rock_platforms = rockcraft_yaml["platforms"]
rock_name = rockcraft_yaml["name"]

target_archs = []
for platf, values in rock_platforms.items():
    if isinstance(values, dict) and "build-for" in values:
        target_archs += list(values["build-for"])
        continue
    target_archs.append(platf)

runner_build_matrix = {"include": []}
lpci_build_matrix = {"include": []}

# TODO: is there a reason we cannot build on both systems
if set(target_archs) - set(GH_SUPPORTED_ARCHS.keys()):
    # Then there are other target archs, so we need to build in LP
    lpci_build_matrix["include"].append(
    {"architecture": "-".join(set(target_archs))}
    )
else:
    for runner_arch, runner_name in GH_SUPPORTED_ARCHS.items():
        if runner_arch in target_archs:
            runner_build_matrix["include"].append(
            {"architecture": runner_arch, "runner": runner_name}
            )

with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
    print(f"rock-name={rock_name}", file=gh_out)
    print(f"runner-build-matrix={json.dumps(runner_build_matrix)}", file=gh_out)
    print(f"lpci-build-matrix={json.dumps(lpci_build_matrix)}", file=gh_out)