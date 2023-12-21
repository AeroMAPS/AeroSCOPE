# @Time : 02/10/2023 10:31
# @Author : a.salgas
# @File : flight_level_plots.py
# @Software: PyCharm


import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import random


def pax_map_plot(flights_gpb_df):
    # Create the scattergeo figure

    fig = go.Figure()

    meanwidth = flights_gpb_df["CO2 Ppax"].mean()

    for i in range(len(flights_gpb_df)):
        fig.add_trace(
            go.Scattergeo(
                lon=[
                    flights_gpb_df["departure_lon"][i],
                    flights_gpb_df["arrival_lon"][i],
                ],
                lat=[
                    flights_gpb_df["departure_lat"][i],
                    flights_gpb_df["arrival_lat"][i],
                ],
                mode="lines",
                line=dict(
                    width=flights_gpb_df["CO2 Ppax"][i] / (1.5 * meanwidth),
                    color="#023047",
                ),
                opacity=0.8,
            )
        )

    fig.add_trace(
        go.Scattergeo(
            lon=flights_gpb_df["arrival_lon"],
            lat=flights_gpb_df["arrival_lat"],
            hoverinfo="text",
            text=flights_gpb_df["CO2 Ppax"],
            mode="markers",
            marker=dict(
                size=flights_gpb_df["CO2 Ppax"]
                / (0.01 * flights_gpb_df["CO2 Ppax"].mean()),
                color="#ffb703",
                sizemode="area",
                opacity=0.8,
                line=dict(width=0.5, color="black"),
            ),
            customdata=flights_gpb_df["iata_arrival"],
            hovertemplate="Flights to: "
            + "%{customdata}<br>"
            + "CO2 Ppax"
            + ": %{text:.0f}<br>"
            + "<extra></extra>",
        )
    )

    fig.update_geos(showcountries=True)
    fig.update_layout(
        showlegend=False, height=800, title="Route values for {}".format("CO2 Ppax")
    )
    fig.update_layout(
        margin=dict(l=5, r=5, t=60, b=5)
    )  # Adjust layout margins and padding
    return fig
