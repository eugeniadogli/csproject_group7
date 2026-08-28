# Ellen Maame Ama Hassan 
# Proof of Data Analysis and Visualization of the datasets: utilities, substations, and lines
# Data Analyst 

# Exploratory Data Analysis (EDA)
import pandas as pd
# Loading the data from CSV files
utilities = pd.read_csv('utilities.csv')
substations = pd.read_csv('substations.csv')  
lines = pd.read_csv('lines.csv')    

#The display of the first 5 rows of each dataset

print(utilities.head())
print(substations.head())
print(lines.head())

# info about the datasets
print(utilities.info())
print(substations.info())
print(lines.info())

# describe the datasets
print(utilities.describe())
print(substations.describe())
print(lines.describe())

print(substations.columns)

# distributions of the variables in the datasets

import matplotlib.pyplot as plt
region_counts = substations["Region"]. value_counts()
plt.figure(figsize=(16, 5))
region_counts.plot(kind='bar')

substations["Region"].hist()

plt.xlabel("Region") 
plt.ylabel("Number of Substations")
plt.title("Distribution of substations by region")
plt.xticks(rotation=45, ha='right')

plt.show()

#Relationship between the variables in the datasets
# Using a scatter plot to visualise and investigate whether voltage and capacity are reated. 

print(substations.dtypes) # to check the data types of the columns in the substations dataset

# Capacity histogram
plt.figure(figsize=(10, 6))
substations["Capacity (MVA)"].hist()
plt.xlabel("Capacity (MVA)")
plt.ylabel("Frequency")
plt.title("Distribution of Substation Capacities")
plt.show()

# Observation of the histogram 
'''
 From the histogram, we can observe that the distribution of substation capacities is right-skewed,
 with a majority of substations having lower capacities and a few substations having significantly higher capacities. 
 This indicates that while most substations are designed to handle moderate loads, there are some that are built to accommodate much larger loads,
 which could be due to their strategic importance or location in the power grid.
'''  

# Relationship between 2 numerical variables: Capacity and Voltage
plt.figure(figsize=(10, 6))
plt.scatter(substations["Capacity (MVA)"], substations["Voltage (kV)"])
plt.xlabel("Capacity (MVA)")
plt.ylabel("Voltage (kV)")
plt.title("Relationship between Substation Capacity and Voltage")
plt.show()

# Analysis of the scatter plot
'''
The scatter plot shows the relationship between substation capacity and voltage. 
From the plot, we can observe that there is a positive correlation between capacity and voltage, 
meaning that as the capacity of a substation increases, the voltage also tends to increase. 
This relationship is expected, as substations with higher capacities are typically designed
to handle higher voltages to efficiently transmit electricity over long distances. 
However, there are some outliers in the data where substations with similar capacities have different voltages,
which could be due to specific design considerations or operational requirements.
'''

# measuring their correlation
# Correlation coefficient between capacity and voltage and it tells you how two variables are related to each other.
correlation = substations["Capacity (MVA)"].corr(substations["Voltage (kV)"])
print(f"The correlation between substation capacity and voltage is: {correlation:.2f}")

# Interpretation of the correlation coefficient
'''
A correlation coefficient of 0.44 indicates a moderate positive correlation between substation capacity and voltage.
This means that, in general, as the capacity of a substation increases, the voltage also tends to increase.
However, the correlation is not very strong, suggesting that other factors may also influence the relationship between capacity and voltage in substations.
'''
# boxplot to visualize the distribution of substation capacities and identify any potential outliers
plt.boxplot(substations["Capacity (MVA)"].dropna()) # dropna means remove or drop missing values.
plt.ylabel("Capacity (MVA)")
plt.title("Boxplot of Substation Capacities")
plt.show()

substations["Type"].value_counts()

# Comparing the Capacity of Substations by Type using a boxplot
substations.boxplot(column="Capacity (MVA)", by="Type")
plt.xlabel("Substation Type")
plt.ylabel("Capacity (MVA)")
plt.title("Comparison of Substation Capacities by Type")
plt.suptitle('') # to remove the default title

plt.show()
#Analysis of the boxplot
'''
The box plot shows that Transmission substations have the highest median capacity, 
followed by Bulk Supply Points, while Distribution substations have the lowest median capacity.
Transmission substations also have a relatively wide range of capacities, indicating greater variation among them.
'''
# Commission year 

plt.hist(substations["Commissioning Year"].dropna(),bins = 20)
plt.xlabel("Commissioning Year")
plt.ylabel("Number of Substations")
plt.title("Distribution of Substation Commission Years")
plt.show()    

# Statistial Analysis 
# Select the Voltage and Capacity columns for statistical analysis and remove the missing values. 

correlation_data = substations[["Voltage (kV)", "Capacity (MVA)"]].dropna()

