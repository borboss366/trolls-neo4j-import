# at first install the neo4j connect module
import csv
import re
from typing import Optional
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
DRIVER = GraphDatabase.driver(URI, auth=("neo4j", "12345"))

# def print_friends_of(tx, name):
#  for record in tx.run("MATCH (a:Person)-[:KNOWS]->(f) "
#                        "WHERE a.name = {name} "
#                        "RETURN f.name", name=name):
#      print(record["f.name"])


# Delete all the stuff
# MATCH (n) DETACH DELETE n

def get_node_name(file_name) -> Optional[str]:
    match = re.search("node_([a-zA-Z]+)[.]csv", file_name)

    if match is None:
        return None

    return match.group(1)

def load_csv_node(file_name):
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
                params = dict(zip(fields, row))
                param_string = ", ".join("{k}: {v}".format(k=k, v=v if isinstance(v, int) else "\"" + v + "\"") for (k, v) in params.items())
                param_string = "{" + param_string + "}"
                print(param_string)
                session.run("MERGE (node:{node_name} {param_string})".format(node_name=node_name, param_string=param_string))

            csvfile.close()

        session.close()

load_csv_node("dump/node_Hashtag.csv")
