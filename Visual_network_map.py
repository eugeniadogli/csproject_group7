import csv
import folium
from geopy.distance import geodesic


# Assigning the datasets generated to variables
with open('lines.csv', 'r') as f:
    line_ID = []
    utility_ID = []
    source_substation_ID = []
    source_substation = []
    destination_substation_ID = []
    destination_substation = []
    voltage = []
    length = []
    capacity = []
    status = []
    line_type = []

    for line in f:
        Line_ID,Utility_ID,Source_Substation_ID,Source_Substation,Destination_Substation_ID,Destination_Substation,Voltage,Length,Capacity,Status,Line_Type = line.strip().split(',')
        line_ID.append(Line_ID)
        utility_ID.append(Utility_ID)
        source_substation_ID.append(Source_Substation_ID)
        source_substation.append(Source_Substation)
        destination_substation_ID.append(Destination_Substation_ID)
        destination_substation.append(Destination_Substation)
        voltage.append(Voltage)
        length.append(Length)
        capacity.append(Capacity)
        status.append(Status)
        line_type.append(Line_Type)



with open('substations.csv', 'r') as s:
    substation_ID = []
    name = []
    short_name = []
    region = []
    country = []
    latitude = []
    longitude = []
    voltage = []
    capacity = []
    commissioning_year = []
    type = []
    status = []


    for line1 in s:
        Substation_ID,Name,Short_Name,Region,Country,Latitude,Longitude,Voltage,Capacity,Commissioning_Year,Type,Status = line1.strip().split(',')
        substation_ID.append(Substation_ID)
        name.append(Name)
        short_name.append(Short_Name)
        region.append(Region)
        country.append(Country)
        latitude.append(float(Latitude))
        longitude.append(float(Longitude))
        voltage.append(Voltage)
        capacity.append(Capacity)
        commissioning_year.append(Commissioning_Year)
        type.append(Type)
        status.append(Status)

# Geographic analysis
# - Recompute (or verify) line distances using the geodesic/haversine formula
# - Analyse substation density by region
# - Identify geographic clusters and coverage gaps
# - Map each utility's line network
 
# Spatial visualizations
# - National map with all substations colored by voltage level
# - Line-density heatmaps
# - Utility-specific network maps
# - Regional and cross-border connectivity analysis
