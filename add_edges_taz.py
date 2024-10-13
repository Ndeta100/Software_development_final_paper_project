import sumolib

net = sumolib.net.readNet('tallinn.net.xml')
edges = net.getEdges()

with open("edges_list.txt", "w") as file:
    for edge in edges:
        file.write(f"{edge.getID()}\n")
