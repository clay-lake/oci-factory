import subprocess as sub
from pathlib import Path
from string import Template

# Usage:
# python3 call_graph.py | dot -Tpng > output.png

# root that all callee nodes will be found in
PROJ_PATH = Path(__file__).parent

CALLER_NODE_SEARCH_DIR = [
    PROJ_PATH/Path(".github/workflows"),
    PROJ_PATH/Path("src"),
    ]

# File Types of Interest. ignore files not of these types
FTOI = [".py", ".sh", ".go", ".yml", ".yaml"] 

# graph template, adjust global style here
GRAPH_TEMPLATE= Template("""
digraph packages {
rankdir=LR
$body
}
""")
"""
concentrate=true;
size="30,40";
"""

def search_in_files(pattern, root=PROJ_PATH):
    """Find matches of pattern in all files recursively from root"""
    grep_output = sub.check_output(["grep", "-l", "-r", pattern, str(root)]).decode("utf-8")
    results = [Path(line) for line in grep_output.splitlines()]

    return results

# find all files in CALLER_NODE_SEARCH_DIR that are FTOI
caller_node_paths = [cnp for cnsd in CALLER_NODE_SEARCH_DIR \
                     for cnp in cnsd.rglob("*") \
                        if cnp.is_file() and cnp.suffix in FTOI]

graph = [] # inserted into body of dotty template 
for cnp in caller_node_paths:
    node_A_name = cnp.name

    # create edges (and non existent nodes) for all matches in PROJ_PATH
    for match_path in search_in_files(node_A_name):
        node_B_name = match_path.name
        
        # exclude edges if ...
        if match_path == node_A_name \
            or not Path(match_path).suffix in FTOI:
            continue

        # append edge to graph
        graph.append(f'"{node_B_name}" -> "{node_A_name}"')

    # TODO: create edges for callee nodes that exclude suffix 


print(GRAPH_TEMPLATE.substitute(body="\n".join(graph)))