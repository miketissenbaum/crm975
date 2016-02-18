from collections import Counter
import csv, json
import networkx as nx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph

f = csv.reader(open("productive-patterns-2.csv"))

bigrams = []
for line in f:
	bigrams.extend(zip(line,line[1:]))
print bigrams

outlinks = Counter()
counts = Counter()
for elt in bigrams:
    counts[elt] += 1
    outlinks[elt[0]] += 1
excludeBigrams = {}
for c in counts:
	if counts[c] < 2:
		excludeBigrams[c] = counts[c]

f = csv.reader(open("productive-patterns-2.csv"))

bigrams = []
for line in f:
	lineBigrams = zip(line, line[1:])
	excludeBool = 0
	for exclude in excludeBigrams:
		if exclude in lineBigrams:
			excludeBool = True
			break
	if not excludeBool:
		bigrams.extend(lineBigrams)

outlinks = Counter()
counts = Counter()
for elt in bigrams:
    counts[elt] += 1
    outlinks[elt[0]] += 1
mm = {elt: round(counts[elt]/float(outlinks[elt[0]]),2) for elt in counts}


writer = csv.writer(open('dict.csv', 'wb'))
for key, value in mm.items():
   writer.writerow([key, value])

G = nx.DiGraph()
for edge in mm:
	if(mm[edge] > 0.1):
		G.add_edge(edge[0],edge[1],label=mm[edge])

A=nx.to_agraph(G)
A.graph_attr.update(dpi="600")
A.layout(prog="dot")
A.draw('ordered-graph-hi.png')



# for n in G:
# 	G.node[n]['name'] = n

# d = json_graph.node_link_data(G)

# json.dump(d, open('force/force.json', 'w'))
# print ('Wrote node-link JSON data to force/force.json')

# http_server.load_url('force/force.html')
# print('or copy files etc')


# img=mpimg.imread('ordered-graph.png')
# imgplot = plt.imshow(img)
# plt.show()