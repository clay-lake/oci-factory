#!/usr/bin/env python3

import pytest
import generate_matrix
from tempfile import TemporaryDirectory
from pathlib import Path


def test_get_target_archs():

    project = {
        "name": "hello)",
        "title": "Hello World",
        "summary": "An Hello World rock",
        "description": "This is just an example of a Rockcraft project\nfor a Hello World rock.\n",
        "version": "latest",
        "base": "bare",
        "build-base": "ubuntu@22.04",
        "license": "Apache-2.0",
        "run-user": "_daemon_",
        "environment": {"FOO": "bar"},
        "services": {
            "hello": {
                "override": "replace",
                "command": "/usr/bin/hello -t",
                "environment": {"VAR1": "value", "VAR2": "other value"},
            }
        },
        "platforms": {
            "amd64": None,
            "armhf": {"build-for": ["armhf", "arm64"]},
            "ibm": {"build-on": ["s390x"], "build-for": "s390x"},
        },
        "parts": {"hello": {"plugin": "nil", "stage-packages": ["hello"]}},
    }

    arches = generate_matrix.get_target_archs(project)
    assert arches == {"arm64", "armhf", "amd64"}


def test_configure_matrices():

    build_matrices = generate_matrix.configure_matrices(
        ["amd64"], {"amd64": "ubuntu-22.04"}, False
    )
    expected_result = {
        "runner-build-matrix": {
            "include": [{"architecture": "amd64", "runner": "ubuntu-22.04"}]
        },
        "lpci-build-matrix": {"include": []},
    }

    assert build_matrices == expected_result


def test_configure_matrices_fallback_exception():

    with pytest.raises(generate_matrix.MissingArchSupport):
        generate_matrix.configure_matrices(
            ["arm64"], {"amd64": "ubuntu-22.04"}, False
        )


def test_configure_matrices_lcpi_fallback():

    build_matrices = generate_matrix.configure_matrices(
        ["arm64"], {"amd64": "ubuntu-22.04"}, True
    )
    expected_result = {
        'runner-build-matrix': {'include': []},
        'lpci-build-matrix': {'include': [{'architecture': 'arm64'}]}
    }

    assert build_matrices == expected_result



def test_set_build_config_outputs():

    test_build_matrices = {
        "runner-build-matrix": {
            "include": [{"architecture": "amd64", "runner": "ubuntu-22.04"}]
        },
        "lpci-build-matrix": {"include": []},
    }

    with TemporaryDirectory() as tmp:

        env_path = Path(tmp) / "env"

        generate_matrix.set_build_config_outputs("test", test_build_matrices, output_file=env_path)

        with open(env_path, 'r') as fh:
            gh_output = fh.read()


    expected_result = """rock-name=test
runner-build-matrix={"include": [{"architecture": "amd64", "runner": "ubuntu-22.04"}]}
lpci-build-matrix={"include": []}
"""

    assert gh_output == expected_result