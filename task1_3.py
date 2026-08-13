import pandas as pd

utilities = pd.read_csv('utilities.csv')
lines = pd.read_csv('lines.csv')
substations = pd.read_csv("substations.csv")

#Checking invalid  Utility IDs in the utility datset
valid_utility_ids = set(utilities['Utility ID'])
invalid_utility_ids = lines[~lines['Utility ID'].isin(valid_utility_ids)]
print("Invalid Utility IDs in this dataset are: ", len(invalid_utility_ids))

#Checking invalid Destination Substation IDs in the lines dataset
invalid_destination_ids = lines[~lines['Destination Substation ID'].isin(substations['Substation ID'])]
print('Invalid Destination Substation IDs in this dataset are: ', len(invalid_destination_ids))
invalid_source_ids = lines[~lines["Source Substation ID"].isin(substations['Substation ID'])]
print("Invalid Source Substation IDs in this dataset are: ", len(invalid_source_ids))

#Creating a lookup dictionary for utilty IDs and their corresponding names
utillity_lookup = dict(zip(utilities['Utility ID'], utilities['Name']))
print("\n Utility Lookup Dictionary: ", utillity_lookup)

#Creating a lookup dictionary for substation IDs and their corresponding names
substation_lookup = dict(zip(substations['Substation ID'], substations['Name']))
print("\n substation Lookup Dictionary: ", substation_lookup)

#Merging the lines dataset with the utility and substation datasets to get the names of the utilities and substations
intergrated_data = lines.merge(utilities, left_on='Utility ID', right_on='Utility ID', how='left').merge(substations, left_on='Source Substation ID', right_on='Substation ID', how='left').merge(substations, left_on='Destination Substation ID', right_on='Substation ID', how='left')
intergrated_data = intergrated_data.rename(columns={'Name_x': 'Utility Name', 'Name_y': 'Source Substation Name', 'Name': 'Destination Substation Name'})

#Saving the intergrated dataset to a new CSV file
intergrated_data.to_csv('intergrated_data.csv', index=False)
print("\n Intergrated dataset saved to intergrated_data.csv")
