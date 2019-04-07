import csv
import re
from typing import Optional
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
DRIVER = GraphDatabase.driver(URI, auth=("neo4j", "12345"))

