import plotly.express as px
import pandas as pd
import argparse

# define arguments
parser = argparse.ArgumentParser(description="View RaceCapture GPS data with rich speed information")
parser.add_argument('filename')
args = parser.parse_args()

# read data csv, extract gps fields, and then drop unknown values
# make sure to extract just the columns you want BEFORE dropping unknown
# you risk losing data by dropping naively
df = pd.read_csv(args.filename)

gps = df[["Interval|\"ms\"|0|0|1", "Latitude|\"Degrees\"|-180.0|180.0|25", "Longitude|\"Degrees\"|-180.0|180.0|25", "Speed|\"mph\"|0.0|150.0|25"]]
gps.dropna(
    axis = 0,
    how = 'any',
    subset = None,
    inplace = True
)

# ignore GPS values from before initialization (ie, 0s)
gps = gps[gps["Latitude|\"Degrees\"|-180.0|180.0|25"] != 0]

# this color scale is okay. have to work around the very light map bg
color_scale = [(0, 'green'), (1,'red')]

# create and show figure, note there are many options not shown for plotting
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