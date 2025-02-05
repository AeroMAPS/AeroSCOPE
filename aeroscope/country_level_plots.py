# @Time : 02/10/2023 10:23
# @Author : a.salgas
# @File : country_level_plots.py
# @Software: PyCharm

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def countries_map_plot(country_flows, value_watched_ctry):
    # Create the scattergeo figure
    fig = go.Figure()

    meanval = country_flows[country_flows["departure_country"] != country_flows["arrival_country"]][
        value_watched_ctry
    ].mean()

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
                + ": %{text:.2e}<br>"
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


def formatter(x, pos):
    del pos
    return str(round(x * 100))


def distance_cumul_plot_country(flights_df):
    fig = go.Figure()

    # Define bins for a quick cumulative distribution rendering. 10 km
    bins = list(range(0, int(flights_df["distance_km"].max()) + 10, 10))

    # Cumulative distributions for each metric
    # Seats
    hist_seats, edges_seats = (
        flights_df["Seats"].groupby(pd.cut(flights_df["distance_km"], bins)).sum(),
        bins[1:],
    )
    hist_cumul_seats = hist_seats.cumsum() / hist_seats.sum() * 100
    fig.add_trace(
        go.Scatter(
            x=edges_seats,
            y=hist_cumul_seats,
            mode="lines",
            name="Seats",
            line=dict(color="#1f77b4", width=2),
            hovertemplate="%{y:.2f} %",
        )
    )

    # ASK
    hist_ask, edges_ask = (
        flights_df["ASK"].groupby(pd.cut(flights_df["distance_km"], bins)).sum(),
        bins[1:],
    )
    hist_cumul_ask = hist_ask.cumsum() / hist_ask.sum() * 100
    fig.add_trace(
        go.Scatter(
            x=edges_ask,
            y=hist_cumul_ask,
            mode="lines",
            name="ASK",
            line=dict(color="#ff7f0e", width=2),
            hovertemplate="%{y:.2f} %",
        )
    )

    #  CO2
    hist_co2, edges_co2 = (
        flights_df["CO2 (kg)"].groupby(pd.cut(flights_df["distance_km"], bins)).sum(),
        bins[1:],
    )
    hist_cumul_co2 = hist_co2.cumsum() / hist_co2.sum() * 100
    fig.add_trace(
        go.Scatter(
            x=edges_co2,
            y=hist_cumul_co2,
            mode="lines",
            name="CO2 (kg)",
            line=dict(color="#2ca02c", width=2),
            hovertemplate="%{y:.2f} %",
        )
    )

    # Formatting
    fig.update_layout(
        title="Metrics cumulative distribution vs flight distance",
        xaxis_title="Distance (km)",
        yaxis_title="Cumulative distribution (%)",
        template="plotly_white",
        hovermode="x",
        margin=dict(l=60, r=60, t=60, b=60),
        legend=dict(
            x=0.82,
            y=0.08,
            bgcolor="rgba(255, 255, 255, 0.5)",
        ),
    )

    return fig


def distance_cumul_plot_country_OS(flights_df):
    fig = go.Figure()

    # Define bins for a quick cumulative distribution rendering. 10 km
    bins = list(range(0, int(flights_df["distance_km"].max()) + 10, 10))

    # Cumulative distributions for each metric
    # N Flights
    hist_flights, edges_flights = (
        flights_df["n_flights"].groupby(pd.cut(flights_df["distance_km"], bins)).sum(),
        bins[1:],
    )
    hist_cumul_flights = hist_flights.cumsum() / hist_flights.sum() * 100
    fig.add_trace(
        go.Scatter(
            x=edges_flights,
            y=hist_cumul_flights,
            mode="lines",
            name="Number of flights",
            line=dict(color="#1f77b4", width=2),
            hovertemplate="%{y:.2f} %",
        )
    )

    # Formatting
    fig.update_layout(
        title="Metrics cumulative distribution vs flight distance",
        xaxis_title="Distance (km)",
        yaxis_title="Cumulative distribution (%)",
        template="plotly_white",
        hovermode="x",
        margin=dict(l=60, r=60, t=60, b=60),
        legend=dict(
            x=0.82,
            y=0.08,
            bgcolor="rgba(255, 255, 255, 0.5)",
        ),
    )

    return fig


