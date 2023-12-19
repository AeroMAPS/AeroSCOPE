### COUNTRIES FRONTEND
import country_level_plots
import ipyvuetify as v
from ipywidgets import Output
from IPython.display import display
from functools import partial


class CountriesTab:
    """
    Handles both Opensky and Compiled data types
    """

    def __init__(self, aeroscopedataclass):
        ## define widgets
        self.autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Countries",
            items=list(
                aeroscopedataclass.country_flows.departure_country_name.unique()
            ),
            multiple=True,
            variant="outlined",
        )

        self.select_world_button = v.Btn(
            children=["World View"],
            variant="outlined",
            color="light-blue-darken-4",
            class_="ma-2",
        )

        if aeroscopedataclass.type == "compilation":
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
        else:
            self.value_watched_radio = v.RadioGroup(
                v_model="n_flights",  # Set the initial selected value here
                row=True,
                children=[
                    v.Radio(label="FLIGHTS", value="n_flights"),
                ],
                class_="mb-3",
            )

        # v-btn-toggle switch between the two main figures
        self.toggle_button_plot1 = v.BtnToggle(
            v_model="map",
            children=[
                v.Btn(value="map", children=["Map"]),
                v.Btn(value="tree", children=["Tree"]),
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
        self.select_world_button.on_event("click", self._select_world)

        # TODO +++ change the filtering logic: decoupling from plot switch to avoid unnecessary operations!
        self.autocomplete.observe(
            partial(self._plot1_update, dataclass=dataclass), names="v_model"
        )
        self.autocomplete.observe(
            partial(self._plot2_update, dataclass=dataclass), names="v_model"
        )
        self.autocomplete.observe(
            partial(self._plot3_update, dataclass=dataclass), names="v_model"
        )

        self.value_watched_radio.observe(
            partial(self._plot1_update, dataclass=dataclass), names="v_model"
        )
        self.value_watched_radio.observe(
            partial(self._plot2_update, dataclass=dataclass), names="v_model"
        )
        self.value_watched_radio.observe(
            partial(self._plot3_update, dataclass=dataclass), names="v_model"
        )

        self.toggle_button_plot1.observe(
            partial(self._plot1_update, dataclass=dataclass), names="v_model"
        )
        self.toggle_button_plot2.observe(
            partial(self._plot2_update, dataclass=dataclass), names="v_model"
        )
        self.toggle_button_plot3.observe(
            partial(self._plot3_update, dataclass=dataclass), names="v_model"
        )

    def _select_world(self, widget, event, data):
        self.autocomplete.v_model = list()

    def _render_initial_plots(self, dataclass):
        if dataclass.type == "compilation":
            init_value = "co2"
        else:  # OPENSKY
            init_value = "n_flights"
        with self.output_1:
            fig_ctry_1 = country_level_plots.countries_global_plot(
                dataclass.country_fixed, init_value
            )
            display(fig_ctry_1)

        with self.output_2:
            fig_ctry_2 = country_level_plots.distance_histogram_plot_country(
                dataclass.flights_df, init_value
            )
            display(fig_ctry_2)

        with self.output_3:
            fig_ctry_3 = country_level_plots.aircraft_pie(
                dataclass.flights_df, init_value
            )
            display(fig_ctry_3)

    # TODO like flight plot split updates between data and plot
    def _plot1_update(self, change, dataclass):
        filtered_values = self.autocomplete.v_model
        value_watched_ctry = self.value_watched_radio.v_model
        active_main_graph_country = self.toggle_button_plot1.v_model

        if len(filtered_values) == 0:
            # Global plot, triggered by empty coutry filter
            with self.output_1:
                self.output_1.clear_output(wait=True)
                if active_main_graph_country == "map":
                    fig_ctry_1 = country_level_plots.countries_global_plot(
                        dataclass.country_fixed, value_watched_ctry
                    )
                else:
                    fig_ctry_1 = country_level_plots.countries_treemap_plot(
                        dataclass.country_flows, value_watched_ctry
                    )
                display(fig_ctry_1)

        else:
            filtered_country_flows = dataclass.country_flows[
                dataclass.country_flows["departure_country_name"].isin(filtered_values)
            ].reset_index()

            with self.output_1:
                self.output_1.clear_output(wait=True)
                if active_main_graph_country == "map":
                    fig_ctry_1 = country_level_plots.countries_map_plot(
                        filtered_country_flows, value_watched_ctry
                    )
                else:
                    fig_ctry_1 = country_level_plots.countries_treemap_plot(
                        filtered_country_flows, value_watched_ctry
                    )
                display(fig_ctry_1)

    def _plot2_update(self, change, dataclass):
        filtered_values = self.autocomplete.v_model
        value_watched_ctry = self.value_watched_radio.v_model
        active_analysis_graph_country = self.toggle_button_plot2.v_model

        if len(filtered_values) == 0:
            filtered_flights_df = dataclass.flights_df
        else:
            filtered_flights_df = dataclass.flights_df[
                dataclass.flights_df["departure_country_name"].isin(filtered_values)
            ].reset_index()

        with self.output_2:
            self.output_2.clear_output(wait=True)
            if active_analysis_graph_country == "hist":
                fig_ctry_2 = country_level_plots.distance_histogram_plot_country(
                    filtered_flights_df, value_watched_ctry
                )
            elif active_analysis_graph_country == "ecdf":
                if dataclass.type == "compilation":
                    fig_ctry_2 = country_level_plots.distance_cumul_plot_country(
                        filtered_flights_df
                    )
                else:  # OPENSKY
                    fig_ctry_2 = country_level_plots.distance_cumul_plot_country_OS(
                        filtered_flights_df
                    )
            elif active_analysis_graph_country == "kde_acft":
                fig_ctry_2 = country_level_plots.distance_share_country(
                    filtered_flights_df, value_watched_ctry
                )
            else:
                fig_ctry_2 = country_level_plots.distance_share_dom_int_country(
                    filtered_flights_df, value_watched_ctry
                )
            display(fig_ctry_2)

    def _plot3_update(self, change, dataclass):
        filtered_values = self.autocomplete.v_model
        value_watched_ctry = self.value_watched_radio.v_model
        active_pie_country = self.toggle_button_plot3.v_model

        if len(filtered_values) == 0:
            filtered_flights_df = dataclass.flights_df
        else:
            filtered_flights_df = dataclass.flights_df[
                dataclass.flights_df["departure_country_name"].isin(filtered_values)
            ].reset_index()

        with self.output_3:
            self.output_3.clear_output(wait=True)
            if active_pie_country == "acft":
                fig_ctry_3 = country_level_plots.aircraft_pie(
                    filtered_flights_df, value_watched_ctry
                )
            elif active_pie_country == "acft_class":
                fig_ctry_3 = country_level_plots.aircraft_class_pie(
                    filtered_flights_df, value_watched_ctry
                )
            elif active_pie_country == "airline":
                fig_ctry_3 = country_level_plots.aircraft_user_pie(
                    filtered_flights_df, value_watched_ctry
                )
            else:
                fig_ctry_3 = country_level_plots.dom_share_pie(
                    filtered_flights_df, value_watched_ctry
                )
            display(fig_ctry_3)

    def _make_layout(self):
        h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        col_selects = v.Col(
            justify="center",  # Center the components horizontally
            cols="3",
            no_gutters=False,
            # class_='mb-4',  # Add margin at the bottom
            children=[
                v.Row(
                    # cols='6',  # Adjust the column width as needed
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
                    # cols='6',  # Adjust the column width as needed
                    children=[
                        v.Card(
                            outlined=False,
                            elevation=0,
                            style_="height: 100%",
                            children=[
                                v.CardText(
                                    children=[
                                        v.CardTitle(
                                            children="Departure countries filter"
                                        ),
                                        self.autocomplete,
                                        self.select_world_button,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        row_mega_map = v.Row(
            children=[
                v.Flex(
                    md12=True,
                    children=[
                        v.Col(
                            md12=True,
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

        row_threeplots = v.Row(
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

        col_plots = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=False,
            # cols='10',
            # class_='mb-4',  # Add margin at the bottom
            children=[row_mega_map, row_threeplots],
        )

        self.layout = v.Row(children=[col_selects, v_divider, col_plots])
