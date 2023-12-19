# @Time : 02/10/2023 10:31
# @Author : a.salgas
# @File : flight_level_plots.py
# @Software: PyCharm


import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import random


def flights_map_plot(flights_gpb_df, value_watched_flights):
    # Create the scattergeo figure
    fig = go.Figure()

    meanwidth = flights_gpb_df[value_watched_flights].mean()

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
                    width=flights_gpb_df[value_watched_flights][i] / (1.5 * meanwidth),
                    color="#023047",
                ),
                opacity=0.8,
            )
        )

    # group by airport

    if "n_flights" in flights_gpb_df.columns:
        airport_df = (
            flights_gpb_df.groupby("iata_arrival")
            .agg(
                {
                    "co2": "sum",
                    "ask": "sum",
                    "seats": "sum",
                    "n_flights": "sum",
                    "arrival_lon": "first",
                    "arrival_lat": "first",
                }
            )
            .reset_index()
        )
    else:
        airport_df = (
            flights_gpb_df.groupby("iata_arrival")
            .agg(
                {
                    "co2": "sum",
                    "ask": "sum",
                    "seats": "sum",
                    "arrival_lon": "first",
                    "arrival_lat": "first",
                }
            )
            .reset_index()
        )

    fig.add_trace(
        go.Scattergeo(
            lon=airport_df["arrival_lon"],
            lat=airport_df["arrival_lat"],
            hoverinfo="text",
            text=airport_df[value_watched_flights],
            mode="markers",
            marker=dict(
                size=airport_df[value_watched_flights]
                / (0.01 * airport_df[value_watched_flights].mean()),
                color="#ffb703",
                sizemode="area",
                opacity=0.8,
                line=dict(width=0.5, color="black"),
            ),
            customdata=airport_df["iata_arrival"],
            hovertemplate="Flights to: "
            + "%{customdata}<br>"
            + value_watched_flights
            + ": %{text:.0f}<br>"
            + "<extra></extra>",
        )
    )

    fig.update_geos(showcountries=True)
    fig.update_layout(
        showlegend=False,
        height=800,
        title="Route values for {}".format(value_watched_flights),
    )
    fig.update_layout(
        margin=dict(l=5, r=5, t=60, b=5)
    )  # Adjust layout margins and padding
    return fig


def flights_map_plot_OS(flights_gpb_df, value_watched_flights):
    # Create the scattergeo figure
    fig = go.Figure()

    meanwidth = flights_gpb_df[value_watched_flights].mean()

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
                    width=flights_gpb_df[value_watched_flights][i] / (1.5 * meanwidth),
                    color="#023047",
                ),
                opacity=0.8,
            )
        )

    # group by airport

    if "n_flights" in flights_gpb_df.columns:
        airport_df = (
            flights_gpb_df.groupby("dest")
            .agg(
                {
                    "co2": "sum",
                    "ask": "sum",
                    "seats": "sum",
                    "n_flights": "sum",
                    "arrival_lon": "first",
                    "arrival_lat": "first",
                }
            )
            .reset_index()
        )
    else:
        airport_df = (
            flights_gpb_df.groupby("iata_arrival")
            .agg(
                {
                    "co2": "sum",
                    "ask": "sum",
                    "seats": "sum",
                    "arrival_lon": "first",
                    "arrival_lat": "first",
                }
            )
            .reset_index()
        )

    fig.add_trace(
        go.Scattergeo(
            lon=airport_df["arrival_lon"],
            lat=airport_df["arrival_lat"],
            hoverinfo="text",
            text=airport_df[value_watched_flights],
            mode="markers",
            marker=dict(
                size=airport_df[value_watched_flights]
                / (0.01 * airport_df[value_watched_flights].mean()),
                color="#ffb703",
                sizemode="area",
                opacity=0.8,
                line=dict(width=0.5, color="black"),
            ),
            customdata=airport_df["dest"],
            hovertemplate="Flights to: "
            + "%{customdata}<br>"
            + value_watched_flights
            + ": %{text:.0f}<br>"
            + "<extra></extra>",
        )
    )

    fig.update_geos(showcountries=True)
    fig.update_layout(
        showlegend=False,
        height=800,
        title="Route values for {}".format(value_watched_flights),
    )
    fig.update_layout(
        margin=dict(l=5, r=5, t=60, b=5)
    )  # Adjust layout margins and padding
    return fig