# number of observations
n = len(correlation_data)
print("The number of valid observations is :",n)

# t - statistic calculation
import math 
r = 0.44
n = 44
t = (r * math.sqrt(n - 2)) / (math.sqrt(1 - r**2))
print(f"The t-statistic is: {t:.2f}")
# r tells you how strong the relationship is between the two variables,
# n tells you how many data points you have.

import numpy as np
import pandas as pd 

print("NumPy:",np.__version__)
print("Pandas:",pd.__version__)

import numpy as np
correlation_data = substations[["Voltage (kV)", "Capacity (MVA)"]].dropna()

x = correlation_data["Voltage (kV)"].to_numpy()
y = correlation_data["Capacity (MVA)"].to_numpy()

observed_r = np.corrcoef(x, y)[0, 1]
np.random.seed(42)

num_permutations = 10000
count = 0

for i in range(num_permutations):
    shuffled_y = np.random.permutation(y)
    random_r = np.corrcoef(x, shuffled_y)[0, 1]

    if abs(random_r) >= abs(observed_r):
        count += 1
# Calculate p-value

p_value = count / num_permutations
print(f"The p-value is: {p_value}")

# Status distribution 

status_counts = substations["Status"].value_counts()
print(status_counts) 
# Interpretation:
'''
The majority of substations in the datasets are active, with 43 out of 44 substations (approximately 97.7%) classified as active.
Only 1 substation (approximately 2.3%) is inactive. This indicates that the dataset is highly dominated by operational substations.
'''
# Visualisation of the results 
substations["Status"].value_counts().plot(kind="bar")

plt.title("Substation Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number of Substations")
plt.show()
# Graph analysis: 
# The graph should show a very tall bar for Active (43) and a very small bar for Inactive (1)

print(utilities.columns)
print(substations.columns)
print(lines.columns)

print(utilities.shape)
print(substations.shape)
print(lines.shape)
# Relatiosnship checks- After running the ycode, all 3 relationships are valid.
print(lines["Utility ID"].isin(utilities["Utility ID"]).value_counts())

print(lines["Source Substation ID"].isin(substations["Substation ID"]).value_counts())

print(lines["Destination Substation ID"].isin(substations["Substation ID"]).value_counts())
print(lines["Utility ID"].isin(utilities["Utility ID"]).value_counts())

lines_with_utilities = lines.merge(
    utilities,
    on = "Utility ID",
    how = "left"
)
print(lines_with_utilities.head())
print(lines_with_utilities.shape)

lines_integrated = lines_with_utilities.merge(  

    substations,
    left_on = "Source Substation ID",
    right_on = "Substation ID",
    how = "left",
    suffixes=("","_Source")
)

print(lines_integrated.head())
print(lines_integrated.shape)

# Destination substation - Here We are combining the three datasets so that each electricity line has information about its utility, source substation, and destination substation.

lines_integrated = lines_integrated.merge(
    substations,
    left_on="Destination Substation ID",
    right_on="Substation ID",
    how="left",
    suffixes=("", "_Destination")
)

print(lines_integrated.head())
print(lines_integrated.shape)

# Analysis: 
'''
The three datasets were successfully integrated using their unique identifiers. All 55 electricity lines were matched to valid utilities, source substations, and destination substations,
 producing an integrated dataset of 55 rows and 41 columns.
'''
# Now : 
'''
We're taking the 44 substations from our dataset and turning each one into a NetworkX node,
while storing important information about each substation.
'''
import networkx as nx 
G = nx.Graph()

for _, row in substations.iterrows():
    G.add_node(
        row["Substation ID"],
        name=row["Name"],
        region=row["Region"],
        voltage=row["Voltage (kV)"],
        capacity=row["Capacity (MVA)"]
    )

print("Number of nodes:", G.number_of_nodes()) # 44 expected output 
 
for _, row in lines.iterrows():
    G.add_edge(
        row["Source Substation ID"],
        row["Destination Substation ID"],
        line_id=row["Line ID"],
        voltage=row["Voltage (kV)"],
        length=row["Length (km)"],
        capacity=row["Capacity (MVA)"],
        status=row["Status"],
        line_type=row["Line Type"]
    )
print("Number of edges:", G.number_of_edges())

# Calculates how many connections each node has using dictionaries: 
degree = dict(G.degree())

print("Degree of each substation:")
print(degree)
# Substations 3, 7, and 16 have the highest degree (5).

# A measure of how the connected nodes are relative to the rest of the network:

degree_centrality = nx.degree_centrality(G)

print("Degree centrality:")
print(degree_centrality)

# The formula is:
'''
Degree Centrality(v) = degree of v / n-1 
'''
# Betweeness centarlity 

betweenness_centrality = nx.betweenness_centrality(G)

