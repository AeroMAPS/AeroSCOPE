# @Time : 07/12/2023 10:39
# @Author : a.salgas
# @File : continental_front.py
# @Software: PyCharm

import continental_level_plots
import ipyvuetify as v
from ipywidgets import Output
from IPython.display import display
from functools import partial


class ContinentalTab:
    def __init__(self, aeroscopedataclass):
        self.select = v.Select(
            v_model=["AF", "AS", "EU", "NA", "SA", "OC"],
            multiple=True,
            clearable=True,
            chips=True,
            items=[
                {"label": "Africa", "value": "AF"},
                {"label": "Asia", "value": "AS"},
                {"label": "Europe", "value": "EU"},
                {"label": "North America", "value": "NA"},
                {"label": "South America", "value": "SA"},
                {"label": "Oceania", "value": "OC"},
            ],
            item_text="label",
            item_value="value",
        )

        self.value_watched_radio = v.RadioGroup(
            v_model="CO2 (Mt)",  # Set the initial selected value here
            row=True,
            children=[
                v.Radio(label="CO\u2082", value="CO2 (Mt)"),
                v.Radio(label="ASK", value="ASK (Bn)"),
                v.Radio(label="SEATS", value="Seats (Mn)"),
            ],
            class_="mb-3",
        )
        self.output_1 = Output()
        self.output_2 = Output()
        self.output_3 = Output()
        self._render_initial_plots(aeroscopedataclass)
        self._make_connections(aeroscopedataclass)
        self._make_layout()

    def _render_initial_plots(self, dataclass):
        with self.output_1:
            fig_conti_1 = continental_level_plots.continental_map_plot(
                dataclass.conti_scatter, dataclass.continental_flows_non_dir, "CO2 (Mt)"
            )
            display(fig_conti_1)

        with self.output_2:
            fig_conti_2 = continental_level_plots.continental_treemap_plot(
                dataclass.continental_flows, "CO2 (Mt)"
            )
            display(fig_conti_2)

        with self.output_3:
            fig_conti_3 = continental_level_plots.distance_histogram_plot_continent(
                dataclass.flights_df, "CO2 (Mt)"
            )
            display(fig_conti_3)

    def _plots_update(self, change, dataclass):
        filtered_values = self.select.v_model
        value_watched_conti = self.value_watched_radio.v_model

        filtered_df_depart = dataclass.conti_scatter[
            dataclass.conti_scatter["departure_continent"].isin(filtered_values)
        ].reset_index()
        filtered_df = dataclass.continental_flows[
            dataclass.continental_flows["departure_continent"].isin(filtered_values)
        ].reset_index()
        filtered_fl_df = dataclass.flights_df[
            dataclass.flights_df["departure_continent"].isin(filtered_values)
        ].reset_index()

        # continental_flows_non_dir[['AV1', 'AV2']] = continental_flows_non_dir['group_col'].copy().apply(lambda x: pd.Series(x))
        filtered_non_dir = dataclass.continental_flows_non_dir[
            (dataclass.continental_flows_non_dir.AV1.isin(filtered_values))
            | (dataclass.continental_flows_non_dir.AV2.isin(filtered_values))
        ].reset_index()

        with self.output_1:
            self.output_1.clear_output(wait=True)
            fig_conti_1 = continental_level_plots.continental_map_plot(
                filtered_df_depart, filtered_non_dir, value_watched_conti
            )
            display(fig_conti_1)

        with self.output_2:
            self.output_2.clear_output(wait=True)
            fig_conti_2 = continental_level_plots.continental_treemap_plot(
                filtered_df, value_watched_conti
            )
            display(fig_conti_2)

        with self.output_3:
            self.output_3.clear_output(wait=True)
            fig_conti_3 = continental_level_plots.distance_histogram_plot_continent(
                filtered_fl_df, value_watched_conti
            )
            display(fig_conti_3)

    def _make_connections(self, dataclass):
        # # Connect the event handler to the controls

        self.select.observe(
            partial(self._plots_update, dataclass=dataclass), names="v_model"
        )
        self.value_watched_radio.observe(
            partial(self._plots_update, dataclass=dataclass), names="v_model"
        )

    def _make_layout(self):
        h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        col_selects = v.Col(
            justify="center",  # Center the components horizontally
            no_gutters=False,
            cols="3",
            # class_='mb-4',  # Add margin at the bottom
            children=[
                v.Row(
                    # cols='6',  # Adjust the column width as needed
                    children=[
                        v.Card(
                            outlined=False,
                            elevation=0,
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
                            children=[
                                v.CardText(
                                    children=[
                                        v.CardTitle(
                                            children="Select 'departure' continents"
                                        ),
                                        self.select,
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        row_mega_map = v.Row(
            justify="center",
            children=[
                v.Flex(
                    md12=True,
                    children=[
                        v.Col(
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

        row_twoplots = v.Row(
            justify="center",
            children=[
                v.Flex(
                    lg6=True,
                    md12=True,
                    children=[
                        v.Col(
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
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
                            children=[
                                v.Card(
                                    outlined=True,
                                    elevation=0,
                                    children=[
                                        self.output_3,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        row_disclaimer_cty = v.Col(
            children=[
                v.Card(
                    outlined=False,
                    elevation=0,
                    style_="width: 100%",
                    children=[
                        v.CardText(
                            children=[
                                "Please wait for the plots to be rendered before changing the indicator or the continents. \n Doing so could break the process. \n If it happens please relaod the page."
                            ],
                            class_="text-center teal--text darken-4",
                            style_="font-size: 16px;",
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
            children=[row_disclaimer_cty, row_mega_map, row_twoplots],
        )

        self.layout = v.Row(children=[col_selects, v_divider, col_plots])
