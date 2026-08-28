import folium
import pandas as pd
from folium.plugins import MeasureControl, MiniMap
from folium.plugins import HeatMap
from geopy.distance import geodesic
import math



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
        latitude.append(Latitude)
        longitude.append(Longitude)
        voltage.append(Voltage)
        capacity.append(Capacity)
        commissioning_year.append(Commissioning_Year)
        type.append(Type)
        status.append(Status)



with open('utilities.csv', 'r') as u:
    utility_ID = []
    uname = []
    alias = []
    code = []
    utype = []
    country = []
    active = []

    for line2 in u:
        Utility_ID,Uname,Alias,Code,Utype,Country,Active = line2.strip().split(',')
        utility_ID.append(Utility_ID)
        uname.append(Uname)
        alias.append(Alias)
        code.append(Code)
        utype.append(Utype)
        country.append(Country)
        active.append(Active)


eco_footprints = pd.read_csv('substations.csv')


with open('ghana_regions_detailed.geojson', 'r') as geojson_file:
    geojson_data = geojson_file.read()
ghana_url = geojson_data

carto = 'https://basemaps.cartocdn.com/rastertiles/voyager/%7Bz%7D/%7Bx%7D/%7By%7D.png?key=cb1_2huq_1_4fd2daa58c0a2c3bca3aab62'
carto_attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>'

m = folium.Map(location=[7.9465, -1.0232], tiles = carto, attr=carto_attr, subdomains='abcd', zoom_start=7)

folium.GeoJson(ghana_url, name='geojson').add_to(m)
folium.Choropleth(
    geo_data = ghana_url,
    name='choropleth',
    data = eco_footprints,
    columns=['Region', 'Capacity (MVA)'],
    key_on = 'feature.properties.shapeName',
    fill_color = 'YlGn',
    fill_opacity = 0.7,
    line_opacity = 0.2,
    legend_name = 'Substation Capacity (MVA)'
).add_to(m)


heat_data = [[float(latitude[i]), float(longitude[i]), float(voltage[i])] for i in range(1, len(latitude))]

# - Line-density heatmaps
HeatMap(data=heat_data, radius=25, blur=15, max_zoom=18).add_to(m)


# HAVERSINE DISTANCE CALCULATION
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


# - Analyse substation density by region
df = pd.read_csv("substations.csv")


map_center = [df["Latitude"].mean(), df["Longitude"].mean()]


fg_active_nodes = folium.FeatureGroup(name="Active Substations", show=True)
fg_inactive_nodes = folium.FeatureGroup(name="Inactive Substations", show=True)
fg_transmission_grid = folium.FeatureGroup(
    name="Regional Grid Links", show=True
)
fg_cross_border = folium.FeatureGroup(
    name="Cross-Border Interconnectors", show=True
)

# - Identify geographic clusters and coverage gaps
for _, row in df.iterrows():
    is_active = str(row["Status"]).strip().lower() == "active"
    color = "#2ecc71" if is_active else "#e74c3c"
    fill_color = "#3498db" if row["Country"] == "Ghana" else "#e67e22"

   
    radius = max(5, min(14, math.sqrt(row["Capacity (MVA)"])))

    popup_html = f"""
    <div style="font-family: sans-serif; min-width: 170px;">
        <h4 style="margin:0 0 5px 0;">{row['Name']}</h4>
        <b>ID:</b> {row['Substation ID']}<br>
        <b>Region / Country:</b> {row['Region']}, {row['Country']}<br>
        <b>Type:</b> {row['Type']}<br>
        <b>Voltage:</b> {row['Voltage (kV)']} kV<br>
        <b>Capacity:</b> {row['Capacity (MVA)']} MVA<br>
        <b>Commissioned:</b> {row['Commissioning Year']}<br>
        <b>Status:</b> <span style="color:{color};"><b>{row['Status']}</b></span>
    </div>
    """

    marker = folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=radius,
        color=color,
        weight=2,
        fill=True,
        fill_color=fill_color,
        fill_opacity=0.85,
        tooltip=f"{row['Name']} ({row['Voltage (kV)']} kV)",
        popup=folium.Popup(popup_html, max_width=300),
    )

    if is_active:
        marker.add_to(fg_active_nodes)
    else:
        marker.add_to(fg_inactive_nodes)

# - Map each utility's line network
total_network_km = 0
cross_border_count = 0


