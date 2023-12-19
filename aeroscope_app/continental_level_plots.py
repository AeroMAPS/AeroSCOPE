# @Time : 02/10/2023 10:20
# @Author : a.salgas
# @File : continental_level_plots.py
# @Software: PyCharm


import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


color_discrete_map = {
    "AS": "#EE9B00",
    "AF": "#E9D8A6",
    "EU": "#005F73",
    "NA": "#9B2226",
    "OC": "#94D2BD",
    "SA": "#BB3E03",
    "(?)": "lightgrey",
}


def continental_treemap_plot(continental_flows, value_watched_conti):
    if len(continental_flows) > 0:
        fig = px.treemap(
            continental_flows,
            path=[
                px.Constant("World"),
                "departure_continent_name",
                "arrival_continent_name",
            ],
            values=value_watched_conti,
            color="arrival_continent",
            color_discrete_map=color_discrete_map,
            title="Treemap for {}".format(value_watched_conti),
        )

        fig.update_layout(margin=dict(l=5, r=5, t=60, b=5))

        if value_watched_conti == "CO2 (Mt)":
            fig.update_traces(
                hovertemplate="Flow=%{id}<br>CO<sub>2</sub>=%{value:.2f} (Mt)"
            )
            fig.update_traces(
                marker=dict(cornerradius=5),
                textinfo="label+value+percent entry",
                texttemplate="%{label}<br>%{value:.0f} Mt<br>%{percentEntry}",
            )
        elif value_watched_conti == "ASK (Bn)":
            fig.update_traces(hovertemplate="Flow=%{id}<br>ASK=%{value:.2f} (Bn)")
            fig.update_traces(
                marker=dict(cornerradius=5),
                textinfo="label+value+percent entry",
                texttemplate="%{label}<br>%{value:.1f} Bn<br>%{percentEntry}",
            )
        elif value_watched_conti == "Seats (Mn)":
            fig.update_traces(hovertemplate="Flow=%{id}<br>Seats=%{value:.2f} (Mn)")
            fig.update_traces(
                marker=dict(cornerradius=5),
                textinfo="label+value+percent entry",
                texttemplate="%{label}<br>%{value:.1f} Mn<br>%{percentEntry}",
            )
        elif value_watched_conti == "n_flights":
            fig.update_traces(hovertemplate="Flow=%{id}<br>Flights=%{value:.2f} (Mn)")
            fig.update_traces(
                marker=dict(cornerradius=5),
                textinfo="label+value+percent entry",
                texttemplate="%{label}<br>%{value:.1f} Mn<br>%{percentEntry}",
            )

        return fig
    else:
        return "Please select at least one continent!"


### plotly histogramm deprecated, too slow

# def distance_histogram_plot_continent(flights_df_conti, value_watched_conti):
#     if len(flights_df_conti)>0:
#         fig = px.histogram(
#             flights_df_conti,
#             x="distance_km",
#             y=value_watched_conti,
#             color="arrival_continent",
#             color_discrete_map=color_discrete_map,
#             title='Repartition of {} by flight distance'.format(value_watched_conti),
#             histfunc="sum",
#         )

#         fig.update_traces(xbins=dict(
#             start=0.0,
#             end=flights_df_conti.distance_km.max(),
#             size=500))

#         fig.update_layout(
#             # title="Histogram of CO2 Emissions by Distance and Arrival Continent",
#             xaxis_title="Distance (km)",
#             yaxis_title=value_watched_conti,
#             legend_title="Arrival Continent",
#             showlegend=True,
#         )
#         fig.update_layout(
#             margin=dict(l=5, r=5, t=60, b=5),
#             legend=dict(
#                 yanchor="top",
#                 xanchor="right",
#                 x=0.9,
#                 bgcolor='rgba(220, 220, 220, 0.7)'
#             )
#         )

