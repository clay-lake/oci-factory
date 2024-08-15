#! /bin/env python3

from pathlib import Path
import os
import logging
import argparse
import json
from pprint import pprint # TODO: Delete me
from dataclasses import dataclass
from datetime import datetime
import re

# TODO:
# - add severity markers for table
# - add notification interface

@dataclass
class Vulnerability:
    # Note, these should be ordered
    severity: str
    target: str
    class_name: str
    id: str
    package_name: str
    last_modified: str

    @classmethod
    def get_fields(cls):
        fields = list(cls.__dataclass_fields__.keys())
        return fields
    
    def get_row(self):
        row = self.format_row([getattr(self, f, "") for f in self.get_fields()])
        return row
    
    @classmethod
    def get_header(cls, header_break = "--:", line_break = "\n"):
        # --: should align right
        fields = cls.get_fields()
        header_lines = [
            cls.format_row(fields),
            cls.format_row([header_break for f in fields])
        ] 
        row = line_break.join(header_lines)
        return row

    @staticmethod
    def format_row(row, separator: str = "|"):
        row_cells = [str(f) if f is not None else "" for f in row]
        formatted =  separator + separator.join(row_cells) + separator

        return formatted


def parse_iso_date(date: str):
    """Earlier versions of Python reject Zulu time"""
    time_str = re.sub('Z$', '+00:00', date) 

    date_obj = datetime.fromisoformat(time_str)
    return date_obj

def vuln_key(vuln):
    # Possible improvement, sort by severity as well as date
    # make timestamp compliant for older python versions
    date_key = parse_iso_date(vuln.last_modified)

    return date_key,

def process_report(report, last_scan, output_file = None):

    # scan json cosign-vuln for vulnerabilities 
    vulnerabilities = list()

    for result in report["scanner"]["result"]["Results"]: # .scanner.result.Results[]

        if "Vulnerabilities" in result: # there may be no Vulnerabilities
            for vln in result["Vulnerabilities"]:
                
                vulnerabilities.append(
                    Vulnerability(
                        vln.get("Severity"),
                        result.get("Target"),
                        result.get("Class"),
                        vln.get("VulnerabilityID"),
                        vln.get("PkgName"),
                        vln.get("LastModifiedDate")
                        )
                    )
            

    if vulnerabilities:

        vulnerabilities_sorted = sorted(vulnerabilities, key=vuln_key, reverse=True)

        if last_scan is not None:
            new_vulnerabilities = list(
                    filter(
                        lambda v: v.last_modified > last_scan, 
                        vulnerabilities_sorted
                        )
                    )

            print(f"**{len(new_vulnerabilities)} new vulnerabilities found since {last_scan.isoformat()}**", file=output_file)
        
        # print table of vulnerabilities 
        print(Vulnerability.get_header(), file=output_file)
        for row in vulnerabilities_sorted:
            print(row.get_row(), file=output_file)

    else:
        print(f"**No vulnerabilities found!**", file=output_file)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--report-path",
        help="Path to cosign-vuln json report.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--last-scan",
        help="Timestamp of last scan in ISO-8601 format.",
        type=str,
        required=False,
    )


    args = parser.parse_args()
    
    with open(args.report_path, 'r') as fh:
        report = json.load(fh)

    last_scan = parse_iso_date(args.last_scan) if args.last_scan is not None else None

    process_report(report, last_scan)