print("Betweenness centrality:")
print(betweenness_centrality)
# Substation 16 has the highest betweenness centrality (0.5255).
# meaning - It means that, based on the structure of your graph, Substation 16 appears frequently on 
# shortest paths connecting other substations.

#Results interpretations: 
'''
Substation 16 had the highest betweenness centrality (0.5255), suggesting that it plays a significant 
bridging role within the network structure. Substations 12, 7, and 20 also showed relatively high betweenness values.
The results demonstrate that a substation's number of direct connections does not necessarily determine its structural importance, 
as illustrated by the difference between Substations 3 and 16.
'''
# Closeness Centrality  it asks how close is each substation to all other substations 

closeness_centrality = nx.closeness_centrality(G)

print("Closeness centrality:")
print(closeness_centrality)
# Substation 16 has the highest closeness centrality (0.2641),indicating that it is relatively close to other substations 
# within the network and can reach them through comparatively short paths. Substations 12 and 20 also recorded relatively high closeness values.

# Page Rank - it measures the importance of a node based on the node it is connected to 

pagerank = nx.pagerank(G)

print("PageRank:")
print(pagerank)

# Intrepretation 
'''
Substation 34 recorded the highest PageRank value of approximately 0.0470, 
suggesting that it has relatively high structural importance based on the connections within the network.
 Substations 7 and 16 also recorded high PageRank values.
'''
# Clustering Coefficient: checking whether the neighbouring substations are also connected to each other 
clustering = nx.clustering(G)

print("Clustering coefficient:")
print(clustering)

'''
The clustering coefficient results show variation in the local connectivity of the network. 
Several substations recorded a coefficient of 1.0, indicating that their neighbouring substations are fully interconnected. 
Other substations recorded lower values, including zero, indicating limited or no interconnectedness among their immediate neighbours.
'''
# Connected Componenets 
components = list(nx.connected_components(G))

print("Number of connected components:", len(components))
print("Connected components:")
print(components)
#Interpretation: 
'''
The network contains three connected components. The largest component contains 42 substations,
 while Substations 33 and 44 form separate isolated components. This indicates that, within the synthetic dataset,
most substations are connected through the main network, while two substations have no recorded connections.
'''
# Shortest Path: 
path = nx.shortest_path(G, source=1, target=43)

print("Shortest path from Substation 1 to Substation 43:")
print(path)
'''
Report interpretation
The shortest path between Substations 1 and 43 consists of 10 connections, passing through 11 substations.
This demonstrates how shortest-path analysis can be used to examine connectivity between assets within the network.
Since the graph is unweighted, the result represents the minimum number of network connections rather than the minimum geographical or physical distance.
'''
# Communities : Showing which substation naturally form groups within the networks.
communities = nx.community.greedy_modularity_communities(G)
print("Communities:")
for i, community in enumerate(communities, 1):
    print(f"Community {i}: {sorted(community)}")

'''
Report interpretation
Community detection identified 10 communities within the network. The communities represent groups of substations with relatively stronger internal connectivity.
The two isolated substations, 33 and 44, each formed their own community because they have no recorded connections to other substations.
'''
# Bridges shows which electrial lines are oin critical links between parts of the network? 

bridges = list(nx.bridges(G))
print("Bridges:")
print(bridges)

'''
Interpretation
The analysis identified 21 bridge edges in the network.
These connections are structurally important because removing any one of them would increase network fragmentation. 
The results indicate that several lines provide important links between different parts of the synthetic network.
'''
# Network Efficiency : How efficient are the networks 

efficiency = nx.global_efficiency(G)
print("Network efficiency:", efficiency) # 0.244
'''
The global network efficiency was approximately 0.2440. This indicates relatively limited overall connectivity efficiency within the synthetic network.
The presence of two isolated substations also contributes to the lower efficiency because they cannot reach other nodes.
'''

# N-1 contingency analysis: remove Substation 16

G_failure = G.copy()

G_failure.remove_node(16)

print("Original number of components:", nx.number_connected_components(G))
print("Components after removing Substation 16:",
      nx.number_connected_components(G_failure))
# Intrepretation 
'''
An N-1 contingency test was performed by removing Substation 16 from a copy of the network graph.
The number of connected components increased from 3 to 5, indicating that the removal caused additional network fragmentation. 
This suggests that Substation 16 plays an important structural role in maintaining connectivity within the synthetic network.
'''

# N-1 contingency analysis: remove one bridge line

G_line_failure = G.copy()

G_line_failure.remove_edge(16, 20)

print("Original number of components:", nx.number_connected_components(G))
print("Components after removing line (16, 20):",
      nx.number_connected_components(G_line_failure))