#         fig.update_layout()
#         if value_watched_conti == 'CO2 (Mt)':
#             fig.update_traces(
#                 hovertemplate='Arrival Continent=%{customdata}<br>Distance group (km)=%{x}<br>CO2 (Mt)=%{y:.2f}<extra></extra>',
#                 customdata=flights_df_conti['arrival_continent_name'])
#         elif value_watched_conti == 'ASK (Bn)':
#             fig.update_traces(
#                 hovertemplate='Arrival Continent=%{customdata}<br>Distance group (km)=%{x}<br>ASK (Bn)=%{y:.2f}<extra></extra>',
#                 customdata=flights_df_conti['arrival_continent_name'])
#         elif value_watched_conti == 'Seats (Mn)':
#             fig.update_traces(
#                 hovertemplate='Arrival Continent=%{customdata}<br>Distance group (km)=%{x}<br>Seats (Mn)=%{y:.2f}<extra></extra>',
#                 customdata=flights_df_conti['arrival_continent_name'])

#         return fig
#     else:
#         return('Please select at least one continent!')


def distance_histogram_plot_continent(flights_df_conti, value_watched_conti):
    plt.ioff()
    if len(flights_df_conti) > 0:
        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize=(10, 6.5))
        sns.histplot(
            data=flights_df_conti,
            x="distance_km",
            weights=value_watched_conti,
            hue="arrival_continent",
            element="step",
            multiple="stack",
            palette=color_discrete_map,
            common_norm=False,
            bins=range(0, int(flights_df_conti["distance_km"].max()) + 500, 500),
            alpha=1,
            ax=ax,
        )
        ax.set_title("Repartition of {} by flight distance".format(value_watched_conti))
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel(value_watched_conti)
        return fig
    else:
        print("Please select at least one continent!")
        return


def continental_map_plot(conti_scatter, continental_flows_non_dir, value_watched_conti):
    # Create the scattergeo figure
    if len(conti_scatter) > 0:
        fig = go.Figure()
        for i in range(len(continental_flows_non_dir)):
            fig.add_trace(
                go.Scattergeo(
                    lon=[
                        continental_flows_non_dir["dep_lon"][i],
                        continental_flows_non_dir["arr_lon"][i],
                    ],
                    lat=[
                        continental_flows_non_dir["dep_lat"][i],
                        continental_flows_non_dir["arr_lat"][i],
                    ],
                    mode="lines",
                    line=dict(
                        width=continental_flows_non_dir[value_watched_conti][i]
                        / (0.02 * max(continental_flows_non_dir[value_watched_conti])),
                        color="#EE9B00",
                    ),
                    opacity=1,
                    showlegend=False,
                )
            )

        conti_scatter.sort_values(by=value_watched_conti, ascending=False, inplace=True)
        # Define the color mapping
        color_map = {True: "#005F73", False: "#EE9B00"}

        fig.add_trace(
            go.Scattergeo(
                lon=conti_scatter["dep_lon"],
                lat=conti_scatter["dep_lat"],
                text=conti_scatter[value_watched_conti],
                mode="markers",
                marker=dict(
                    size=conti_scatter[value_watched_conti]
                    / (0.0001 * max(conti_scatter[value_watched_conti])),
                    sizemode="area",
                    color=[color_map[val] for val in conti_scatter["inside"]],
                    line=dict(width=0.5, color="white"),
                    opacity=1,
                    # name='yy'
                ),
                customdata=conti_scatter[["departure_continent_name", "inside"]],
                hovertemplate="Departure Continent: %{customdata[0]}<br>"
                + "Flights inside zone: %{customdata[1]}<br>"
                + value_watched_conti
                + ": %{text:.1f}<br>"
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
                    size=50, color="#005F73"
                ),  # Define color and size for 'Flights remaining in the zone'
                name="Flights remaining in the zone",  # Legend label for this category
            )
        )

        fig.add_trace(
            go.Scattergeo(
                lon=[None],
                lat=[None],
                mode="markers",
                marker=dict(
                    size=50, color="#EE9B00"
                ),  # Define color and size for 'Flights going out of the zone'
                name="Flights going out of the zone",  # Legend label for this category
            )
        )

        fig.update_layout(
            showlegend=True,
            height=800,
            title="Continental flows of {}".format(value_watched_conti),
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
    else:
        return "Please select at least one continent!"
