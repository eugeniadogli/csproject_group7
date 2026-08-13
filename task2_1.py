import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

substations = pd.read_csv("substations.csv")
lines = pd.read_csv("lines.csv")
# Create network graph — undirected, since AC power can flow either way
# along a line depending on system conditions (unlike a scheduled flight,
# which always has a fixed origin and destination)
G = nx.Graph()
# Add substations as nodes with attributes (region, voltage, coordinates, etc.)
for _, row in substations.iterrows():
    G.add_node(
        row['Substation ID'],
        region=row['Region'],
        voltage=row['Voltage (kV)'],
        coordinates=(row['Latitude'],
                     row['Longitude'])
    )
# Add lines as edges with weights (length, capacity, etc.)
for _, row in lines.iterrows():
    G.add_edge(
        row['Source Substation ID'],
        row['Destination Substation ID'],
        length=row['Length (km)'],
        capacity=row['Capacity (MVA)']
    )

print("Number of nodes (substations):", G.number_of_nodes()) #44 nodes
print("Number of edges (lines):", G.number_of_edges()) #55 edges
 
# Calculate network metrics
# - Node centrality measures (degree, betweenness, closeness, PageRank)
degree_centrality = nx.degree_centrality(G)
print("Degree Centrality:", degree_centrality)

betweenness_centrality = nx.betweenness_centrality(G)
print("Betweenness Centrality:", betweenness_centrality)

closeness_centrality = nx.closeness_centrality(G)
print("Closeness Centrality:", closeness_centrality)

# - Network diameter and average path length
if nx.is_connected(G):
    diameter = nx.diameter(G)
    avg_path_length = nx.average_shortest_path_length(G)
    print("Network Diameter:", diameter)
    print("Average Path Length:", avg_path_length)
else:
    print("The network is not connected, so diameter and average path length cannot be calculated.")

# - Clustering coefficients
clustering_coefficients = nx.clustering(G)
print("Clustering Coefficients:", clustering_coefficients)

average_clustering_coefficient = nx.average_clustering(G)
print("Average Clustering Coefficient:", average_clustering_coefficient)

# - Community detection
from networkx.algorithms import community
communities = community.greedy_modularity_communities(G)
print("Communities:", communities)

for i, comm in enumerate(communities):
    print(f"Community {i + 1}: {list(comm)}")


# - Critical-substation identification
top_critical_substations = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 Critical Substations (by Betweenness Centrality):")
for substation, centrality in top_critical_substations:
    print(f"  {substation}: {centrality}")

# Analyse network structure
# - Identify the most-connected substations (regional 'superhubs')
top_connected_substations = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 Most Connected Substations (by Degree Centrality):")
for substation, centrality in top_connected_substations:
    print(f"  {substation}: {centrality}")

# - Find bridge lines (critical single points of connection)
bridge_edges = list(nx.bridges(G))
print("Bridge Lines (Critical Single Points of Connection):", bridge_edges)
for edge in bridge_edges:
    print(f"  {edge[0]} <-> {edge[1]}")

# - Detect isolated components
components = list(nx.connected_components(G))
print("Isolated Components:")
for i, component in enumerate(components):
    print(f"  Component {i + 1}: {list(component)}")

# - Measure network efficiency
efficiency = nx.global_efficiency(G)
print("Network Efficiency:", efficiency)
