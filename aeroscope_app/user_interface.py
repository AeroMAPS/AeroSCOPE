from datetime import datetime

import pandas as pd
import ipyvuetify as v
from ipywidgets import Output

from continental_front import ContinentalTab
from country_front import CountriesTab
from detailled_front import DetailledTab, DetailledTab_OS
from passenger_front import PassengerTab
from aeromaps_front import AeroMAPSTab
from IPython.display import display


# Create the layout
v.theme.dark = False

v_img = v.Img(cover=True, max_width="25%", src="logo/aeroscope.png", class_="mx-auto")

divider = v.Divider(vertical=True)


source_radio = v.RadioGroup(
    v_model="compilation",
    label="Data source:",
    class_="text-center mt-6",
    row=True,
    children=[
        v.Radio(label="Compilation", value="compilation", mandatory=True),
        v.Radio(label="OpenSky", value="opensky"),
    ],
)

title_layout = v.AppBar(
    app=True,
    color="white",
    align_center=True,
    children=[
        source_radio,
        ### SPACER thing is very cheap, better way to center title???
        v.Spacer(),
        v.ToolbarTitle(children=[v_img]),
        v.Spacer(),
        v.Spacer(),
        v.Btn(
            icon=True,
            href="https://aeromaps.isae-supaero.fr/",
            target="_blank",
            children=[
                v.Img(
                    src="./logo/aeromaps.png",
                    contain=True,
                    width="28px",
                ),
            ],
        ),
        v.Btn(
            icon=True,
            href="https://zenodo.org/records/10143773",
            target="_blank",
            children=[v.Icon(children=["mdi-database"])],
        ),
        v.Btn(
            icon=True,
            href="https://github.com/AeroMAPS/AeroSCOPE",
            target="_blank",
            children=[v.Icon(children=["mdi-github-circle"])],
        ),
    ],
)


footer_layout = v.Footer(
    class_=" text-center d-flex flex-column",
    style_="background-color: white;",
    children=[
        v.Col(
            class_="text-center mt-4",
            children=[
                f"{datetime.now().year} — ",
                v.Html(tag="strong", children=["©ISAE-SUPAERO"]),
            ],
        )
    ],
)


class Simulator(v.Card):
    def __init__(self, use_opensky_data=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if use_opensky_data:
            self.load_opensky_data()

        else:
            self.load_compiled_data()

        self.initialize_tabs(self.data)

        self.children = [
            self.tabs_layout,
        ]

    def load_compiled_data(self):
        #### Import various plot file. In case the source file is modified, please rerun preprocess.py ####

        from core import AeroscopeDataClass

        self.data = AeroscopeDataClass(
            # read continental level data
            continental_flows=pd.read_csv(
                "./plot_files/continental_flows.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            continental_flows_non_dir=pd.read_csv(
                "./plot_files/continental_flows_non_dir.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            conti_scatter=pd.read_csv(
                "./plot_files/conti_scatter.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            # read country level data
            country_flows=pd.read_csv(
                "./plot_files/country_flows.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            country_fixed=pd.read_csv(
                "./plot_files/country_fixed.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            # read flight_level_data
            flights_df=pd.read_csv(
                "./plot_files/flights_df.zip",
                compression="zip",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            type="compilation",
        )

    def load_opensky_data(self):
        from core import AeroscopeDataClass

        self.data = AeroscopeDataClass(
            # read continental level data
            continental_flows=pd.read_csv(
                "./plot_files_os/continental_flows.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            continental_flows_non_dir=pd.read_csv(
                "./plot_files_os/continental_flows_non_dir.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            conti_scatter=pd.read_csv(
                "./plot_files_os/conti_scatter.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            # read country level data
            country_flows=pd.read_csv(
                "./plot_files_os/country_flows.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            country_fixed=pd.read_csv(
                "./plot_files_os/country_fixed.csv",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
            ),
            # read flight_level_data
            flights_df=pd.read_csv(
                "./plot_files_os/flights_df.zip",
                compression="zip",
                sep=",",
                keep_default_na=False,
                na_values=["", "NaN"],
                index_col=0,
                low_memory=False,  # avoid mixed type warning. Fix the core Pb of unknown coordinates
            ),
            type="opensky",
        )

    def initialize_tabs(self, aeroscope_data):
        if aeroscope_data.type == "compilation":
            continental_tab = ContinentalTab(aeroscopedataclass=aeroscope_data)
            countries_tab = CountriesTab(aeroscopedataclass=aeroscope_data)
            detailled_tab = DetailledTab(aeroscopedataclass=aeroscope_data)
            passenger_tab = PassengerTab(aeroscopedataclass=aeroscope_data)
            aeromaps_tab = AeroMAPSTab(aeroscopedataclass=aeroscope_data)

            self.tabs_layout = v.Tabs(
                fixed_tabs=True,
                background_color="#050A30",
                children=[
                    v.Tab(
                        children=["Continental Mode"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    v.Tab(
                        children=["Country Mode"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    # Darken text color for active tab
                    v.Tab(
                        children=["Detailed Mode"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    # Darken text color for active tab
                    v.Tab(
                        children=["Passenger Mode"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    # Darken text color for active tab
                    v.Tab(
                        children=["AeroMAPS Export"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    # Darken text color for active tab
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[continental_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[countries_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[detailled_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[passenger_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[aeromaps_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                ],
            )
        elif aeroscope_data.type == "opensky":
            countries_tab = CountriesTab(aeroscopedataclass=aeroscope_data)
            detailled_tab = DetailledTab_OS(aeroscopedataclass=aeroscope_data)

            self.tabs_layout = v.Tabs(
                fixed_tabs=True,
                background_color="#050A30",
                children=[
                    v.Tab(
                        children=["Country Mode"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    # Darken text color for active tab
                    v.Tab(
                        children=["Detailed Mode"],
                        style_="color: white;",
                        active_class="teal--text text--lighten-1",
                    ),
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[countries_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                    v.TabItem(
                        children=[
                            v.Container(fluid=True, children=[detailled_tab.layout])
                        ],
                        style_="background-color: white;",
                    ),
                ],
            )


class UserInterface:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.compiled_simulator = Simulator(
            use_opensky_data=False,
            class_="mt-9 pa-0",
            # id='inspire',
            style_="background-color: white; pa-0 ma-0;",  # Set the desired background color and padding here
        )

        self.opensky_simulator = Simulator(
            use_opensky_data=True,
            class_="mt-9 pa-0",
            # id='inspire',
            style_="background-color: white; pa-0 ma-0;",  # Set the desired background color and padding here
        )

        self.output_simulator = Output()

        with self.output_simulator:
            display(self.compiled_simulator)

        self.app = v.App(
            class_="mt-0 pa-0",
            style_="background-color: white; pa-0 ma-0;",  # Set the desired background color and padding here
            children=[
                title_layout,
                self.output_simulator,
                v.Divider(vertical=False),
                footer_layout,
            ],
        )

        source_radio.observe(self._select_mode, names="v_model")

    def _select_mode(self, change=None):
        with self.output_simulator:
            source = source_radio.v_model
            self.output_simulator.clear_output()
            if source == "compilation":
                display(self.compiled_simulator)
            else:
                display(self.opensky_simulator)
