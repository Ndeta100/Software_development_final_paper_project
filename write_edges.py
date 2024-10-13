import random

# Load all edges from the file
with open("edges_list.txt") as f:
    edges = f.read().splitlines()

# Select a random sample of 100 edges
selected_edges = random.sample(edges, 100)

# Write the TAZ file
with open("tazfile.xml", "w") as f:
    f.write("<tazs>\n")
    f.write('  <taz id="taz_1" edges="{}"/>\n'.format(" ".join(selected_edges)))
    f.write("</tazs>\n")
