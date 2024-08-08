#!/usr/bin/env python3

import yaml
import os
import argparse
import json

# TODO: 
# - rename to something more descriptive
# - refactor and add testing


parser = argparse.ArgumentParser()

parser.add_argument(
    "--rockfile-directory",
    help="Path where to directory containing rockcraft.yaml",
    required=True,
)
args = parser.parse_args()

BUILD_WITH_LPCI = 0

with open(f"{args.rockfile_directory}/rockcraft.yaml") as rf:
    rockcraft_yaml = yaml.safe_load(rf)

platforms = rockcraft_yaml["platforms"]

target_archs = []
for platf, values in platforms.items():
    if isinstance(values, dict) and "build-for" in values:
        target_archs += list(values["build-for"])
        continue
    target_archs.append(platf)

print(f"Target architectures: {set(target_archs)}")

matrix = {"include": []}
gh_supported_archs = {"amd64": "ubuntu-22.04", "arm64": "Ubuntu_ARM64_4C_16G_01"}
if set(target_archs) - set(gh_supported_archs.keys()):
    # Then there are other target archs, so we need to build in LP
    matrix["include"].append(
    {"architecture": "-".join(set(target_archs)), "runner": gh_supported_archs["amd64"]}
    )
    BUILD_WITH_LPCI = 1
else:
    for runner_arch, runner_name in gh_supported_archs.items():
        if runner_arch in target_archs:
            matrix["include"].append(
            {"architecture": runner_arch, "runner": runner_name}
            )
matrix_json = json.dumps(matrix)
with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
    print(f"build-for={matrix_json}", file=gh_out)
    print(f"build-with-lpci={BUILD_WITH_LPCI}", file=gh_out)