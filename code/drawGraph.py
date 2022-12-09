import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt


g = rdflib.Graph()
result = g.parse('data/graphExample.ttl', format='ttl')

G = rdflib_to_networkx_multidigraph(result)

# Plot Networkx instance of RDF Graph
pos = nx.spring_layout(G, scale=10)

# node_labels = {i: i for i in G.nodes}
node_labels = {}
for i in G.nodes:
    # print(i)
    if 'spotify' and 'artist' in i:
        node_labels[i] = "%s%s" % ("spotify/artist:", i.rsplit('/', 1)[-1])
    elif 'spotify' and 'album' in i:
        node_labels[i] = "%s%s" % ("spotify/album:", i.rsplit('/', 1)[-1])
    elif 'spotify' and 'track' in i:
        node_labels[i] = "%s%s" % ("spotify/track:", i.rsplit('/', 1)[-1])
    elif 'dbpedia' in i:
        node_labels[i] = "%s%s" % ("dbpedia:", i.rsplit('/', 1)[-1])
    elif 'http' in i:
        node_labels[i] = i.rsplit('/', 1)[-1]
    else:
        node_labels[i] = i
    # print(node_labels[i])
for i, label in node_labels.items():
    print(label)

nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=2)
nx.draw(G, with_labels=True)
plt.show()
