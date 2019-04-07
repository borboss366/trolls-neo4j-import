import csv
import re
from typing import Optional
from neo4j import GraphDatabase
import common_parse

URI = "bolt://localhost:7687"
DRIVER = GraphDatabase.driver(URI, auth=("neo4j", "12345"))

def get_node_name(file_name) -> Optional[str]:
    match = re.search("node_([a-zA-Z]+)[.]csv", file_name)

    if match is None:
        return None

    return match.group(1)

def load_csv_node(file_name):
    def replace_weird(val):
        if isinstance(val, int):
            return val

        return val.replace(common_parse.WEIRD_CHAR, '\n')

    node_name = get_node_name(file_name)

    if node_name is None:
        print("Could not parse node name from " + file_name)
        return

    with DRIVER.session() as session:
        with open(file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            print("Loading the node " + node_name + ", fields " + ", ".join(fields))

            for row in csvreader:
                row = map(replace_weird, row)
                params = dict(zip(fields, row))
                param_string = ", ".join("{k}: {v}".format(k=k, v=v if isinstance(v, int) else "\"" + v + "\"") for (k, v) in params.items())
                param_string = "{" + param_string + "}"
                print(param_string)
                session.run("MERGE (node:{node_name} {param_string})".format(node_name=node_name, param_string=param_string))

            csvfile.close()

        session.close()

load_csv_node("dump/node_User.csv")
load_csv_node("dump/node_Hashtag.csv")
load_csv_node("dump/node_Troll.csv")
load_csv_node("dump/node_Tweet.csv")
load_csv_node("dump/node_URL.csv")
load_csv_node("dump/node_Source.csv")
