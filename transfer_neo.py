from neo4j import GraphDatabase

URI_LOCAL = "bolt://localhost:7687"
DRIVER_LOCAL = GraphDatabase.driver(URI_LOCAL, auth=("neo4j", "12345"))

# replace with bolt endpoint address here
URI_REMOTE = "bolt://XXX:XXX"
DRIVER_REMOTE = GraphDatabase.driver(URI_REMOTE, auth=("neo4j", "XXX"))

KEYS = {
    "Hashtag": "tag",
    "Source": "name",
    "User": "user_key",
    "Tweet": "id",
    "URL": "expanded_url"}

def set_node_visited(node_name, visited):
    with DRIVER_REMOTE.session() as remote_session:
        remote_session.run(
            "CALL apoc.periodic.iterate('MATCH (p:{node}) RETURN p', 'SET p.visited = {visited}', {{batchSize:10000, parallel:true}})"
            .format(node=node_name, visited=visited))

def set_relationship_visited(relationship_name, visited):
    with DRIVER_REMOTE.session() as remote_session:
        remote_session.run(
            "CALL apoc.periodic.iterate('MATCH ()-[r:{relationship}]-() RETURN r', 'SET r.visited = {visited}', {{batchSize:10000, parallel:true}})"
            .format(relationship=relationship_name, visited=visited))


def load_node(node_name):
    with DRIVER_REMOTE.session() as remote_session:
        set_node_visited(node_name, 0)

        with DRIVER_LOCAL.session() as local_session:
            def prepare(val):
                if isinstance(val, int):
                    return "{}".format(val)
                return "\"" + val.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r") + "\""
            
            finished = False
            batch_number = 0

            while not finished:
                finished = True
                batch_number += 1
                print("Batch {}".format(batch_number))

                for record in remote_session.run("MATCH (n: {} {{visited: 0}}) SET n.visited = 1 RETURN n LIMIT 1000".format(node_name)):
                    finished = False
                    item = record["n"]
                    keys = item.keys()
                    good_keys = filter(lambda k, item=item: item[k] is not None and k != "visited", keys)
                    param_string = ", ".join(map(lambda k, item=item: k + ": " "{}".format(prepare(item[k])), good_keys))
                    query = "CREATE " + "(:{}".format(":".join(item.labels)) +  " { " + param_string + " })"
                    local_session.write_transaction(lambda tx, query=query: tx.run(query))

        set_node_visited(node_name, 0)

def load_relations(node_from_name, node_from_key, node_to_name, node_to_key, relationship_name):
    with DRIVER_REMOTE.session() as remote_session:
        set_relationship_visited(relationship_name, 0)

        with DRIVER_LOCAL.session() as local_session:

            finished = False
            batch_number = 0

            while not finished:
                finished = True
                batch_number += 1
                print("Batch {}".format(batch_number))

                for record in remote_session.run(
                        "MATCH (n:{f})-[r:{r} {{visited:0}}]->(m: {t}) SET r.visited = 1 RETURN n.{kf} as n, m.{kt} as m LIMIT 1000"
                        .format(f=node_from_name, r=relationship_name, t=node_to_name, kf=node_from_key, kt=node_to_key)):
                    finished = False

                    from_remote = record["n"].replace("\"", "\\\"")
                    to_remote = record["m"].replace("\"", "\\\"")

                    query = "MATCH (n:{f} {{ {kf}: \"{kfv}\" }}), (m:{t} {{ {kt}: \"{ktv}\" }}) MERGE (n)-[:{rn}]->(m)".format(
                        f=node_from_name, t=node_to_name, kf=node_from_key, kt=node_to_key, kfv=from_remote, ktv=to_remote, rn=relationship_name)
                    local_session.write_transaction(lambda tx, query=query: tx.run(query))

        set_relationship_visited(relationship_name, 0)

def load_relations_auto(node_from_name, node_to_name, relationship_name):
    load_relations(node_from_name, KEYS[node_from_name], node_to_name, KEYS[node_to_name], relationship_name)

load_node("Tweet")
load_node("User")
load_node("Hashtag")
load_node("Source")
load_node("URL")

load_relations_auto("Tweet", "Hashtag", "HAS_TAG")
load_relations_auto("Tweet", "Tweet", "IN_REPLY_TO")
load_relations_auto("Tweet", "User", "MENTIONS")
load_relations_auto("User", "Tweet", "POSTED")
load_relations_auto("Tweet", "Tweet", "RETWEETED")
load_relations_auto("Tweet", "URL", "HAS_LINK")
load_relations_auto("Tweet", "Source", "POSTED_VIA")