# Intrepretation 
'''
An N-1 contingency test was also performed by removing the bridge connecting Substations 16 and 20. 
The number of connected components increased from 3 to 4, demonstrating that the removal of this line causes additional network fragmentation.
This confirms the structural importance of the identified bridge.
'''
# Visualisations 
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.title("National Electricity Grid Network")
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=500,
    font_size=8
)
plt.show()

# Highlight substations with high betweenness centrality

node_colors = []

for node in G.nodes():
    if betweenness_centrality[node] >= 0.4:
        node_colors.append("red")
    else:
        node_colors.append("lightblue")

plt.figure(figsize=(12, 8))
plt.title("Electricity Grid Network - High Betweenness Substations")
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=500,
    font_size=8
)
plt.show()

# Geographical distribution of substations

plt.figure(figsize=(10, 8))
plt.title("Geographical Distribution of Substations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.scatter(
    substations["Longitude"],
    substations["Latitude"],
    s=50
)
plt.show()

# Geographical distribution of substations by capacity

plt.figure(figsize=(10, 8))

plt.title("Geographical Distribution of Substations by Capacity")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.scatter(
    substations["Longitude"],
    substations["Latitude"],
    s=substations["Capacity (MVA)"]
)
plt.show()

# Label high-capacity substations

plt.figure(figsize=(10, 8))
plt.title("Top 5 Highest-Capacity Substations by Location")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.scatter(
    substations["Longitude"],
    substations["Latitude"],
    s=substations["Capacity (MVA)"]
)

for _, row in substations.nlargest(5, "Capacity (MVA)").iterrows():
    plt.annotate(
        row["Short Name"],
        (row["Longitude"], row["Latitude"])
    )
plt.show()

# Number of substations by region

plt.title("Number of Substations by Region")
plt.xlabel("Region")
plt.ylabel("Number of Substations")
plt.xticks(rotation=45)
region_counts = substations["Region"].value_counts()
region_counts.plot(kind="bar", figsize=(10, 6))
plt.show()

# Average substation capacity by region
plt.title("Average Substation Capacity by Region")
plt.xlabel("Region")
plt.ylabel("Average Capacity (MVA)")
plt.xticks(rotation=45)

average_capacity = substations.groupby("Region")["Capacity (MVA)"].mean()
average_capacity.plot(kind="bar", figsize=(10, 6))
plt.show()

# Average commissioning year by region

average_year = substations.groupby("Region")["Commissioning Year"].mean()

plt.title("Average Substation Commissioning Year by Region")
plt.xlabel("Region")
plt.ylabel("Average Commissioning Year")
plt.xticks(rotation=45)

average_year.plot(kind="bar", figsize=(10, 6))
plt.show()

# Line status analysis

line_status = lines["Status"].value_counts()
plt.title("Transmission and Distribution Line Status")
plt.xlabel("Status")
plt.ylabel("Number of Lines")
plt.xticks(rotation=0)
line_status.plot(kind="bar", figsize=(8, 6))
plt.show()

# Substation status analysis
plt.title("Substation Operational Status")
plt.xlabel("Status")
plt.ylabel("Number of Substations")
plt.xticks(rotation=0)
substation_status = substations["Status"].value_counts()

substation_status.plot(kind="bar", figsize=(8, 6))
plt.show()

# Number of lines operated by each utility

utility_lines = lines["Utility ID"].value_counts()

utility_lines.plot(kind="bar", figsize=(8, 6))

plt.title("Number of Lines Operated by Utility")
plt.xlabel("Utility ID")
plt.ylabel("Number of Lines")
plt.xticks(rotation=0)

plt.show()

# Voltage level distribution

voltage_counts = substations["Voltage (kV)"].value_counts().sort_index()

voltage_counts.plot(kind="bar", figsize=(8, 6))

plt.title("Distribution of Substation Voltage Levels")
plt.xlabel("Voltage (kV)")
plt.ylabel("Number of Substations")
plt.xticks(rotation=0)

plt.show()


# Distribution of electricity line lengths

plt.figure(figsize=(10, 6))

plt.hist(lines["Length (km)"].dropna(), bins=10)

plt.title("Distribution of Electricity Line Lengths")
plt.xlabel("Line Length (km)")
plt.ylabel("Number of Lines")

plt.show()

# Distribution of electricity line capacities

plt.figure(figsize=(10, 6))

plt.hist(lines["Capacity (MVA)"].dropna(), bins=10)

plt.title("Distribution of Electricity Line Capacities")
plt.xlabel("Capacity (MVA)")
plt.ylabel("Number of Lines")

plt.show()

# Line type distribution

line_types = lines["Line Type"].value_counts()

line_types.plot(kind="bar", figsize=(8, 6))

plt.title("Distribution of Electricity Line Types")
plt.xlabel("Line Type")
plt.ylabel("Number of Lines")
plt.xticks(rotation=0)

plt.show()


