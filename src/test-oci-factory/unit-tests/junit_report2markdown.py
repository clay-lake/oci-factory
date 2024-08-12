#! /bin/env python3
import xml.etree.ElementTree as ET


def print_element(element, output = None):
    print("```", file=output)
    for key, value in element.attrib.items():
        print(f"{key}: {value}")
    
    if element.text is not None:
        if content := element.text.strip():
            print(f"text: \n{content}")

    print("```", file=output)


def print_result_pie_chart(root, output = None):

    chart_data = {
        "failed": int(root.attrib.get("failures", 0)),
        "error": int(root.attrib.get("errors", 0)),
        "skipped": int(root.attrib.get("skipped", 0)),
    }

    chart_data["pass"] = int(root.attrib.get("tests",0)) - chart_data["failed"] - chart_data["error"] - chart_data["skipped"]

    print("```mermaid", file=output)

    # theme colors in order: pass, failed, error, skipped
    print("%%{init: {'theme': 'base', 'themeVariables': { 'pie1': '#0f0', 'pie2': '#f00', 'pie3': '#fa0', 'pie4': '#ff0'}}}%%", file=output)

    print(f"pie title {root.attrib['name']} Results", file=output)
    for key, value in chart_data.items():
        print(f'"{key}" : {value}', file=output)

    print("```", file=output)


def markdown_report(root, output = None):

    print_result_pie_chart(root, output)

    for testcase in root.findall('testcase'):

        print("<details>", file=output)
        # print(f"<summary>{testcase.attrib['name']} - {testcase.attrib['classname']}</summary>", file=output)
        print(f"<summary>{testcase.attrib['name'].replace('_', ' ').title()}</summary>", file=output)

        print_element(testcase)
        
        for child in testcase.iter():
            print(child.tag)
            print_element(child)

        print("</details>", file=output)


if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-junit",
        help="Path to JUnit XML Report",
        required=True,
        type=str
    )

    args = parser.parse_args()


    tree = ET.parse(args.input_junit)
    root = tree.getroot()
    
    for testsuite in root.findall("testsuite"):
        markdown_report(testsuite, output=sys.stdout)

