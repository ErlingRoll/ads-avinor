import pandas as pd
import plotly.graph_objects as go

i = 10

file_path_airports = "../data/DimFlyplassProccesedV2.csv"
file_path_paths = "../data/data_filtered/change_percent.csv"

df_airports = pd.read_csv(file_path_airports, index_col=None, low_memory=False, error_bad_lines=False)
df_airports.drop_duplicates(subset="IATACode", keep="first", inplace=True)

df_flight_paths = pd.read_csv(file_path_paths, index_col=None, low_memory=False, error_bad_lines=False)

df_flight_paths[['start',  'end']] = df_flight_paths.route.str.split("-", expand=True,)
df_flight_paths = df_flight_paths.drop(columns='route')

long_list = list
for index, row in df_flight_paths.iterrows():
    df_flight_paths.at[index, "start_lat"] = df_airports.loc[df_airports["IATACode"] == row["start"]]["Latitude"].values
    df_flight_paths.at[index, "start_lon"] = df_airports.loc[df_airports["IATACode"] == row["start"]]["Longitude"].values
    df_flight_paths.at[index, "end_lat"] = df_airports.loc[df_airports["IATACode"] == row["end"]]["Latitude"].values
    df_flight_paths.at[index, "end_lon"] = df_airports.loc[df_airports["IATACode"] == row["end"]]["Longitude"].values


fig = go.Figure()
fig.add_trace(go.Scattergeo(
    locationmode="geojson-id",
    geojson="europe",
    lon=df_airports['Longitude'],
    lat=df_airports['Latitude'],
    hoverinfo='text',
    text=df_airports['Description'],
    mode='markers+text',
    marker=dict(
        size=2,
        color='rgb(255, 0, 0)',
        line=dict(
            width=3,
            color='rgba(68, 68, 68, 0)'
        )
    )))

flight_paths = []
#for i in range(len(df_flight_paths)):
for i in range(i):
    fig.add_trace(
        go.Scattergeo(
            locationmode="geojson-id",
            geojson="nor",
            #lon=[df_flight_paths.iloc[i]['start_lon'], df_flight_paths['end_lon'].iloc[i]],
            #lat=[df_flight_paths.iloc[i]['start_lat'], df_flight_paths['end_lat'].iloc[i]],
            lon=[df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i]],
            lat=[df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i]],
            mode='lines',
            line=dict(width=(df_flight_paths['change'][i])/5, color='red'),
            opacity=float(0.5),
        )
    )

fig.update_geos(resolution=50)

fig.update_layout(
    title_text='Feb. 2011 American Airline flight paths<br>(Hover for airport names)',
    showlegend=False,
    geo=dict(
        scope="europe",
        projection_type='aitoff',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)

fig.show()