def distance_share_country(flights_df, value_watched_ctry):
    fig = go.Figure()

    # Define bins (500 km intervals)
    bin_width = 500
    bins = list(range(0, int(flights_df["distance_km"].max()) + bin_width, bin_width))
    bin_centers = [b + bin_width / 2 for b in bins[:-1]]  # Midpoints of each bin

    # Compute shares without modifying flights_df
    grouped = (
        flights_df.groupby([pd.cut(flights_df["distance_km"], bins, right=False), "acft_class"])[
            value_watched_ctry
        ]
        .sum()
        .unstack(fill_value=0)
    )
    share_df = grouped.div(grouped.sum(axis=1), axis=0) * 100  # Convert to percentage

    bin_ranges = [f"{b - bin_width / 2}-{b + bin_width /2}" for b in bin_centers]

    # Add traces for each aircraft class (stacked bars)
    for acft_class in share_df.columns:
        fig.add_trace(
            go.Bar(
                x=bin_centers,  # Use the center of bins for tick alignment
                y=share_df[acft_class],
                name=acft_class,
                width=bin_width,  # Ensure bars have correct width
                opacity=0.7,  # Add transparency to the bars
                hovertemplate=(
                    "Distance %{customdata} km:<br>"  # Bin range precomputed
                    "Share of " + acft_class + ": %{y:.2f} %<extra></extra>"
                ),
                customdata=bin_ranges,  # Pass the bin range as customdata
                marker=dict(
                    line=dict(width=0)  # Remove the white line between bars
                ),
            )
        )

    # Formatting (Stacked Histogram)
    fig.update_layout(
        title=f"Aircraft class used vs flight distance<br>Weighting on: {value_watched_ctry}",
        xaxis_title="Distance (km)",
        yaxis_title="Aircraft class distribution (%)",
        template="plotly_white",
        hovermode="closest",
        barmode="stack",  # Stacked histogram style
        yaxis=dict(tickformat=".0f", range=[0, 100]),
        xaxis=dict(
            tickmode="linear",
            dtick=bin_width,
            range=[0, bins[-1]],
            title="Distance (km)",
        ),
        legend=dict(x=0.82, y=0.08, bgcolor="rgba(255, 255, 255, 0.5)"),
        colorway=px.colors.qualitative.T10,
        margin=dict(l=60, r=60, t=60, b=60),
    )

    return fig


def distance_share_dom_int_country(flights_df, value_watched_ctry):
    fig = go.Figure()

    bin_width = 500
    bins = list(range(0, int(flights_df["distance_km"].max()) + bin_width, bin_width))
    bin_centers = [b + bin_width / 2 for b in bins[:-1]]

    grouped = (
        flights_df.groupby([pd.cut(flights_df["distance_km"], bins), "domestic"])[
            value_watched_ctry
        ]
        .sum()
        .unstack(fill_value=0)
    )

    share_df = grouped.div(grouped.sum(axis=1), axis=0) * 100

    bin_ranges = [f"{b - bin_width / 2}-{b + bin_width / 2}" for b in bin_centers]

    for flight_type in share_df.columns:
        fig.add_trace(
            go.Bar(
                x=bin_centers,
                y=share_df[flight_type],
                name="Domestic" if flight_type == 1 else "International",
                width=bin_width,
                opacity=0.7,
                hovertemplate=("Distance %{customdata} km:<br>" + "%{y:.2f} %<extra></extra>"),
                customdata=bin_ranges,
                marker=dict(line=dict(width=0)),
            )
        )

    fig.update_layout(
        title=f"Flight type vs flight distance<br>Weighting on: {value_watched_ctry}",
        xaxis_title="Distance (km)",
        yaxis_title="Flight type distribution (%)",
        template="plotly_white",
        hovermode="x",
        barmode="stack",
        yaxis=dict(tickformat=".0f", range=[0, 100]),  # Ensure % scaling
        xaxis=dict(
            tickmode="linear",
            dtick=bin_width,
            range=[0, bins[-1]],
        ),
        legend_title="Flight Type",
        legend=dict(x=0.82, y=0.08, bgcolor="rgba(255, 255, 255, 0.5)"),
        colorway=px.colors.qualitative.T10,
        margin=dict(l=60, r=60, t=60, b=60),
    )

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
            + ": %{text:.2e}<br>"
            + "<extra></extra>",
        )
    )
    fig.update_geos(showcountries=True)
    fig.update_layout(
        showlegend=False,
        height=800,
        title="Country values for {}".format(value_watched_ctry),
    )
    fig.update_layout(margin=dict(l=5, r=5, t=60, b=5))  # Adjust layout margins and padding
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

    if value_watched_ctry == "CO2 (kg)":
        fig.update_traces(hovertemplate="Flow=%{id}<br>CO<sub>2</sub>=%{value:.2e} (kg)")
    elif value_watched_ctry == "ASK":
        fig.update_traces(hovertemplate="Flow=%{id}<br>ASK=%{value:.2e}")
    elif value_watched_ctry == "Seats":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Seats=%{value:.2e}")
    elif value_watched_ctry == "n_flights":
        fig.update_traces(hovertemplate="Flow=%{id}<br>Flights=%{value:.2e}")

    return fig


