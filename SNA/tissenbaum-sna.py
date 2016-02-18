import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from random import choice, sample, randint
import os
import csv


# returns a defaultdict of startnodes mapped to lists of endnodes
def generate_directed_network(number_of_nodes, number_of_edges):
    list_of_random_names = ["agustina","alexia","arcelia","augustine","barb","basil",
                            "bernarda","bob","charlette","corrine","cristy","crysta",
                            "deidra","haley","hyo","jamila","janyce","jenna","judson",
                            "kacie","katlyn","kelvin","keva","krysten","lasonya",
                            "lavon","lawanda","lemuel","leona","lionel","meagan",
                            "michelina","neoma","pandora","pierre","porfirio","ronna",
                            "shala","shemeka","sherman","shiloh","tessie","thalia",
                            "tonita","tyler","velma","velva","willa","winfred","yajaira"]
    if number_of_nodes > len(list_of_random_names):
        raise IndexError("too many nodes!")
    elif number_of_nodes < 2:
        raise IndexError("too few nodes!")
    elif number_of_edges > (number_of_nodes - 1)**2:
        raise IndexError("too many edges!")
    elif number_of_edges < 1:
        raise IndexError("too few edges!")
    nodes = sample(list_of_random_names,number_of_nodes)
    network_map = defaultdict(list)
    for edge_number in range(number_of_edges):
        start_node = choice(nodes)
        end_node = choice(nodes)
        while (end_node in network_map[start_node]) or (end_node == start_node):
            start_node = choice(nodes)
            end_node = choice(nodes)
        network_map[start_node].append(end_node)
    return network_map


# expects data about digraph in form:
# name_a,name_b
# name_a,name_c
# ...
def read_directed_network(csv_in_filename):
    network_map = defaultdict(list)
    csv_data = csv.reader(open(csv_in_filename))
    for line in csv_data:
        node_a = line[0]
        node_b = line[1]
        network_map[node_a].append(node_b)
    return network_map


def make_color_list(number_of_nodes,number_of_colors=5):
    base_colors = [round((1.0 * i)/number_of_colors,3) for i in range(number_of_colors)]
    return sample(base_colors*number_of_nodes,number_of_nodes)


def make_klique_color_list(G,iterations=1000,max_colors=5):
    output_colors = make_color_list(G.number_of_nodes(),number_of_colors=randint(2,max_colors))
    best_klique = kliquefinder_metric(G,output_colors)
    for i in range(iterations):
        local_x_colors = make_color_list(G.number_of_nodes(),number_of_colors=randint(2,max_colors))
        current_klique = kliquefinder_metric(G,local_x_colors)
        if kliquefinder_metric(G,local_x_colors) > best_klique:
            output_colors = local_x_colors
            best_klique = current_klique
    return output_colors


def kliquefinder_metric(p_G, p_color_list):
    all_nodes = p_G.nodes()
    x_colormap = {all_nodes[i]:p_color_list[i] for i in range(p_G.number_of_nodes())}
    countA = countB = countC = countD = 0.0
    for node_a in all_nodes:
        countA += len([node_b for node_b in all_nodes if node_b not in p_G[node_a] and x_colormap[node_a] != x_colormap[node_b]])
        countB += len([node_b for node_b in all_nodes if node_b     in p_G[node_a] and x_colormap[node_a] != x_colormap[node_b]])
        countC += len([node_b for node_b in all_nodes if node_b not in p_G[node_a] and x_colormap[node_a] == x_colormap[node_b]])
        countD += len([node_b for node_b in all_nodes if node_b     in p_G[node_a] and x_colormap[node_a] == x_colormap[node_b]])
    # print countA,countB,countC,countD
    return (countA + countD) * 1.0 / (countB + countC)

input_file_name = 'slack_relations.csv'
if os.path.isfile(input_file_name):
    print "Reading input network from: " + input_file_name
    my_network = read_directed_network(input_file_name)
else:
    num_nodes = 15
    num_edges = int(num_nodes * 1.25)
    print "Generating network of size:", num_nodes, "nodes,", num_edges, "edges"
    my_network = generate_directed_network(num_nodes, num_edges)


G = nx.Graph()  # Undirected network
# G = nx.DiGraph()  #Directed network

for node_a in sorted(my_network):
    G.add_node(node_a)
    for node_b in sorted(my_network[node_a]):
        # print ','.join([node_a,node_b])
        G.add_edge(node_a,node_b)

pos = nx.spring_layout(G, iterations=1000)

offset =-0.05
pos_labels = {}
keys = pos.keys()
for key in keys:
    x, y = pos[key]
    pos_labels[key] = ([x, y+offset])

formattedLabels = {}
for f in nx.degree_centrality(G):
    x = nx.degree_centrality(G)[f]
    formattedLabels[f] = "centrality: " +str(x)

counter = 0
newLabels = {}
for x in pos_labels.keys():
    # newLabels[x] = (x +"\n"+ formattedLabels.values()[counter])
    newLabels[x] = x
    counter +=1




x_colors = make_klique_color_list(G,iterations=1000,max_colors=3)
nx.draw(G,pos=pos,with_labels=False,cmap=plt.get_cmap('rainbow'),vmin=0,vmax=1,node_color=x_colors,font_size=24,alpha=0.5)
nx.draw_networkx_labels(G,pos=pos_labels,labels=newLabels)
print "lables" +" " +str(pos_labels)


print "kliques",len(set(x_colors))
print "nx.degree_centrality(G)",nx.degree_centrality(G)
print "nx.betweenness_centrality(G)",nx.betweenness_centrality(G)
plt.annotate("Most Central" +" " +max(nx.degree_centrality(G)),
             xy=(-0.58, .7),
             transform=plt.gca().transAxes)
plt.annotate("Cliques" +" " +str(len((set(x_colors)))),
             xy=(-0.58, .75),
             transform=plt.gca().transAxes)
plt.show()
