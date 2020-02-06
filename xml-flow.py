import xml.etree.ElementTree as ET
import os
import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import pylab as plt
import pygraphviz as pgv


# globalPath = '/home/tom/PycharmProjects/XMLFlow/test_env'
globalPath = "/home/tom/Projects/Scripting/Data"
source = []
target = []
link = []


# Build a base for the file structure to be translated into a dataframe
directories = []
contents = []
types = []

for root, dirs, files in os.walk(globalPath):
    for d in dirs:
        directories.append(root)
        contents.append(os.path.join(root, d))
        types.append("Directory")
    for f in files:
        directories.append(root)
        contents.append(os.path.join(root, f))
        types.append("File")


# Dictionary to be imported into Pandas
d_tree = {"Directory": directories, "Content": contents, "Type": types}

df_tree = pd.DataFrame(data=d_tree)
df_tree = df_tree.iloc[0:100, :]
print(df_tree)


G = nx.DiGraph()

root_node = df_tree.iloc[0, 0]
G.add_node(root_node, rank=0, shape="box", label=root_node.split("/").pop())

for i, col in df_tree.iterrows():

    # Create edges
    G.add_edge(col[0], col[1], attr_dict=col[2:].to_dict())

    # Create nodes
    node_label = col[1].split("/").pop()

    def style(directory, file):
        if col[2] == "Directory":
            return directory
        else:
            return file

    G.add_node(
        col[1],
        label=node_label,
        style="filled",
        color=style("/brbg4/4", "/brbg4/1"),
        fillcolor=style("/brbg4/3", "/brbg4/2"),
    )

print(f"Number of edges: {G.number_of_edges()}")
print(f"Number of nodes: {G.number_of_nodes()}")

# G.graph["graph"] = {'rankdir': 'TD'}
G.graph["node"] = {"shape": "box"}

# G = nx.complete_graph(30)
A = nx.nx_agraph.to_agraph(G)
A.layout("fdp")
A.draw("filegraph.png")

# g = nx.complete_graph(20)
# A = to_agraph(g)
# A.layout('circo')
# A.draw('filegraph.png')


"""
def get_files(path, ext):
    lst = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("." + ext):
                lst.append(os.path.join(root, file))
    return lst


def get_data(files, tag, attr):
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        for item in root.iter(tag):
            source.append("." + file[len(globalPath) :])
            target.append(item.attrib.get(attr))
            link.append(tag)

    return {"Source": source, "Target": target, "Link": link}


xmls = get_files(globalPath, "xml")

d_dpdy = get_data(xmls, "Dependency", "name")
d_rsrc = get_data(xmls, "Resource", "name")

df = pd.DataFrame(data=d_dpdy)

print(df)

g = nx.DiGraph()

for i, col in df.iterrows():
    g.add_edge(col[0], col[1], attr_dict=col[2:].to_dict())

# node_color = []
# for i, col in df.iterrows():
#     if col[2] == 'Dependency':
#         node_color.append('orange')
#     else:
#         node_color.append('yellow')


print(f"Number of edges: {g.number_of_edges()}")
print(f"Number of nodes: {g.number_of_nodes()}")


# pyplot.figure(figsize=(8, 6))
# nx.draw(g, node_size=10, node_color='orange', edge_color='grey')
# pyplot.title('XML Map')
# pyplot.show()

# TODO: Works but needs better labeling
# TODO: Maybe first graph the file/folder tree itself, then connect files and folders accordingly
G = nx.gn_graph(300)
A = nx.nx_agraph.to_agraph(G)
# A.graph_attr["size"] = "8, 6"
A.draw("xmlgraph.png", prog="twopi")
"""
