# Ellen Maame Ama Hassan 
# Proof of Data Analysis and Visualization of the datasets: utilities, substations, and lines
# Data Analyst 

# Exploratory Data Analysis (EDA)
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