def flights_treemap_plot(flights_df, value_watched_flights):
    fig = px.treemap(
        flights_df,
        path=[
            px.Constant("Total currently selected"),
            "iata_departure",
            "iata_arrival",
            "airline_iata",
            "acft_icao",
        ],
        values=value_watched_flights,
        color_discrete_sequence=px.colors.qualitative.T10,
        title="Treemap for {}".format(value_watched_flights),
    )

    fig.update_layout(margin=dict(l=5, r=5, t=60, b=5))
    fig.update_traces(
        marker=dict(cornerradius=5),
    )

    if value_watched_flights == "co2":
        fig.update_traces(
            hovertemplate="Flow=%{id}<br>CO<sub>2</sub>=%{value:.2f} (lg)"
        )
    elif value_watched_flights == "ask":
        fig.update_traces(hovertemplate="Flow=%{id}<br>ASK=%{value:.2f}")
    elif value_watched_flights == "seats":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Seats=%{value:.2f}")
    elif value_watched_flights == "n_flights":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Flights=%{value:.2f}")

    return fig


def flights_treemap_plot_OS(flights_df, value_watched_flights):
    fig = px.treemap(
        flights_df,
        path=[
            px.Constant("Total currently selected"),
            "origin",
            "dest",
            "airline_iata",
            "acft_icao",
        ],
        values=value_watched_flights,
        color_discrete_sequence=px.colors.qualitative.T10,
        title="Treemap for {}".format(value_watched_flights),
    )

    fig.update_layout(margin=dict(l=5, r=5, t=60, b=5))
    fig.update_traces(
        marker=dict(cornerradius=5),
    )

    if value_watched_flights == "co2":
        fig.update_traces(
            hovertemplate="Flow=%{id}<br>CO<sub>2</sub>=%{value:.2f} (lg)"
        )
    elif value_watched_flights == "ask":
        fig.update_traces(hovertemplate="Flow=%{id}<br>ASK=%{value:.2f}")
    elif value_watched_flights == "seats":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Seats=%{value:.2f}")
    elif value_watched_flights == "n_flights":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Flights=%{value:.2f}")

    return fig


def distance_histogram_plot_flights(flights_df, value_watched_ctry):
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6.5))
    sns.histplot(
        data=flights_df,
        x="distance_km",
        weights=value_watched_ctry,
        common_norm=False,
        element="step",
        color="#EE9B00",
        bins=range(0, int(flights_df["distance_km"].max()) + 500, 500),
        ax=ax,
        alpha=0.5,
    )
    ax.set_title("Repartition of {} by flight distance".format(value_watched_ctry))
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel(value_watched_ctry)
    return fig


def formatter(x, pos):
    del pos
    return str(round(x * 100))


def distance_cumul_plot_flights(flights_df):
    sns.set_style("darkgrid")
    # Create a new figure with a single subplot
    fig, ax = plt.subplots(figsize=(10, 6.5))
    sns.histplot(
        flights_df,
        x="distance_km",
        weights="seats",
        label="Seats",
        element="poly",
        fill=False,
        cumulative=True,
        stat="percent",
        ax=ax,
        bins=range(0, int(flights_df["distance_km"].max()) + 50, 50),
    )
    sns.histplot(
        flights_df,
        x="distance_km",
        weights="ask",
        label="ASK",
        element="poly",
        fill=False,
        cumulative=True,
        stat="percent",
        ax=ax,
        bins=range(0, int(flights_df["distance_km"].max()) + 50, 50),
    )
    sns.histplot(
        flights_df,
        x="distance_km",
        weights="co2",
        label="$\mathregular{CO_2}$",
        element="poly",
        fill=False,
        cumulative=True,
        stat="percent",
        ax=ax,
        bins=range(0, int(flights_df["distance_km"].max()) + 50, 50),
    )

    ax.legend()

    # Set the title, x-axis label, and y-axis label
    ax.set_title("Metrics cumulative distribution vs flight distance")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Cumulative distribution (%)")

    return fig


