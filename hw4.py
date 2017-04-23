from itertools import groupby
from multiprocessing import Pool
import nltk
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from numpy import genfromtxt
import csv

text = None
csvfile = open('casts.csv','rb')
csvFileArray = []
for row in csv.reader(csvfile, delimiter = ';'):
    csvFileArray.append((row[1], row[2]))

groupedByFilm = ([() + tuple(elem for _, elem in group) for key, group in groupby(csvFileArray[:150], lambda pair: pair[0])])
G = nx.Graph()
for item in csvFileArray[:150]:
    G.add_node(""+item[1].decode('utf-8').encode('ascii', 'ignore'))

for items in groupedByFilm:
    for item in items:
        for item2 in items:
            if item != item2:
                G.add_edges_from([(""+item.decode('utf-8').encode('ascii', 'ignore'), ""+item2.decode('utf-8').encode('ascii', 'ignore'))])



plt.figure(figsize=(20, 10))
pos = graphviz_layout(G, prog="fdp")
nx.draw(G, pos,
        labels={v: str(v) for v in G},
        cmap=plt.get_cmap("bwr"),
        node_color=[G.degree(v) for v in G],
        font_size=12
        )
plt.show()

nx.write_gexf(G, "export.gexf")

centralities = [nx.degree_centrality, nx.closeness_centrality,nx.betweenness_centrality, nx.eigenvector_centrality]
region=220
for centrality in centralities:
    region+=1
    plt.subplot(region)
    plt.title(centrality.__name__)
    nx.draw(G, pos, labels={v:str(v) for v in G},
      cmap = plt.get_cmap("bwr"), node_color=[centrality(G)[k] for k in centrality(G)])
plt.savefig("centralities.png")
plt.show()

communities = {node: cid + 1 for cid, community in enumerate(nx.k_clique_communities(G, 3)) for node in community}

pos = graphviz_layout(G, prog="fdp")
nx.draw(G, pos,
        labels={v: str(v) for v in G},
        cmap=plt.get_cmap("rainbow"),
        node_color=[communities[v] if v in communities else 0 for v in G])
plt.savefig("communities.png")
plt.show()

for component in nx.connected_components(G):
    print(component)

