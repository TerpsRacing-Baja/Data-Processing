import plotly.express as px
import pandas as pd

df = pd.read_csv("WITH-sway-bar-accel-right-wheels-2.csv")

df.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)

gps = df[["Interval|\"ms\"|0|0|1", "Latitude|\"Degrees\"|-180.0|180.0|25", "Longitude|\"Degrees\"|-180.0|180.0|25", "Speed|\"mph\"|0.0|150.0|25"]]
gps = gps[gps["Latitude|\"Degrees\"|-180.0|180.0|25"] != 0]
gps = gps[gps["Interval|\"ms\"|0|0|1"] >= 31043]

color_scale = [(0, 'blue'), (1,'orange')]

fig = px.scatter_mapbox(gps, 
                        lat="Latitude|\"Degrees\"|-180.0|180.0|25", 
                        lon="Longitude|\"Degrees\"|-180.0|180.0|25",
                        color="Speed|\"mph\"|0.0|150.0|25",
                        color_continuous_scale=color_scale,
                        hover_name="Interval|\"ms\"|0|0|1", 
                        hover_data="Interval|\"ms\"|0|0|1",
                        zoom=18, 
                        height=800,
                        width=800)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()