grouped_regions = df.groupby("Region")
for region_name, group in grouped_regions:
    substations = group.to_dict("records")
    for i in range(len(substations) - 1):
        s1, s2 = substations[i], substations[i + 1]
        dist = haversine_km(
            s1["Latitude"], s1["Longitude"], s2["Latitude"], s2["Longitude"]
        )
        total_network_km += dist

        folium.PolyLine(
            locations=[
                [s1["Latitude"], s1["Longitude"]],
                [s2["Latitude"], s2["Longitude"]],
            ],
            color="#2980b9",
            weight=3,
            opacity=0.7,
            tooltip=f"{region_name} Line ({dist:.1f} km)",
        ).add_to(fg_transmission_grid)

# - Regional and cross-border connectivity analysis
cross_border_pairs = [
    (35, 37),  # Bawku Substation (Ghana) <-> Bolgatanga Interconnection (Burkina)
    (37, 43),  # Bolgatanga Intercon <-> Bobo-Dioulasso Hub
    (15, 38),  # Axim Substation (Ghana) <-> Elubo Border Station (Cote d'Ivoire)
    (38, 42),  # Elubo Border <-> Abidjan Transmission Hub
    (24, 39),  # Ho Substation (Ghana) <-> Aflao Border Station (Togo)
    (39, 40),  # Aflao Border <-> Lome Transmission Hub
    (40, 41),  # Lome (Togo) <-> Cotonou (Benin)
    (42, 44),  # Abidjan (Cote d'Ivoire) <-> Conakry (Guinea)
]

for src_id, tgt_id in cross_border_pairs:
    src = df[df["Substation ID"] == src_id].iloc[0]
    tgt = df[df["Substation ID"] == tgt_id].iloc[0]

    dist = haversine_km(
        src["Latitude"], src["Longitude"], tgt["Latitude"], tgt["Longitude"]
    )
    total_network_km += dist
    cross_border_count += 1

    popup_html = f"""
    <div style="font-family: sans-serif; min-width: 180px;">
        <h4 style="margin:0 0 5px 0;">Cross-Border Interconnector</h4>
        <b>Route:</b> {src['Name']} ({src['Country']}) &rarr; {tgt['Name']} ({tgt['Country']})<br>
        <b>Distance:</b> {dist:.1f} km<br>
        <b>Voltage Rating:</b> {max(src['Voltage (kV)'], tgt['Voltage (kV)'])} kV
    </div>
    """

    folium.PolyLine(
        locations=[
            [src["Latitude"], src["Longitude"]],
            [tgt["Latitude"], tgt["Longitude"]],
        ],
        color="#e67e22",
        weight=4,
        dash_array="6, 6",
        opacity=0.9,
        tooltip=f"Cross-Border Line: {src['Country']} ↔ {tgt['Country']} ({dist:.1f} km)",
        popup=folium.Popup(popup_html, max_width=300),
    ).add_to(fg_cross_border)


active_count = len(df[df["Status"] == "Active"])
inactive_count = len(df[df["Status"] == "Inactive"])
total_capacity = df["Capacity (MVA)"].sum()

hud_html = f"""
<div style="
    position: fixed; 
    bottom: 30px; left: 30px; width: 280px;
    background-color: white; z-index:9999; font-size:12px;
    border:2px solid #bdc3c7; border-radius: 8px; padding: 12px;
    font-family: sans-serif; box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
">
    <b style="font-size:14px; color:#2c3e50;">Regional Connectivity Summary</b><br>
    <hr style="margin: 6px 0;">
    <b>Total Substations:</b> {len(df)} ({active_count} Active / {inactive_count} Inactive)<br>
    <b>Total Transformer Capacity:</b> {total_capacity:,.1f} MVA<br>
    <b>Total Analyzed Grid Lines:</b> {total_network_km:,.1f} km<br>
    <b>Cross-Border Corridors:</b> {cross_border_count} links<br>
    <hr style="margin: 6px 0;">
    <span style="color:#3498db;">●</span> Ghana Nodes &nbsp; 
    <span style="color:#e67e22;">●</span> Regional/Foreign Nodes<br>
    <span style="color:#2980b9;">━</span> Regional Lines &nbsp; 
    <span style="color:#e67e22;">┅</span> Cross-Border Lines
</div>
"""
m.get_root().html.add_child(folium.Element(hud_html))


fg_active_nodes.add_to(m)
fg_inactive_nodes.add_to(m)
fg_transmission_grid.add_to(m)
fg_cross_border.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)
m.add_child(
    MeasureControl(position="topright", primary_length_unit="kilometers")
)
MiniMap(toggle_display=True).add_to(m)
m.save("footprint.html")