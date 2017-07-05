# Neo4j python driver download URL: https://anaconda.org/conda-forge/neo4j-python-driver
# conda install -c conda-forge neo4j-python-driver=1.3.1 

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os
import os.path as path
import sys
import neo4j.v1

def get_country(tx):
    for record in tx.run("MATCH (n:Country) RETURN n.name LIMIT 100"):
    	print record["n.name"]

authFilepath = "../../API_Database_file/neo4j_auth"

admin = "" 
psw = ""

with open(authFilepath, 'r') as f:
    admin, psw = f.read().split()


driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth(admin, psw), encrypted=True)
with driver.session() as session:
	session.read_transaction(get_country)

print dir(neo4j.v1)