#! /bin/env python3

import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from io import StringIO

import format_markdown_report as report


@pytest.fixture
def sample_failure():

    sample_path = Path(__file__).parent / "data/sample_failure.xml"

    tree = ET.parse(sample_path)
    root = tree.getroot()
    return root


@pytest.fixture
def str_buff():

    with StringIO() as buffer:
        yield buffer


def test_print_junit_report_redirection(sample_failure, str_buff, capsys):

    report.print_junit_report(sample_failure, str_buff)
    report.print_junit_report(sample_failure, None)  # print to stdout

    str_buff.seek(0)
    str_buff_content = str_buff.read()

    captured = capsys.readouterr()
    stdout_content = captured.out

    assert stdout_content == str_buff_content, "printing to multiple locations"


def test_assert_false():

    assert False, "Hello World"


def test_assert_error():
    import notamodule