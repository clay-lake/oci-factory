#! /usr/bin/env python3

import configure
from tempfile import TemporaryDirectory
from pathlib import Path


def test_set_report_name():

    suffix = "vulnerability-report.json"
    name = "example"
    result = configure.set_report_name(name, suffix)

    assert isinstance(result, dict), "Check return type"
    assert "report-name" in result, "Check output name"

    assert result["report-name"].find(suffix) >= 0, "result does not contain suffix"
    assert result["report-name"].find(name) >= 0, "result does not contain name"


def set_trivyignore_exists(archive_dir: str):

    with TemporaryDirectory() as tmp:

        trivyignore_path = Path(tmp) / ".trivyignore"
        trivyignore_path.touch()

        result = configure.set_trivyignore(tmp)

        assert isinstance(result, dict), "Check return type"
        assert "trivyignore-path" in result, "Check output name"

        assert result["trivyignore-path"] == trivyignore_path, "result path is invalid"


def set_trivyignore_does_not_exists(archive_dir: str):

    with TemporaryDirectory() as tmp:

        trivyignore_path = Path(tmp) / ".trivyignore"

        result = configure.set_trivyignore(tmp)

        assert isinstance(result, dict), "Check return type"
        assert "trivyignore-path" in result, "Check output name"

        assert result["trivyignore-path"] == trivyignore_path, "result path is invalid"


def test_set_github_output():

    output_dict = {
        "hello": "world",
        "foo": "bar",
    }

    with TemporaryDirectory() as tmp:

        env_path = Path(tmp) / "env"

        configure.set_github_output(output_dict, output_file=env_path)

        with open(env_path, "r") as fh:
            gh_output = fh.read()

    expected_result = """hello=world
foo=bar
"""
    assert gh_output == expected_result
