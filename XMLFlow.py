import xml.etree.ElementTree as ET
import os.path
from pathlib import Path
import pydotplus

globalPath = 'd:\\Projects\\Scripts\\XMLParser'
iterPath = 'Some\\Initial\\Path'
xmlFileName = 'Data.xml'
dotFileName = 'xml.dot'
resourceList = []

graph = pydotplus.Dot(graph_type='digraph', strict=False)
graph.set_graphviz_executables(
    {'dot': 'c:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe'})
tree = ET.parse(os.path.join(globalPath, iterPath, xmlFileName))


def pathFinder(root):

    for child in root.iter('Resource'):
        print(child.attrib)
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
    graph.add_node(pydotplus.Node(iterPath))  # Create root node
    root = tree.getroot()

    pathFinder(root)  # Initialize crawler

    # Write file
    gWrite = graph.write_dot(os.path.join(globalPath, dotFileName))
    gCreate = graph.create(prog='dot', format='dot')
    if gWrite:
        print('-- ' + dotFileName + ' written successfully!')