def distance_histogram_plot_country(flights_df, value_watched_ctry):
    fig = go.Figure()

    # Define bins for the histogram (500 km intervals)
    bin_width = 500
    bins = list(range(0, int(flights_df["distance_km"].max()) + bin_width, bin_width))
    bin_centers = [b + bin_width / 2 for b in bins[:-1]]  # Midpoints of each bin

    bin_ranges = [f"{b - bin_width / 2}-{b + bin_width / 2}" for b in bin_centers]

    # Compute the sum of values in each bin
    grouped = flights_df.groupby(pd.cut(flights_df["distance_km"], bins))[value_watched_ctry].sum()

    # Add bars for the histogram
    fig.add_trace(
        go.Bar(
            x=bin_centers,  # Use the center of bins for tick alignment
            y=grouped,
            name=value_watched_ctry,
            width=bin_width,  # Ensure bars have correct width
            marker=dict(color="#EE9B00", opacity=0.5),
            hovertemplate=(
                "Distance %{customdata} km:<br>" + value_watched_ctry + " %{y:.2e}<extra></extra>"
            ),
            customdata=bin_ranges,
        )
    )

    # Formatting
    fig.update_layout(
        title=f"Repartition of {value_watched_ctry} by flight distance",
        xaxis_title="Distance (km)",
        yaxis_title=value_watched_ctry,
        template="plotly_white",
        hovermode="closest",
        bargap=0.3,
        xaxis=dict(
            tickmode="linear",
            dtick=bin_width,
            range=[0, bins[-1]],
        ),
        margin=dict(l=60, r=60, t=60, b=60),
    )

    return fig


def aircraft_pie(flights_df, value_watched_ctry):
    top_aircraft = flights_df.groupby("acft_icao")[value_watched_ctry].sum().nlargest(10)
    other_total = flights_df[value_watched_ctry].sum() - top_aircraft.sum()
    top_aircraft.loc["Other"] = other_total
    fig = px.pie(
        values=top_aircraft,
        names=top_aircraft.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Aircraft", "values": value_watched_ctry},
    )
    fig.update_traces(
        textposition="inside", hovertemplate=value_watched_ctry + " for %{label}: %{value:.2e}"
    )
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
    fig.update_traces(
        textposition="inside", hovertemplate=value_watched_ctry + " for %{label}: %{value:.2e}"
    )
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by aircraft class".format(value_watched_ctry),
        legend=dict(
            title="Aircraft class:",
        ),
    )
    return fig


def aircraft_user_pie(flights_df, value_watched_ctry):
    top_airlines = flights_df.groupby("airline_iata")[value_watched_ctry].sum().nlargest(10)
    other_total = flights_df[value_watched_ctry].sum() - top_airlines.sum()
    top_airlines.loc["Other"] = other_total
    fig = px.pie(
        values=top_airlines,
        names=top_airlines.index,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"names": "Airline", "values": value_watched_ctry},
    )
    fig.update_traces(
        textposition="inside", hovertemplate=value_watched_ctry + " for %{label}: %{value:.2e}"
    )
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
    df_group["domestic"] = df_group["domestic"].replace(0, "International").replace(1, "Domestic")
    fig = px.pie(
        values=df_group[value_watched_ctry],
        names=df_group.domestic,
        color_discrete_sequence=px.colors.qualitative.T10,
    )
    fig.update_traces(
        textposition="inside", hovertemplate=value_watched_ctry + " for %{label}: %{value:.2e}"
    )
    fig.update_layout(
        margin=dict(l=60, r=60, t=60, b=60),
        title="{} by type".format(value_watched_ctry),
        legend=dict(
            title="Flight type:",
        ),
    )
    return fig
