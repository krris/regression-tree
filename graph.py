# -*- coding: utf-8 -*-
"""
Example usage of pydot.
"""
import pydot 

# create a new graph
graph = pydot.Dot(graph_type='graph')

for i in range(2):
    # the pydot.Edge() constructor receives two parameters, a source node and a destination
    # node, they are just strings like you can see
    edge = pydot.Edge("root", "first_level%d" % i, label="label")
    # to add the edge to our graph
    graph.add_edge(edge)

# now let us add some vassals
node_num= 0
for i in range(2):
    # create another two nodes for prevoius node
    for j in range(2):
        edge = pydot.Edge("first_level%d" % i, "second_level%d" % node_num)
        graph.add_edge(edge)
        node_num += 1

# let's save our graph into a file
graph.write_png('graph.png')
