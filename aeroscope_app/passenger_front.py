# @Time : 07/12/2023 16:58
# @Author : a.salgas
# @File : passenger_front.py
# @Software: PyCharm


### PAX FRONTEND
import pax_level_plots
import ipyvuetify as v
from ipywidgets import Output
from IPython.display import display
from functools import partial
import numpy as np


class PassengerTab:
    def __init__(self, aeroscopedataclass):
        ## define widgets

        # Airport filter
        self.autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airport IATA",
            items=list(aeroscopedataclass.flights_df.iata_departure.unique()),
            multiple=False,
            variant="outlined",
        )

        self.output_1 = Output()

        self._render_initial_plots()
        self._make_connections(aeroscopedataclass)
        self._make_layout()

    def _make_connections(self, dataclass):
        self.autocomplete.observe(
            partial(self._plot1_update, dataclass=dataclass), names="v_model"
        )

    def _render_initial_plots(self):
        with self.output_1:
            print("Please select a departure")

    def _plot1_update(self, change, dataclass):
        filtered_pax_departure = self.autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_pax_departure:
            filtered_flights_df = dataclass.flights_df[
                dataclass.flights_df["iata_departure"] == filtered_pax_departure
            ].reset_index()
            with self.output_1:
                self.output_1.clear_output(wait=True)
                filtered_flights_df = filtered_flights_df[
                    ~filtered_flights_df["CO2 Ppax"].isin([0, np.nan, np.inf, -np.inf])
                ]
                flights_df_od = (
                    filtered_flights_df.groupby(["iata_departure", "iata_arrival"])
                    .agg(
                        {
                            "acft_icao": ", ".join,
                            "airline_iata": ", ".join,
                            "departure_lon": "first",
                            "departure_lat": "first",
                            "arrival_lon": "first",
                            "arrival_lat": "first",
                            "CO2 Ppax": "mean",
                            "seats": "sum",
                        }
                    )
                    .reset_index()
                )

                # Remove flights if not enough seats for this mode (avoid exotic routes)
                flights_df_od = flights_df_od[
                    flights_df_od["seats"] > 20000
                ].reset_index()
                # Apply the function to the DataFrame column
                flights_df_od["airline_iata"] = flights_df_od["airline_iata"].apply(
                    remove_duplicates
                )
                flights_df_od["acft_icao"] = flights_df_od["acft_icao"].apply(
                    remove_duplicates
                )
                fig_pax_1 = pax_level_plots.pax_map_plot(flights_df_od)

                display(fig_pax_1)

    def _make_layout(self):
        h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        ### PAGE ARCHITECTURE

        ## Define the rows

        row_disclaimer_pax = v.Col(
            # cols='12',  # Adjust the column width as needed
            children=[
                v.Card(
                    outlined=False,
                    elevation=0,
                    style_="width: 100%",
                    children=[
                        v.CardText(
                            children=[
                                "Caution: Accuracy is limited (particularly in some regions) in this mode. Data must therefore be used with the necessary precautions."
                            ],
                            class_="text-center teal--text darken-4",
                            style_="font-size: 16px;",
                        ),
                    ],
                ),
            ],
        )

        col_selects_pax = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=False,
            cols="3",
            class_="mb-4",  # Add margin at the bottom
            children=[
                v.Row(
                    # cols='2',  # Adjust the column width as needed
                    children=[
                        v.Card(
                            outlined=False,
                            elevation=0,
                            style_="height: 100%",
                            children=[
                                v.CardText(
                                    children=[
                                        v.CardTitle(children="Departure"),
                                        self.autocomplete,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
                v.Row(
                    # cols='2',  # Adjust the column width as needed
                    children=[
                        v.Card(
                            outlined=False,
                            elevation=0,
                            style_="height: 100%",
                            children=[
                                v.CardText(
                                    children=[
                                        v.Btn(
                                            children=["IATA code?"],
                                            _metadata={"mount_id": "link_button"},
                                            href="https://www.iata.org/en/publications/directories/code-search/",
                                            target="_blank",
                                            color="light-blue-darken-4",
                                            class_="ma-2",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        row_mega_map_pax = v.Row(
            children=[
                v.Flex(
                    md12=True,
                    children=[
                        v.Col(
                            xs12=True,
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
                                        v.CardText(
                                            children=[
                                                self.output_1,
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                            style_="max-width: 100%;",
                        ),
                    ],
                ),
            ],
        )

        col_plots_pax = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=True,
            # cols='10',
            # class_='mb-4',  # Add margin at the bottom
            children=[row_disclaimer_pax, row_mega_map_pax],
        )
        self.layout = v.Row(children=[col_selects_pax, v_divider, col_plots_pax])


# Function to remove duplicates from a comma-separated string
def remove_duplicates(input_str):
    # Split the string into a list of substrings
    substrings = input_str.split(", ")
    # Remove duplicates and preserve the order
    unique_substrings = list(dict.fromkeys(substrings))
    # Join the unique substrings back into a single string
    result_str = ", ".join(unique_substrings)
    return result_str
