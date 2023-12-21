# @Time : 07/12/2023 15:52
# @Author : a.salgas
# @File : detailled_front.py
# @Software: PyCharm
import flight_level_plots
import ipyvuetify as v
from ipywidgets import Output
from IPython.display import display
from functools import partial


class DetailledTab:
    def __init__(self, aeroscopedataclass):
        self.in_class_flights_df = aeroscopedataclass.flights_df.copy()

        ## define widgets
        # Airline filter
        self.airline_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airline IATA",
            items=list(aeroscopedataclass.flights_df.airline_iata.unique()),
            multiple=True,
            variant="outlined",
        )

        # Aircraft filter
        self.aircraft_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Aircraft ICAO",
            items=list(aeroscopedataclass.flights_df.acft_icao.unique()),
            multiple=True,
            variant="outlined",
        )

        # Airport filter
        self.departure_airport_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airport IATA",
            items=list(aeroscopedataclass.flights_df.iata_departure.unique()),
            multiple=True,
            variant="outlined",
        )

        self.arrival_airport_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airport IATA",
            items=list(aeroscopedataclass.flights_df.iata_arrival.unique()),
            multiple=True,
            variant="outlined",
        )
        # Value watched
        self.value_watched_radio = v.RadioGroup(
            v_model="co2",  # Set the initial selected value here
            row=True,
            children=[
                v.Radio(label="CO\u2082 (kg)", value="co2"),
                v.Radio(label="ASK", value="ask"),
                v.Radio(label="SEATS", value="seats"),
            ],
            class_="mb-3",
        )

        # Button to reset all filters
        self.reset_all_button = v.Btn(
            children=["Reset All"], color="light-blue-darken-4", class_="ma-2"
        )

        # Toggle button switch between the two main figures
        self.toggle_button_plot1 = v.BtnToggle(
            v_model="map",
            variant="outlined",
            children=[
                v.Btn(value="map", children=["Map"], variant="outlined"),
                v.Btn(value="tree", children=["Tree"], variant="outlined"),
            ],
        )

        # v-btn-toggle switch between the two main figures
        self.toggle_button_plot2 = v.BtnToggle(
            v_model="hist",
            children=[
                v.Btn(value="hist", children=["Histogram"]),
                v.Btn(value="ecdf", children=["Cumulative"]),
                v.Btn(value="kde_acft", children=["Aircraft type"]),
                v.Btn(value="kde_dom", children=["Flight Type"]),
            ],
        )

        self.toggle_button_plot3 = v.BtnToggle(
            v_model="acft",
            variant="text",
            children=[
                v.Btn(value="acft", children=["Aircraft Type"]),
                v.Btn(value="acft_class", children=["Aircraft Class"]),
                v.Btn(value="airline", children=["Airline"]),
                v.Btn(value="dom", children=["Flight Type"]),
            ],
        )

        self.output_1 = Output()
        self.output_2 = Output()
        self.output_3 = Output()

        self._render_initial_plots(aeroscopedataclass)
        self._make_connections(aeroscopedataclass)
        self._make_layout()

    def _make_connections(self, dataclass):
        self.reset_all_button.on_event(
            "click", partial(self._reset_all, dataclass=dataclass)
        )

        self.departure_airport_autocomplete.observe(
            partial(self._data_update_dep, dataclass=dataclass), names="v_model"
        )
        self.arrival_airport_autocomplete.observe(
            partial(self._data_update_arr, dataclass=dataclass), names="v_model"
        )
        self.airline_autocomplete.observe(
            partial(self._data_update_airline, dataclass=dataclass), names="v_model"
        )
        self.aircraft_autocomplete.observe(
            partial(self._data_update_aircraft, dataclass=dataclass), names="v_model"
        )

        self.value_watched_radio.observe(self._plot1_update, names="v_model")
        self.value_watched_radio.observe(self._plot2_update, names="v_model")
        self.value_watched_radio.observe(self._plot3_update, names="v_model")

        self.toggle_button_plot1.observe(self._plot1_update, names="v_model")
        self.toggle_button_plot2.observe(self._plot2_update, names="v_model")
        self.toggle_button_plot3.observe(self._plot3_update, names="v_model")

    def _reset_all(self, widget, event, data, dataclass):
        self.departure_airport_autocomplete.v_model = list()
        self.arrival_airport_autocomplete.v_model = list()
        self.airline_autocomplete.v_model = list()
        self.aircraft_autocomplete.v_model = list()
        self.departure_airport_autocomplete.items = (
            dataclass.flights_df.iata_departure.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            dataclass.flights_df.iata_arrival.unique().tolist()
        )
        self.airline_autocomplete.items = (
            dataclass.flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            dataclass.flights_df.acft_icao.unique().tolist()
        )

    def _render_initial_plots(self, dataclass):
        with self.output_1:
            print("Too much data selected for flight map rendering")

        with self.output_2:
            fig_flights_2 = flight_level_plots.distance_histogram_plot_flights(
                dataclass.flights_df, "co2"
            )
            display(fig_flights_2)

        with self.output_3:
            fig_flights_3 = flight_level_plots.aircraft_pie_flights(
                dataclass.flights_df, "co2"
            )
            display(fig_flights_3)

    def _data_update_airline(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_departure"].isin(
                    filtered_departure_airport
                )
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_arrival"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.airline_autocomplete.v_model) == 0:
            self.airline_autocomplete.items = (
                self.in_class_flights_df.airline_iata.unique().tolist()
            )

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _data_update_aircraft(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_departure"].isin(
                    filtered_departure_airport
                )
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_arrival"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.aircraft_autocomplete.v_model) == 0:
            self.aircraft_autocomplete.items = (
                self.in_class_flights_df.acft_icao.unique().tolist()
            )

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _data_update_arr(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_departure"].isin(
                    filtered_departure_airport
                )
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_arrival"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.arrival_airport_autocomplete.v_model) == 0:
            self.arrival_airport_autocomplete.items = (
                self.in_class_flights_df.iata_arrival.unique().tolist()
            )

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _data_update_dep(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_departure"].isin(
                    filtered_departure_airport
                )
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_arrival"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.departure_airport_autocomplete.v_model) == 0:
            self.departure_airport_autocomplete.items = (
                self.in_class_flights_df.iata_departure.unique().tolist()
            )

        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _plot1_update(self, change):
        value_watched_flights = self.value_watched_radio.v_model
        active_main_graph_flights = self.toggle_button_plot1.v_model

        if len(self.in_class_flights_df) < 20000:
            with self.output_1:
                self.output_1.clear_output(wait=True)
                if active_main_graph_flights == "map":
                    # # grouping flighst on and OD basis, and concatenating airline and aircraft information

                    flights_df_od = (
                        self.in_class_flights_df.groupby(
                            ["iata_departure", "iata_arrival"]
                        )
                        .agg(
                            {
                                "acft_icao": ", ".join,
                                "airline_iata": ", ".join,
                                "departure_lon": "first",
                                "departure_lat": "first",
                                "arrival_lon": "first",
                                "arrival_lat": "first",
                                "co2": "sum",
                                "ask": "sum",
                                "seats": "sum",
                            }
                        )
                        .reset_index()
                    )

                    # Apply the function to the DataFrame column
                    flights_df_od["airline_iata"] = flights_df_od["airline_iata"].apply(
                        remove_duplicates
                    )
                    flights_df_od["acft_icao"] = flights_df_od["acft_icao"].apply(
                        remove_duplicates
                    )
                    fig_flights_1 = flight_level_plots.flights_map_plot(
                        flights_df_od, value_watched_flights
                    )
                else:
                    fig_flights_1 = flight_level_plots.flights_treemap_plot(
                        self.in_class_flights_df, value_watched_flights
                    )

                display(fig_flights_1)

        else:
            with self.output_1:
                self.output_1.clear_output(wait=True)
                print("Too much data selected for flight map rendering")

    def _plot2_update(self, change):
        value_watched_flights = self.value_watched_radio.v_model
        active_analysis_graph_flights = self.toggle_button_plot2.v_model

        with self.output_2:
            self.output_2.clear_output(wait=True)
            if active_analysis_graph_flights == "hist":
                fig_flights_2 = flight_level_plots.distance_histogram_plot_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            elif active_analysis_graph_flights == "ecdf":
                fig_flights_2 = flight_level_plots.distance_cumul_plot_flights(
                    self.in_class_flights_df
                )
            elif active_analysis_graph_flights == "kde_acft":
                fig_flights_2 = flight_level_plots.distance_share_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            else:
                fig_flights_2 = flight_level_plots.distance_share_dom_int_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            display(fig_flights_2)

    def _plot3_update(self, change):
        value_watched_flights = self.value_watched_radio.v_model
        active_pie_graph_flights = self.toggle_button_plot3.v_model

        with self.output_3:
            self.output_3.clear_output(wait=True)
            if active_pie_graph_flights == "acft":
                fig_flights_3 = flight_level_plots.aircraft_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            elif active_pie_graph_flights == "acft_class":
                fig_flights_3 = flight_level_plots.aircraft_class_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            elif active_pie_graph_flights == "airline":
                fig_flights_3 = flight_level_plots.aircraft_user_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            else:
                fig_flights_3 = flight_level_plots.dom_share_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            display(fig_flights_3)

    def _make_layout(self):
        h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        ### PAGE ARCHITECTURE

        ## Define the rows

        row_disclaimer = v.Col(
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

        col_selects_flights = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=False,
            cols="3",
            class_="mb-4",  # Add margin at the bottom
            children=[
                v.Row(
                    # cols='4',  # Adjust the column width as needed
                    children=[
                        v.Card(
                            outlined=False,
                            elevation=0,
                            style_="height: 100%",
                            children=[
                                v.CardText(
                                    children=[
                                        v.CardTitle(children="Indicator"),
                                        self.value_watched_radio,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
                h_divider,
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
                                        v.CardTitle(children="Data filters"),
                                        self.reset_all_button,
                                        v.Btn(
                                            children=["IATA code?"],
                                            _metadata={"mount_id": "link_button"},
                                            href="https://www.iata.org/en/publications/directories/code-search/",
                                            target="_blank",
                                            color="light-blue-darken-4",
                                            class_="ma-2",
                                        ),
                                        v.Btn(
                                            children=["ICAO code?"],
                                            _metadata={"mount_id": "link_button"},
                                            href="https://www.icao.int/publications/doc8643/pages/search.aspx",
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
                                        v.CardTitle(children="Aircraft/Airline"),
                                        self.aircraft_autocomplete,
                                        self.airline_autocomplete,
                                        h_divider,
                                        v.CardTitle(children="Departure"),
                                        self.departure_airport_autocomplete,
                                        h_divider,
                                        v.CardTitle(children="Arrival"),
                                        self.arrival_airport_autocomplete,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        row_mega_map_flights = v.Row(
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
                                        v.Html(
                                            tag="div",
                                            class_="d-flex justify-center",
                                            children=[self.toggle_button_plot1],
                                        ),
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

        row_threeplots_flights = v.Row(
            children=[
                v.Flex(
                    lg6=True,
                    md12=True,
                    children=[
                        v.Col(
                            xs12=True,
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
                                        v.Html(
                                            tag="div",
                                            class_="d-flex justify-center",
                                            children=[self.toggle_button_plot2],
                                        ),
                                        self.output_2,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                v.Flex(
                    lg6=True,
                    md12=True,
                    children=[
                        v.Col(
                            xs12=True,
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
                                        v.Html(
                                            tag="div",
                                            class_="d-flex justify-center",
                                            children=[self.toggle_button_plot3],
                                        ),
                                        self.output_3,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        col_plots_flights = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=True,
            # cols='10',
            # class_='mb-4',  # Add margin at the bottom
            children=[row_disclaimer, row_mega_map_flights, row_threeplots_flights],
        )

        self.layout = v.Row(
            children=[col_selects_flights, v_divider, col_plots_flights]
        )


class DetailledTab_OS:
    """
    Specific Opensky variant, too much cases with airport to do a common class with compiled
    """

    def __init__(self, aeroscopedataclass):
        self.in_class_flights_df = aeroscopedataclass.flights_df.copy()

        ## define widgets
        # Airline filter
        self.airline_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airline IATA",
            items=list(aeroscopedataclass.flights_df.airline_iata.unique()),
            multiple=True,
            variant="outlined",
        )

        # Aircraft filter
        self.aircraft_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Aircraft ICAO",
            items=list(aeroscopedataclass.flights_df.acft_icao.unique()),
            multiple=True,
            variant="outlined",
        )

        # Airport filter
        self.departure_airport_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airport ICAO",
            items=list(aeroscopedataclass.flights_df.origin.unique()),
            multiple=True,
            variant="outlined",
        )

        self.arrival_airport_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airport ICAO",
            items=list(aeroscopedataclass.flights_df.dest.unique()),
            multiple=True,
            variant="outlined",
        )
        # Value watched
        self.value_watched_radio = v.RadioGroup(
            v_model="n_flights",  # Set the initial selected value here
            row=True,
            children=[
                v.Radio(label="FLIGHTS", value="n_flights"),
            ],
            class_="mb-3",
        )

        # Button to reset all filters
        self.reset_all_button = v.Btn(
            children=["Reset All"], color="light-blue-darken-4", class_="ma-2"
        )

        # Toggle button switch between the two main figures
        self.toggle_button_plot1 = v.BtnToggle(
            v_model="map",
            variant="outlined",
            children=[
                v.Btn(value="map", children=["Map"], variant="outlined"),
                v.Btn(value="tree", children=["Tree"], variant="outlined"),
            ],
        )

        # v-btn-toggle switch between the two main figures
        self.toggle_button_plot2 = v.BtnToggle(
            v_model="hist",
            children=[
                v.Btn(value="hist", children=["Histogram"]),
                v.Btn(value="ecdf", children=["Cumulative"]),
                v.Btn(value="kde_acft", children=["Aircraft type"]),
                v.Btn(value="kde_dom", children=["Flight Type"]),
            ],
        )

        self.toggle_button_plot3 = v.BtnToggle(
            v_model="acft",
            variant="text",
            children=[
                v.Btn(value="acft", children=["Aircraft Type"]),
                v.Btn(value="acft_class", children=["Aircraft Class"]),
                v.Btn(value="airline", children=["Airline"]),
                v.Btn(value="dom", children=["Flight Type"]),
            ],
        )

        self.output_1 = Output()
        self.output_2 = Output()
        self.output_3 = Output()

        self._render_initial_plots(aeroscopedataclass)
        self._make_connections(aeroscopedataclass)
        self._make_layout()

    def _make_connections(self, dataclass):
        self.reset_all_button.on_event(
            "click", partial(self._reset_all, dataclass=dataclass)
        )

        self.departure_airport_autocomplete.observe(
            partial(self._data_update_dep, dataclass=dataclass), names="v_model"
        )
        self.arrival_airport_autocomplete.observe(
            partial(self._data_update_arr, dataclass=dataclass), names="v_model"
        )
        self.airline_autocomplete.observe(
            partial(self._data_update_airline, dataclass=dataclass), names="v_model"
        )
        self.aircraft_autocomplete.observe(
            partial(self._data_update_aircraft, dataclass=dataclass), names="v_model"
        )

        self.value_watched_radio.observe(self._plot1_update, names="v_model")
        self.value_watched_radio.observe(self._plot2_update, names="v_model")
        self.value_watched_radio.observe(self._plot3_update, names="v_model")

        self.toggle_button_plot1.observe(self._plot1_update, names="v_model")
        self.toggle_button_plot2.observe(self._plot2_update, names="v_model")
        self.toggle_button_plot3.observe(self._plot3_update, names="v_model")

    def _reset_all(self, widget, event, data, dataclass):
        self.departure_airport_autocomplete.v_model = list()
        self.arrival_airport_autocomplete.v_model = list()
        self.airline_autocomplete.v_model = list()
        self.aircraft_autocomplete.v_model = list()
        self.departure_airport_autocomplete.items = (
            dataclass.flights_df.origin.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            dataclass.flights_df.dest.unique().tolist()
        )
        self.airline_autocomplete.items = (
            dataclass.flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            dataclass.flights_df.acft_icao.unique().tolist()
        )

    def _render_initial_plots(self, dataclass):
        with self.output_1:
            print("Too much data selected for flight map rendering")

        with self.output_2:
            fig_flights_2 = flight_level_plots.distance_histogram_plot_flights(
                dataclass.flights_df, "n_flights"
            )
            display(fig_flights_2)

        with self.output_3:
            fig_flights_3 = flight_level_plots.aircraft_pie_flights(
                dataclass.flights_df, "n_flights"
            )
            display(fig_flights_3)

    def _data_update_airline(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["origin"].isin(filtered_departure_airport)
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["dest"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.airline_autocomplete.v_model) == 0:
            self.airline_autocomplete.items = (
                self.in_class_flights_df.airline_iata.unique().tolist()
            )

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.origin.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.dest.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _data_update_aircraft(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["origin"].isin(filtered_departure_airport)
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["dest"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.aircraft_autocomplete.v_model) == 0:
            self.aircraft_autocomplete.items = (
                self.in_class_flights_df.acft_icao.unique().tolist()
            )

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.origin.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.dest.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _data_update_arr(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["origin"].isin(filtered_departure_airport)
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["dest"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.arrival_airport_autocomplete.v_model) == 0:
            self.arrival_airport_autocomplete.items = (
                self.in_class_flights_df.dest.unique().tolist()
            )

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.origin.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _data_update_dep(self, change, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model

        # reset local flight data with base flights_df
        self.in_class_flights_df = dataclass.flights_df.copy()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["origin"].isin(filtered_departure_airport)
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["dest"].isin(filtered_arrival_airport)
            ].reset_index()

        # active airline filter
        if filtered_airline:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["airline_iata"].isin(filtered_airline)
            ].reset_index()

        # active acft filter
        if filtered_aircraft:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["acft_icao"].isin(filtered_aircraft)
            ].reset_index()

        if len(self.departure_airport_autocomplete.v_model) == 0:
            self.departure_airport_autocomplete.items = (
                self.in_class_flights_df.origin.unique().tolist()
            )

        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.dest.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

        self._plot1_update(change)
        self._plot2_update(change)
        self._plot3_update(change)

    def _plot1_update(self, change):
        value_watched_flights = self.value_watched_radio.v_model
        active_main_graph_flights = self.toggle_button_plot1.v_model

        if len(self.in_class_flights_df) < 20000:
            with self.output_1:
                self.output_1.clear_output(wait=True)
                if active_main_graph_flights == "map":
                    # # grouping flighst on and OD basis, and concatenating airline and aircraft information

                    flights_df_od = (
                        self.in_class_flights_df.groupby(["origin", "dest"])
                        .agg(
                            {
                                "acft_icao": ", ".join,
                                "airline_iata": ", ".join,
                                "departure_lon": "first",
                                "departure_lat": "first",
                                "arrival_lon": "first",
                                "arrival_lat": "first",
                                "co2": "sum",
                                "ask": "sum",
                                "seats": "sum",
                                "n_flights": "sum",
                            }
                        )
                        .reset_index()
                    )

                    # Apply the function to the DataFrame column
                    flights_df_od["airline_iata"] = flights_df_od["airline_iata"].apply(
                        remove_duplicates
                    )
                    flights_df_od["acft_icao"] = flights_df_od["acft_icao"].apply(
                        remove_duplicates
                    )
                    fig_flights_1 = flight_level_plots.flights_map_plot_OS(
                        flights_df_od, value_watched_flights
                    )
                else:
                    fig_flights_1 = flight_level_plots.flights_treemap_plot_OS(
                        self.in_class_flights_df, value_watched_flights
                    )

                display(fig_flights_1)

        else:
            with self.output_1:
                self.output_1.clear_output(wait=True)
                print("Too much data selected for flight map rendering")

    def _plot2_update(self, change):
        value_watched_flights = self.value_watched_radio.v_model
        active_analysis_graph_flights = self.toggle_button_plot2.v_model

        with self.output_2:
            self.output_2.clear_output(wait=True)
            if active_analysis_graph_flights == "hist":
                fig_flights_2 = flight_level_plots.distance_histogram_plot_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            elif active_analysis_graph_flights == "ecdf":
                fig_flights_2 = flight_level_plots.distance_cumul_plot_flights_OS(
                    self.in_class_flights_df
                )
            elif active_analysis_graph_flights == "kde_acft":
                fig_flights_2 = flight_level_plots.distance_share_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            else:
                fig_flights_2 = flight_level_plots.distance_share_dom_int_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            display(fig_flights_2)

    def _plot3_update(self, change):
        value_watched_flights = self.value_watched_radio.v_model
        active_pie_graph_flights = self.toggle_button_plot3.v_model

        with self.output_3:
            self.output_3.clear_output(wait=True)
            if active_pie_graph_flights == "acft":
                fig_flights_3 = flight_level_plots.aircraft_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            elif active_pie_graph_flights == "acft_class":
                fig_flights_3 = flight_level_plots.aircraft_class_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            elif active_pie_graph_flights == "airline":
                fig_flights_3 = flight_level_plots.aircraft_user_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            else:
                fig_flights_3 = flight_level_plots.dom_share_pie_flights(
                    self.in_class_flights_df, value_watched_flights
                )
            display(fig_flights_3)

    def _make_layout(self):
        h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        ### PAGE ARCHITECTURE

        ## Define the rows

        row_disclaimer = v.Col(
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

        col_selects_flights = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=False,
            cols="3",
            class_="mb-4",  # Add margin at the bottom
            children=[
                v.Row(
                    # cols='4',  # Adjust the column width as needed
                    children=[
                        v.Card(
                            outlined=False,
                            elevation=0,
                            style_="height: 100%",
                            children=[
                                v.CardText(
                                    children=[
                                        v.CardTitle(children="Indicator"),
                                        self.value_watched_radio,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
                h_divider,
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
                                        v.CardTitle(children="Data filters"),
                                        self.reset_all_button,
                                        v.Btn(
                                            children=["IATA code?"],
                                            _metadata={"mount_id": "link_button"},
                                            href="https://www.iata.org/en/publications/directories/code-search/",
                                            target="_blank",
                                            color="light-blue-darken-4",
                                            class_="ma-2",
                                        ),
                                        v.Btn(
                                            children=["ICAO code?"],
                                            _metadata={"mount_id": "link_button"},
                                            href="https://www.icao.int/publications/doc8643/pages/search.aspx",
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
                                        v.CardTitle(children="Aircraft/Airline"),
                                        self.aircraft_autocomplete,
                                        self.airline_autocomplete,
                                        h_divider,
                                        v.CardTitle(children="Departure"),
                                        self.departure_airport_autocomplete,
                                        h_divider,
                                        v.CardTitle(children="Arrival"),
                                        self.arrival_airport_autocomplete,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        row_mega_map_flights = v.Row(
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
                                        v.Html(
                                            tag="div",
                                            class_="d-flex justify-center",
                                            children=[self.toggle_button_plot1],
                                        ),
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

        row_threeplots_flights = v.Row(
            children=[
                v.Flex(
                    lg6=True,
                    md12=True,
                    children=[
                        v.Col(
                            xs12=True,
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
                                        v.Html(
                                            tag="div",
                                            class_="d-flex justify-center",
                                            children=[self.toggle_button_plot2],
                                        ),
                                        self.output_2,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                v.Flex(
                    lg6=True,
                    md12=True,
                    children=[
                        v.Col(
                            xs12=True,
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
                                        v.Html(
                                            tag="div",
                                            class_="d-flex justify-center",
                                            children=[self.toggle_button_plot3],
                                        ),
                                        self.output_3,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        col_plots_flights = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=True,
            # cols='10',
            # class_='mb-4',  # Add margin at the bottom
            children=[row_disclaimer, row_mega_map_flights, row_threeplots_flights],
        )

        self.layout = v.Row(
            children=[col_selects_flights, v_divider, col_plots_flights]
        )


# Function to remove duplicates from a comma-separated string
def remove_duplicates(input_str):
    # Split the string into a list of substrings
    substrings = input_str.split(", ")
    # Remove duplicates and preserve the order
    unique_substrings = list(dict.fromkeys(substrings))
    # Join the unique substrings back into a single string
    result_str = ", ".join(unique_substrings)
    return result_str
