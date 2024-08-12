#! /bin/env python3
import xml.etree.ElementTree as ET


def print_element(element, output = None):
   
    print(f"<pre>", file = output)

    for key, value in element.attrib.items():
        print(f"{key}: {value}", file = output)
    
    if element.text is not None:
        if content := element.text.strip():
            print(f"text: \n{content}", file = output)

    print(f"</pre>", file = output)

def print_testsuite_pie_chart(testsuite, output = None):

    chart_data = {
        "failed": int(testsuite.attrib.get("failures", 0)),
        "error": int(testsuite.attrib.get("errors", 0)),
        "skipped": int(testsuite.attrib.get("skipped", 0)),
    }

    chart_data["pass"] = int(testsuite.attrib.get("tests",0)) - chart_data["failed"] - chart_data["error"] - chart_data["skipped"]

    print("```mermaid", file=output)

    # theme colors in order: pass, failed, error, skipped
    print("%%{init: {'theme': 'base', 'themeVariables': { 'pie1': '#0f0', 'pie2': '#f00', 'pie3': '#fa0', 'pie4': '#ff0'}}}%%", file=output)

    print(f"pie title {testsuite.attrib['name']} Results", file=output)
    for key, value in chart_data.items():
        print(f'"{key}" : {value}', file=output)

    print("```", file=output)


def print_testsuite_report(testsuite, output = None):

    print_testsuite_pie_chart(testsuite, output)

    for testcase in testsuite.findall('testcase'):

        print("<details>", file=output)
        test_name = testcase.attrib['name'].replace('_', ' ').title()
        test_class =  testcase.attrib['classname']
        print(f"<summary>{test_name} - {test_class}</summary>", file=output)

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
        print_testsuite_report(testsuite, output=sys.stdout)

