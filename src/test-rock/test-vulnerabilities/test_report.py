#! /bin/env python3

from datetime import datetime
import report


def test_parse_iso_date():

    expected = datetime.fromisoformat("2021-05-26T10:14:00+00:00")
    result = report.parse_iso_date("2021-05-26T10:14:00Z")

    assert expected == result, "Zulu designation should be replace with UTC+00:00"


def test_parse_iso_date_non_utc():

    expected = datetime.fromisoformat("2021-05-26T10:14:00+00:00")
    result = report.parse_iso_date("2021-05-26T10:14:00+00:00")

    assert expected == result, "Date time objects should match exactly"


def test_Vulnerability_class():

    expected_row = "|Severity|Target|Class|VulnerabilityID|PkgName||"
    vln = report.Vulnerability(
        "Severity", "Target", "Class", "VulnerabilityID", "PkgName", None
    )

    header = vln.get_header()

    assert (
        len(header.splitlines()) == 2
    ), "Should be 2 lines, header row and a separator"

    row = vln.get_row()

    assert row == expected_row, "Row formatting changed"


def test_vuln_key():

    time_stamp = "2021-05-26T10:14:00Z"
    vln = report.Vulnerability(
        "Severity", "Target", "Class", "VulnerabilityID", "PkgName", time_stamp
    )

    result = report.vuln_key(vln)

    assert result[0] == report.parse_iso_date(
        time_stamp
    ), "Sort key should start with date"