def distance_cumul_plot_flights_OS(flights_df):
    sns.set_style("darkgrid")
    # Create a new figure with a single subplot
    fig, ax = plt.subplots(figsize=(10, 6.5))
    # sns.histplot(flights_df, x='distance_km', weights='seats', label='Seats', element='poly',fill=False, cumulative = True, stat='percent', ax=ax,bins=range(0, int(flights_df["distance_km"].max()) + 50, 50),)
    # sns.histplot(flights_df, x='distance_km', weights='ask', label= 'ASK', element='poly',fill=False, cumulative = True, stat='percent',ax=ax,bins=range(0, int(flights_df["distance_km"].max()) + 50, 50),)
    sns.histplot(
        flights_df,
        x="distance_km",
        weights="n_flights",
        label="Flights",
        element="poly",
        fill=False,
        cumulative=True,
        stat="percent",
        ax=ax,
        bins=range(0, int(flights_df["distance_km"].max()) + 50, 50),
    )

    ax.legend()

    # Set the title, x-axis label, and y-axis label
    ax.set_title("Metrics cumulative distribution vs flight distance")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Cumulative distribution (%)")

    return fig


def distance_share_flights(flights_df, value_watched_ctry):
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6.5))
    sns.histplot(
        data=flights_df,
        x="distance_km",
        weights=value_watched_ctry,
        common_norm=False,
        multiple="fill",
        hue="acft_class",
        bins=range(0, int(flights_df["distance_km"].max()) + 500, 500),
        edgecolor="none",
        alpha=0.6,
        ax=ax,
    )
    ax.yaxis.set_major_formatter(formatter)
    ax.set_title(
        "Aircraft class used vs flight distance\nWeighting on:{}".format(
            value_watched_ctry
        )
    )
    ax.set_xlabel("Distance (km)")
    ax.set_xlim(0, int(flights_df["distance_km"].max()) + 500)
    ax.set_ylabel("Aircraft class distribution (%)")
    return fig


def distance_share_dom_int_flights(flights_df, value_watched_ctry):
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6.5))
    sns.histplot(
        data=flights_df,
        x="distance_km",
        weights=value_watched_ctry,
        common_norm=False,
        multiple="fill",
        hue="domestic",
        edgecolor="none",
        bins=range(0, int(flights_df["distance_km"].max()) + 500, 500),
        alpha=0.6,
        ax=ax,
    )
    ax.yaxis.set_major_formatter(formatter)
    ax.legend(title="Flight Type", labels=["Domestic", "International"])
    ax.set_title(
        "Flight type vs flight distance\nWeighting on :{}".format(value_watched_ctry)
    )
    ax.set_xlabel("Distance (km)")
    ax.set_xlim(0, int(flights_df["distance_km"].max()) + 500)
    ax.set_ylabel("Flight type distribution (%)")
    return fig


def aircraft_pie_flights(flights_df, value_watched_flights):
    top_aircraft = (
        flights_df.groupby("acft_icao")[value_watched_flights].sum().nlargest(10)
    )
    other_total = flights_df[value_watched_flights].sum() - top_aircraft.sum()
    top_aircraft.loc["Other"] = other_total
    fig = px.pie(
        values=top_aircraft,
        names=top_aircraft.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Aircraft", "values": value_watched_flights},
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by aircraft model".format(value_watched_flights),
        legend=dict(
            title="Aircraft type:",
        ),
    )
    return fig


def aircraft_user_pie_flights(flights_df, value_watched_flights):
    top_airlines = (
        flights_df.groupby("airline_iata")[value_watched_flights].sum().nlargest(10)
    )
    other_total = flights_df[value_watched_flights].sum() - top_airlines.sum()
    top_airlines.loc["Other"] = other_total
    fig = px.pie(
        values=top_airlines,
        names=top_airlines.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Airline", "values": value_watched_flights},
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by airline".format(value_watched_flights),
        legend=dict(
            title="Aircraft type:",
        ),
    )
    return fig


def aircraft_class_pie_flights(flights_df, value_watched_ctry):
    aircraft_class = flights_df.groupby("acft_class")[value_watched_ctry].sum()
    fig = px.pie(
        values=aircraft_class,
        names=aircraft_class.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Class", "values": value_watched_ctry},
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by aircraft class".format(value_watched_ctry),
        legend=dict(
            title="Aircraft class:",
        ),
    )
    return fig


def dom_share_pie_flights(flights_df, value_watched_ctry):
    df_group = flights_df.groupby("domestic")[value_watched_ctry].sum().reset_index()
    df_group["domestic"] = (
        df_group["domestic"].replace(0, "International").replace(1, "Domestic")
    )
    fig = px.pie(
        values=df_group[value_watched_ctry],
        names=df_group.domestic,
        color_discrete_sequence=px.colors.qualitative.T10,
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by type".format(value_watched_ctry),
        legend=dict(
            title="Flight type:",
        ),
    )
    return fig
