import xml.etree.ElementTree as ET
import os.path
from pathlib import Path
import pydotplus
from graphviz import Digraph

globalPath = 'd:\\Projects\\Scripts\\XMLFlow\\test_env'
iterPath = 'Some\\Initial\\Path'
xmlFileName = 'Data.xml'
dotFileName = 'xml.dot'
resourceList = []

dot = Digraph(name=iterPath)
tree = ET.parse(os.path.join(globalPath, iterPath, xmlFileName))


def pathFinder(root):

    for child in root.iter('Resource'):
        print(child.attrib)
        # TODO: Address the value instead of the tuple
        # dot.node(child.attrib)
        resourceList.append(child.attrib)

    for child in root.iter('Dependency'):
        print(child.attrib)
        iterPath = Path(os.path.join(
            globalPath, child.attrib['name'], xmlFileName))
        print(iterPath)

        # Check if path and/or file are valid
        # TODO: Figure out what actually is missing (file, dir)
        if os.path.exists(iterPath) is False:
            if os.path.isdir(iterPath):
                print("Path not existing:")
                print(os.path.dirname(iterPath))
                continue
            elif os.path.isfile(iterPath):
                print("File not existing:")
                print(os.path.basename(iterPath))
                continue
            else:
                print('Something else.')
                continue

        tree = ET.parse(iterPath)
        newroot = tree.getroot()
        pathFinder(newroot)


if __name__ == '__main__':
    dot.node(iterPath)  # Create root node
    root = tree.getroot()

    pathFinder(root)  # Initialize crawler

    print(dot.source)
    dot.render('xmlgraph.gv', view=True)
