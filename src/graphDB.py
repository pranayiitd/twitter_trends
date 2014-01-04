#!/usr/bin/env python

"""
Simple example showing node and relationship creation plus
execution of Cypher queries

"""

from __future__ import print_function
# Insert followers as nodes in the graph and make relationship

def insertFollowers(followers):
	# Import Neo4j modules
	from py2neo import neo4j, cypher

	# Attach to the graph db instance
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	followers = [{"name":"Alice","number":1},{"name": "Bob","number":2}]

	# Create two nodes
	# nodes= graph_db.create(followers)
	
	nodes = graph_db.create(*[
    {
        "number": i,
        "name": followers[0]["name"]
    }
    for i in range(len(followers))
	])

	print(nodes,"\n")
	# Join the nodes with a relationship
	# rel_ab = node_a.create_relationship_to(node_b, "KNOWS")

	# # Build a Cypher query
	# query = "START a=node({A}) MATCH a-[:KNOWS]->b RETURN a,b"

	# # Define a row handler...
	# def print_row(row):
	#     a, b = row
	#     print(a["name"] + " knows " + b["name"])

	# # ...and execute the query
	# cypher.execute(graph_db, query, {"A": node_a.id}, row_handler=print_row)

insertFollowers("11")	