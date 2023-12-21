# @Time : 02/10/2023 10:23
# @Author : a.salgas
# @File : country_level_plots.py
# @Software: PyCharm

import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import random
import matplotlib.pyplot as plt


def countries_map_plot(country_flows, value_watched_ctry):
    # Create the scattergeo figure
    fig = go.Figure()

    meanval = country_flows[
        country_flows["departure_country"] != country_flows["arrival_country"]
    ][value_watched_ctry].mean()

    for i in range(len(country_flows)):
        if country_flows["departure_country"][i] == country_flows["arrival_country"][i]:
            color = "black"
        else:
            color = country_flows["color"][i]
        fig.add_trace(
            go.Scattergeo(
                lon=[
                    country_flows["departure_lon"][i],
                    country_flows["arrival_lon"][i],
                ],
                lat=[
                    country_flows["departure_lat"][i],
                    country_flows["arrival_lat"][i],
                ],
                mode="lines",
                line=dict(
                    width=country_flows[value_watched_ctry][i] / (1.5 * meanval),
                    color=color,
                ),
                opacity=0.8,
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scattergeo(
                lon=[country_flows["arrival_lon"][i]],
                lat=[country_flows["arrival_lat"][i]],
                hoverinfo="text",
                text=[country_flows[value_watched_ctry][i]],
                mode="markers",
                marker=dict(
                    size=[country_flows[value_watched_ctry][i]] / (0.01 * meanval),
                    sizemode="area",
                    color=color,
                    line=dict(width=0.5, color="black"),
                ),
                customdata=[
                    [
                        country_flows["departure_country_name"][i],
                        country_flows["arrival_country_name"][i],
                    ]
                ],
                hovertemplate="Flights from: %{customdata[0]}"
                + " to: "
                + "%{customdata[1]}<br>"
                + value_watched_ctry
                + ": %{text:.0f}<br>"
                + "<extra></extra>",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode="markers",
            marker=dict(
                size=500, color="black", opacity=0.6
            ),  # Define color and size for 'Flights remaining in the zone'
            name="Domestic flights",  # Legend label for this category
        )
    )

    fig.update_geos(showcountries=True)
    fig.update_layout(
        showlegend=True,
        height=800,
        title="Country pair flows of {}".format(value_watched_ctry),
    )
    fig.update_layout(
        margin=dict(l=5, r=5, t=60, b=5),
        legend=dict(
            yanchor="top",
            y=0.9,
            xanchor="right",
            x=0.9,
            bgcolor="rgba(220, 220, 220, 0.7)",
        ),
    )  # Adjust layout margins and padding
    return fig


### Deprecated, too slow

# def distance_ecdf_plot_country(flights_df):
#     sns.set_style("darkgrid")
#     # Create a new figure with a single subplot
#     fig, ax = plt.subplots(figsize=(5,5))
#     sns.ecdfplot(flights_df, x='distance_km', weights='seats', label='Seats',stat='percent', ax=ax)
#     sns.ecdfplot(flights_df, x='distance_km', weights='ask', label= 'ASK', stat='percent',ax=ax)
#     sns.ecdfplot(flights_df, x='distance_km', weights='co2', label= '$\mathregular{CO_2}$',stat='percent', ax=ax)

#     ax.legend()

#     # Set the title, x-axis label, and y-axis label
#     ax.set_title("Metrics cumulative distribution vs flight distance")
#     ax.set_xlabel("Distance (km)")
#     ax.set_ylabel("Cumulative distribution (%)")

#     return fig


def formatter(x, pos):
    del pos
    return str(round(x * 100))


def distance_cumul_plot_country(flights_df):
    sns.set_style("darkgrid")
    # Create a new figure with a single subplot
    fig, ax = plt.subplots(figsize=(10, 6))
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
    ax.set_title("Metrics cumulative distribution vs flight distance.")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Cumulative distribution (%)")

    return fig


def distance_cumul_plot_country_OS(flights_df):
    sns.set_style("darkgrid")
    # Create a new figure with a single subplot
    fig, ax = plt.subplots(figsize=(10, 6))
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
    ax.set_title("Metrics cumulative distribution vs flight distance.")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Cumulative distribution (%)")

    return fig


def distance_share_country(flights_df, value_watched_ctry):
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(
        data=flights_df,
        x="distance_km",
        weights=value_watched_ctry,
        common_norm=False,
        multiple="fill",
        hue="acft_class",
        edgecolor="none",
        bins=range(0, int(flights_df["distance_km"].max()) + 500, 500),
        alpha=0.6,
        ax=ax,
    )
    ax.yaxis.set_major_formatter(formatter)
    ax.set_title(
        "Aircraft class used vs flight distance\nWeighting on:{}".format(
            value_watched_ctry
        )
    )
    ax.set_xlim(0, int(flights_df["distance_km"].max()) + 500)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Aircraft class distribution (%)")
    return fig


def distance_share_dom_int_country(flights_df, value_watched_ctry):
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6))
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
    ax.set_xlim(0, int(flights_df["distance_km"].max()) + 500)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Flight type distribution (%)")
    return fig


