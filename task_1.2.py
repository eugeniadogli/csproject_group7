import pandas as pd
# Loading the data from CSV files
utilities = pd.read_csv('csproject_group7/utilities.csv')
substations = pd.read_csv('csproject_group7/substations.csv')  
lines = pd.read_csv('csproject_group7/lines.csv')    

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
