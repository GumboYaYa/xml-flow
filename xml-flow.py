import xml.etree.ElementTree as ET
import os
import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
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
    root = root[29:] # TODO: Synchronizing the paths in both dataframes
    # print(root_short)
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

################################
# Build file structure         #
################################

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

################################
# Build XML structure          #
################################

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
            source.append("Data" + file[len(globalPath) :])
            target.append(item.attrib.get(attr)) #TODO: Convert \ to /
            link.append(tag)

    return {"Source": source, "Target": target, "Link": link}


xmls = get_files(globalPath, "xml")

d_dpdy = get_data(xmls, "Dependency", "name")
d_rsrc = get_data(xmls, "Resource", "name")

df = pd.DataFrame(data=d_dpdy)

print(df.iloc[0, :])

for i, col in df.iterrows():
    G.add_edge(col[0], col[1], attr_dict=col[2:].to_dict())



# G.graph["graph"] = {'rankdir': 'TD'}
G.graph["node"] = {"shape": "box"}

A = nx.nx_agraph.to_agraph(G)
A.layout("fdp")
A.draw("filegraph.png")