def countries_global_plot(country_fixed, value_watched_ctry):
    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=country_fixed["departure_lon"],
            lat=country_fixed["departure_lat"],
            hoverinfo="text",
            text=country_fixed[value_watched_ctry],
            mode="markers",
            marker=dict(
                size=country_fixed[value_watched_ctry]
                / (0.0002 * max(country_fixed[value_watched_ctry])),
                sizemode="area",
                color="#EE9B00",
                line=dict(width=0.5, color="black"),
                opacity=0.8,
            ),
            customdata=country_fixed[["departure_country_name"]],
            hovertemplate="Total departures from: %{customdata[0]}<br>"
            + value_watched_ctry
            + ": %{text:.0f}<br>"
            + "<extra></extra>",
        )
    )
    fig.update_geos(showcountries=True)
    fig.update_layout(
        showlegend=False,
        height=800,
        title="Country values for {}".format(value_watched_ctry),
    )
    fig.update_layout(
        margin=dict(l=5, r=5, t=60, b=5)
    )  # Adjust layout margins and padding
    return fig


def countries_treemap_plot(country_flows, value_watched_ctry):
    fig = px.treemap(
        country_flows,
        path=[
            px.Constant("Total currently selected"),
            "departure_country_name",
            "arrival_country_name",
        ],
        values=value_watched_ctry,
        color_discrete_sequence=px.colors.qualitative.T10,
        color="arrival_country_name",
        title="Treemap for {}".format(value_watched_ctry),
    )

    fig.update_layout(margin=dict(l=5, r=5, t=60, b=5))
    fig.update_traces(
        marker=dict(cornerradius=5),
    )

    if value_watched_ctry == "co2":
        fig.update_traces(
            hovertemplate="Flow=%{id}<br>CO<sub>2</sub>=%{value:.2f} (lg)"
        )
    elif value_watched_ctry == "ask":
        fig.update_traces(hovertemplate="Flow=%{id}<br>ASK=%{value:.2f}")
    elif value_watched_ctry == "seats":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Seats=%{value:.2f}")
    elif value_watched_ctry == "n_flights":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Flights=%{value:.2f}")

    return fig


#### Deprecated version, too slow
# def distance_histogram_plot_country(flights_df, value_watched_ctry):
#     fig = px.histogram(
#         flights_df,
#         x="distance_km",
#         y=value_watched_ctry,
#         histfunc="sum",
#         color_discrete_sequence=px.colors.qualitative.T10,
#         title='Repartition of {} by flight distance'.format(value_watched_ctry),

#     )

#     fig.update_traces(xbins=dict(
#         start=0.0,
#         end=flights_df.distance_km.max(),
#         size=500))

#     fig.update_layout(
#         # title="Histogram of CO2 Emissions by Distance and Arrival Continent",
#         xaxis_title="Distance (km)",
#         yaxis_title=value_watched_ctry,
#         showlegend=False,
#     )

#     fig.update_layout(
#         margin=dict(l=5, r=5, t=60, b=5),
#     )

#     if value_watched_ctry == 'co2':
#         fig.update_traces(hovertemplate='Distance group (km)=%{x}<br>CO2 (kg)=%{y:.0f}<extra></extra>')
#     elif value_watched_ctry == 'ask':
#         fig.update_traces(hovertemplate='Distance group (km)=%{x}<br>ASK=%{y:.0f}<extra></extra>')
#     elif value_watched_ctry == 'seats':
#         fig.update_traces(hovertemplate='Distance group (km)=%{x}<br>Seats=%{y:.0f}<extra></extra>')
#     return fig


def distance_histogram_plot_country(flights_df, value_watched_ctry):
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6))
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


def aircraft_pie(flights_df, value_watched_ctry):
    top_aircraft = (
        flights_df.groupby("acft_icao")[value_watched_ctry].sum().nlargest(10)
    )
    other_total = flights_df[value_watched_ctry].sum() - top_aircraft.sum()
    top_aircraft.loc["Other"] = other_total
    fig = px.pie(
        values=top_aircraft,
        names=top_aircraft.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Aircraft", "values": value_watched_ctry},
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by aircraft".format(value_watched_ctry),
        legend=dict(
            title="Aircraft type:",
        ),
    )
    return fig


def aircraft_class_pie(flights_df, value_watched_ctry):
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


def aircraft_user_pie(flights_df, value_watched_ctry):
    top_airlines = (
        flights_df.groupby("airline_iata")[value_watched_ctry].sum().nlargest(10)
    )
    other_total = flights_df[value_watched_ctry].sum() - top_airlines.sum()
    top_airlines.loc["Other"] = other_total
    fig = px.pie(
        values=top_airlines,
        names=top_airlines.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Airline", "values": value_watched_ctry},
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by airline".format(value_watched_ctry),
        legend=dict(
            title="Airline IATA code:",
        ),
    )
    return fig


def dom_share_pie(flights_df, value_watched_ctry):
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
