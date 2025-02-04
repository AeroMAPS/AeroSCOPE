# @Time : 07/12/2023 17:25
# @Author : a.salgas
# @File : aeromaps_front.py
# @Software: PyCharm
import ipyvuetify as v
import ipywidgets
import pandas as pd
from ipywidgets import Output, widgets
from IPython.display import display, clear_output, HTML
from functools import partial

from base64 import b64encode


############## AEROMAPS EXPORTER #################


class AeroMAPSTab:
    def __init__(self, aeroscopedataclass):
        self.in_class_flights_df = aeroscopedataclass.flights_df.copy()

        ############# Airline filter #############

        self.airline_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Airline IATA",
            items=list(aeroscopedataclass.flights_df.airline_iata.unique()),
            multiple=True,
            variant="outlined",
        )

        ############# Aircraft filter #############

        self.aircraft_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Aircraft ICAO",
            items=list(aeroscopedataclass.flights_df.acft_icao.unique()),
            multiple=True,
            variant="outlined",
        )

        ############# Airport filter #############

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

        ############# Country filter #############

        self.departure_country_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Country",
            items=list(aeroscopedataclass.flights_df.departure_country_name.unique()),
            multiple=True,
            variant="outlined",
        )

        self.arrival_country_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Country",
            items=list(aeroscopedataclass.flights_df.arrival_country_name.unique()),
            multiple=True,
            variant="outlined",
        )

        ############# International Organisation Filter #############

        self.departure_organisation_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="International Organisation",
            items=[
                "European Union",
                "European Union + Outermost Regions",
                "OECD",
                "G7",
                "G20",
                "Eurocontrol Members",
                "BRICS",
                "France + Overseas",
            ],
            multiple=True,
            variant="outlined",
        )

        self.arrival_organisation_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="International Organisation",
            items=[
                "European Union",
                "European Union + Outermost Regions",
                "OECD",
                "G7",
                "G20",
                "Eurocontrol Members",
                "BRICS",
                "France + Overseas",
            ],
            multiple=True,
            variant="outlined",
        )

        ############# Continent filter #############

        self.departure_continent_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Continent",
            items=list(aeroscopedataclass.flights_df.departure_continent_name.unique()),
            multiple=True,
            variant="outlined",
        )

        self.arrival_continent_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Continent",
            items=list(aeroscopedataclass.flights_df.arrival_continent_name.unique()),
            multiple=True,
            variant="outlined",
        )

        ############# Domestic-International filter #############

        self.domestic_autocomplete = v.Autocomplete(
            v_model=[],
            clearable=True,
            chips=True,
            label="Flight type (Domestic: 1/International: 0)",
            items=list(aeroscopedataclass.flights_df.domestic.unique()),
            multiple=True,
            variant="outlined",
        )

        ############# Distance filter #############

        self.range_slider = v.RangeSlider(
            v_model=[0, aeroscopedataclass.flights_df.distance_km.max() + 10],
            max=aeroscopedataclass.flights_df.distance_km.max() + 10,
            min=0,
            step=10,
            label="Distance (km)",
            color="#050A30",
            track_color="grey",
            thumb_color="#26A69A",
            hide_details=False,
            thumb_label="always",
            class_="ma-8 align-center",
        )
        self.reset_all_button = v.Btn(
            children=["Reset All"], color="light-blue-darken-4", class_="ma-2"
        )

        self.link_with_image = widgets.HTML(
            '<a href="https://aeromaps.isae-supaero.fr/" target="_blank">'
            '<img src="logo/aeromaps.png" alt="Logo" style="width: 120px; height: 100px;">'
            "</a>"
        )

        self.dl_button = ipywidgets.Button(description="Download table", button_style="info")

        self._render_initial_table(aeroscopedataclass)
        self._make_connections(aeroscopedataclass)
        self._make_layout()
        self.download_output = Output()
        display(self.download_output)

    def _make_connections(self, dataclass):
        self.reset_all_button.on_event("click", partial(self._reset_all, dataclass=dataclass))

        self.departure_organisation_autocomplete.observe(
            self._select_regional_departure, names="v_model"
        )

        self.arrival_organisation_autocomplete.observe(
            self._select_regional_arrival, names="v_model"
        )

        self.range_slider.observe(
            partial(self._df_update_distance, dataclass=dataclass), names="v_model"
        )
        self.departure_airport_autocomplete.observe(
            partial(self._df_update_dep_arpt, dataclass=dataclass), names="v_model"
        )
        self.departure_country_autocomplete.observe(
            partial(self._df_update_dep_ctry, dataclass=dataclass), names="v_model"
        )

        self.departure_organisation_autocomplete.observe(
            partial(self._df_update_orga, dataclass=dataclass), names="v_model"
        )

        self.departure_continent_autocomplete.observe(
            partial(self._df_update_dep_conti, dataclass=dataclass), names="v_model"
        )
        self.arrival_airport_autocomplete.observe(
            partial(self._df_update_arr_arpt, dataclass=dataclass), names="v_model"
        )
        self.arrival_country_autocomplete.observe(
            partial(self._df_update_arr_ctry, dataclass=dataclass), names="v_model"
        )

        self.arrival_organisation_autocomplete.observe(
            partial(self._df_update_orga, dataclass=dataclass), names="v_model"
        )

        self.arrival_continent_autocomplete.observe(
            partial(self._df_update_arr_conti, dataclass=dataclass), names="v_model"
        )
        self.airline_autocomplete.observe(
            partial(self._df_update_airline, dataclass=dataclass), names="v_model"
        )
        self.aircraft_autocomplete.observe(
            partial(self._df_update_aircraft, dataclass=dataclass), names="v_model"
        )
        self.domestic_autocomplete.observe(
            partial(self._df_update_type, dataclass=dataclass), names="v_model"
        )
        self.dl_button.on_click(self._download_dataframe)

    def _select_regional_departure(self, change):
        selected_organisations = self.departure_organisation_autocomplete.v_model

        regional_list = []
        if "European Union" in selected_organisations:
            regional_list.extend(
                [
                    "Austria, Republic of",
                    "Belgium, Kingdom of",
                    "Bulgaria, Republic of",
                    "Croatia, Republic of",
                    "Cyprus, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Hungary, Republic of",
                    "Ireland",
                    "Italy, Italian Republic",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Malta, Republic of",
                    "Netherlands, Kingdom of the",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Romania",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                ]
            )
        if "European Union + Outermost Regions" in selected_organisations:
            regional_list.extend(
                [
                    "Austria, Republic of",
                    "Belgium, Kingdom of",
                    "Bulgaria, Republic of",
                    "Mayotte",
                    "Croatia, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "French Guiana",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Guadeloupe",
                    "Hungary, Republic of",
                    "Ireland",
                    "Italy, Italian Republic",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Malta, Republic of",
                    "Martinique",
                    "Netherlands, Kingdom of the",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Reunion",
                    "Romania",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                    "Saint Martin",
                ]
            )
        if "France + Overseas" in selected_organisations:
            regional_list.extend(
                [
                    "Mayotte",
                    "French Polynesia",
                    "Guadeloupe",
                    "French Guiana",
                    "Martinique",
                    "New Caledonia",
                    "Reunion",
                    "Saint Barthelemy",
                    "Saint Pierre and Miquelon",
                    "Wallis and Futuna",
                    "Saint Martin",
                    "France, French Republic",
                ]
            )
        if "G7" in selected_organisations:
            regional_list.extend(
                [
                    "Canada",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "Italy, Italian Republic",
                    "Japan",
                    "United Kingdom of Great Britain & Northern Ireland",
                    "United States of America",
                ]
            )
        if "G20" in selected_organisations:
            regional_list.extend(
                [
                    "Argentina, Argentine Republic",
                    "Australia, Commonwealth of",
                    "Brazil, Federative Republic of",
                    "Canada",
                    "China, People's Republic of",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "India, Republic of",
                    "Indonesia, Republic of",
                    "Italy, Italian Republic",
                    "Japan",
                    "Mexico, United Mexican States",
                    "Russian Federation",
                    "Saudi Arabia, Kingdom of",
                    "South Africa, Republic of",
                    "Republic of Korea",
                    "Turkey, Republic of",
                    "United Kingdom of Great Britain & Northern Ireland",
                    "United States of America",
                ]
            )
        if "OECD" in selected_organisations:
            regional_list.extend(
                [
                    "Australia, Commonwealth of",
                    "Austria, Republic of",
                    "Belgium, Kingdom of",
                    "Canada",
                    "Chile, Republic of",
                    "Colombia, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Hungary, Republic of",
                    "Iceland, Republic of",
                    "Ireland",
                    "Israel, State of",
                    "Italy, Italian Republic",
                    "Japan",
                    "Korea, Republic of",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Mexico, United Mexican States",
                    "Netherlands, Kingdom of the",
                    "New Zealand",
                    "Norway, Kingdom of",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                    "Switzerland, Swiss Confederation",
                    "Turkey, Republic of",
                    "United Kingdom of Great Britain & Northern Ireland",
                    "United States of America",
                ]
            )
        if "Eurocontrol Members" in selected_organisations:
            regional_list.extend(
                [
                    "Albania, Republic of",
                    "Armenia, Republic of",
                    "Austria, Republic of",
                    "Azerbaijan, Republic of",
                    "Belgium, Kingdom of",
                    "Bosnia and Herzegovina",
                    "Bulgaria, Republic of",
                    "Croatia, Republic of",
                    "Cyprus, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "Georgia",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Hungary, Republic of",
                    "Ireland",
                    "Italy, Italian Republic",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Malta, Republic of",
                    "Moldova, Republic of",
                    "Monaco, Principality of",
                    "Montenegro, Republic of",
                    "Netherlands, Kingdom of the",
                    "North Macedonia, Republic of",
                    "Norway, Kingdom of",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Romania",
                    "Serbia, Republic of",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                    "Switzerland, Swiss Confederation",
                    "Turkey, Republic of",
                    "Ukraine",
                    "United Kingdom of Great Britain & Northern Ireland",
                ]
            )
        if "BRICS" in selected_organisations:
            regional_list.extend(
                [
                    "Brazil, Federative Republic of",
                    "Russian Federation",
                    "India, Republic of",
                    "China, People's Republic of",
                    "South Africa, Republic of",
                ]
            )

        self.departure_country_autocomplete.v_model = list(set(regional_list))
        self.departure_country_autocomplete.items = list(set(regional_list))

    def _select_regional_arrival(self, change):
        selected_organisations = self.arrival_organisation_autocomplete.v_model

        regional_list = []
        if "European Union" in selected_organisations:
            regional_list.extend(
                [
                    "Austria, Republic of",
                    "Belgium, Kingdom of",
                    "Bulgaria, Republic of",
                    "Croatia, Republic of",
                    "Cyprus, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Hungary, Republic of",
                    "Ireland",
                    "Italy, Italian Republic",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Malta, Republic of",
                    "Netherlands, Kingdom of the",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Romania",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                ]
            )
        if "European Union + Outermost Regions" in selected_organisations:
            regional_list.extend(
                [
                    "Austria, Republic of",
                    "Belgium, Kingdom of",
                    "Bulgaria, Republic of",
                    "Mayotte",
                    "Croatia, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "French Guiana",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Guadeloupe",
                    "Hungary, Republic of",
                    "Ireland",
                    "Italy, Italian Republic",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Malta, Republic of",
                    "Martinique",
                    "Netherlands, Kingdom of the",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Reunion",
                    "Romania",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                    "Saint Martin",
                ]
            )
        if "France + Overseas" in selected_organisations:
            regional_list.extend(
                [
                    "Mayotte",
                    "French Polynesia",
                    "Guadeloupe",
                    "French Guiana",
                    "Martinique",
                    "New Caledonia",
                    "Reunion",
                    "Saint Barthelemy",
                    "Saint Pierre and Miquelon",
                    "Wallis and Futuna",
                    "Saint Martin",
                    "France, French Republic",
                ]
            )
        if "G7" in selected_organisations:
            regional_list.extend(
                [
                    "Canada",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "Italy, Italian Republic",
                    "Japan",
                    "United Kingdom of Great Britain & Northern Ireland",
                    "United States of America",
                ]
            )
        if "G20" in selected_organisations:
            regional_list.extend(
                [
                    "Argentina, Argentine Republic",
                    "Australia, Commonwealth of",
                    "Brazil, Federative Republic of",
                    "Canada",
                    "China, People's Republic of",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "India, Republic of",
                    "Indonesia, Republic of",
                    "Italy, Italian Republic",
                    "Japan",
                    "Mexico, United Mexican States",
                    "Russian Federation",
                    "Saudi Arabia, Kingdom of",
                    "South Africa, Republic of",
                    "Republic of Korea",
                    "Turkey, Republic of",
                    "United Kingdom of Great Britain & Northern Ireland",
                    "United States of America",
                ]
            )
        if "OECD" in selected_organisations:
            regional_list.extend(
                [
                    "Australia, Commonwealth of",
                    "Austria, Republic of",
                    "Belgium, Kingdom of",
                    "Canada",
                    "Chile, Republic of",
                    "Colombia, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Hungary, Republic of",
                    "Iceland, Republic of",
                    "Ireland",
                    "Israel, State of",
                    "Italy, Italian Republic",
                    "Japan",
                    "Korea, Republic of",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Mexico, United Mexican States",
                    "Netherlands, Kingdom of the",
                    "New Zealand",
                    "Norway, Kingdom of",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                    "Switzerland, Swiss Confederation",
                    "Turkey, Republic of",
                    "United Kingdom of Great Britain & Northern Ireland",
                    "United States of America",
                ]
            )
        if "Eurocontrol Members" in selected_organisations:
            regional_list.extend(
                [
                    "Albania, Republic of",
                    "Armenia, Republic of",
                    "Austria, Republic of",
                    "Azerbaijan, Republic of",
                    "Belgium, Kingdom of",
                    "Bosnia and Herzegovina",
                    "Bulgaria, Republic of",
                    "Croatia, Republic of",
                    "Cyprus, Republic of",
                    "Czech Republic",
                    "Denmark, Kingdom of",
                    "Estonia, Republic of",
                    "Finland, Republic of",
                    "France, French Republic",
                    "Georgia",
                    "Germany, Federal Republic of",
                    "Greece, Hellenic Republic",
                    "Hungary, Republic of",
                    "Ireland",
                    "Italy, Italian Republic",
                    "Latvia, Republic of",
                    "Lithuania, Republic of",
                    "Luxembourg, Grand Duchy of",
                    "Malta, Republic of",
                    "Moldova, Republic of",
                    "Monaco, Principality of",
                    "Montenegro, Republic of",
                    "Netherlands, Kingdom of the",
                    "North Macedonia, Republic of",
                    "Norway, Kingdom of",
                    "Poland, Republic of",
                    "Portugal, Portuguese Republic",
                    "Romania",
                    "Serbia, Republic of",
                    "Slovakia (Slovak Republic)",
                    "Slovenia, Republic of",
                    "Spain, Kingdom of",
                    "Sweden, Kingdom of",
                    "Switzerland, Swiss Confederation",
                    "Turkey, Republic of",
                    "Ukraine",
                    "United Kingdom of Great Britain & Northern Ireland",
                ]
            )
        if "BRICS" in selected_organisations:
            regional_list.extend(
                [
                    "Brazil, Federative Republic of",
                    "Russian Federation",
                    "India, Republic of",
                    "China, People's Republic of",
                    "South Africa, Republic of",
                ]
            )

        self.arrival_country_autocomplete.v_model = list(set(regional_list))
        self.arrival_country_autocomplete.items = list(set(regional_list))

    def _reset_all(self, widget, event, data, dataclass):
        self.departure_airport_autocomplete.v_model = list()
        self.departure_country_autocomplete.v_model = list()
        self.departure_organisation_autocomplete.v_model = list()
        self.departure_continent_autocomplete.v_model = list()
        self.arrival_airport_autocomplete.v_model = list()
        self.arrival_country_autocomplete.v_model = list()
        self.arrival_organisation_autocomplete.v_model = list()
        self.arrival_continent_autocomplete.v_model = list()
        self.domestic_autocomplete.v_model = list()
        self.airline_autocomplete.v_model = list()
        self.aircraft_autocomplete.v_model = list()
        self.departure_airport_autocomplete.items = (
            dataclass.flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            dataclass.flights_df.departure_country_name.unique().tolist()
        )

        self.departure_organisation_autocomplete.items = [
            "European Union",
            "European Union + Outermost Regions",
            "OECD",
            "G7",
            "G20",
            "Eurocontrol Members",
            "BRICS",
            "France + Overseas",
        ]

        self.departure_continent_autocomplete.items = (
            dataclass.flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            dataclass.flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            dataclass.flights_df.arrival_country_name.unique().tolist()
        )

        self.arrival_organisation_autocomplete.items = [
            "European Union",
            "European Union + Outermost Regions",
            "OECD",
            "G7",
            "G20",
            "Eurocontrol Members",
            "BRICS",
            "France + Overseas",
        ]

        self.arrival_continent_autocomplete.items = (
            dataclass.flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = dataclass.flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = dataclass.flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = dataclass.flights_df.acft_icao.unique().tolist()
        self.range_slider.v_model = [0, dataclass.flights_df.distance_km.max() + 50]

    def _render_initial_table(self, dataclass):
        headers = [
            {"text": "Metric", "value": "name"},
            {"text": "Value (Total)", "value": "val"},
            {"text": "Value (SR)", "value": "sr"},
            {"text": "Value (MR)", "value": "mr"},
            {"text": "Value (LR)", "value": "lr"},
        ]

        total_sums = self.in_class_flights_df[["CO2 (kg)", "ASK", "Seats"]].sum()
        sr_sums = self.in_class_flights_df[self.in_class_flights_df.distance_km <= 1500][
            ["CO2 (kg)", "ASK", "Seats"]
        ].sum()
        mr_sums = self.in_class_flights_df[
            (self.in_class_flights_df.distance_km > 1500)
            & (self.in_class_flights_df.distance_km <= 4000)
        ][["CO2 (kg)", "ASK", "Seats"]].sum()
        lr_sums = self.in_class_flights_df[self.in_class_flights_df.distance_km > 4000][
            ["CO2 (kg)", "ASK", "Seats"]
        ].sum()

        items = [
            {
                "name": "ASK",
                "val": total_sums["ASK"],
                "sr": sr_sums["ASK"],
                "mr": mr_sums["ASK"],
                "lr": lr_sums["ASK"],
            },
            {
                "name": "CO2 (kg)",
                "val": total_sums["CO2 (kg)"],
                "sr": sr_sums["CO2 (kg)"],
                "mr": mr_sums["CO2 (kg)"],
                "lr": lr_sums["CO2 (kg)"],
            },
            {
                "name": "Seats",
                "val": total_sums["Seats"],
                "sr": sr_sums["Seats"],
                "mr": mr_sums["Seats"],
                "lr": lr_sums["Seats"],
            },
            {
                "name": "CO2 (kg) per ASK",
                "val": total_sums["CO2 (kg)"] / total_sums["ASK"],
                "sr": sr_sums["CO2 (kg)"] / sr_sums["ASK"],
                "mr": mr_sums["CO2 (kg)"] / mr_sums["ASK"],
                "lr": lr_sums["CO2 (kg)"] / lr_sums["ASK"],
            },
            {
                "name": "Energy (MJ) per ASK",
                "val": total_sums["CO2 (kg)"] / total_sums["ASK"] / 3.16 * 44,
                "sr": sr_sums["CO2 (kg)"] / sr_sums["ASK"] / 3.16 * 44,
                "mr": mr_sums["CO2 (kg)"] / mr_sums["ASK"] / 3.16 * 44,
                "lr": lr_sums["CO2 (kg)"] / lr_sums["ASK"] / 3.16 * 44,
            },
            {
                "name": "Share of world ASK (%)",
                "val": total_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
                "sr": sr_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
                "mr": mr_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
                "lr": lr_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
            },
            {
                "name": "Share of world Seats (%)",
                "val": total_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
                "sr": sr_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
                "mr": mr_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
                "lr": lr_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
            },
            {
                "name": "Share of world CO2 (%)",
                "val": total_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
                "sr": sr_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
                "mr": mr_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
                "lr": lr_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
            },
        ]

        self.df_metrics = pd.DataFrame(items)
        self.df_metrics.columns = [header["value"] for header in headers]

        self.output_1 = v.DataTable(
            v_model=[],
            show_select=False,
            headers=headers,
            items=items,
        )

    def _table_update(self, dataclass):
        headers = [
            {"text": "Metric", "value": "name"},
            {"text": "Value (Total)", "value": "val"},
            {"text": "Value (SR)", "value": "sr"},
            {"text": "Value (MR)", "value": "mr"},
            {"text": "Value (LR)", "value": "lr"},
        ]

        total_sums = self.in_class_flights_df[["CO2 (kg)", "ASK", "Seats"]].sum()
        sr_sums = self.in_class_flights_df[self.in_class_flights_df.distance_km <= 1500][
            ["CO2 (kg)", "ASK", "Seats"]
        ].sum()
        mr_sums = self.in_class_flights_df[
            (self.in_class_flights_df.distance_km > 1500)
            & (self.in_class_flights_df.distance_km <= 4000)
        ][["CO2 (kg)", "ASK", "Seats"]].sum()
        lr_sums = self.in_class_flights_df[self.in_class_flights_df.distance_km > 4000][
            ["CO2 (kg)", "ASK", "Seats"]
        ].sum()

        items = [
            {
                "name": "ASK",
                "val": total_sums["ASK"],
                "sr": sr_sums["ASK"],
                "mr": mr_sums["ASK"],
                "lr": lr_sums["ASK"],
            },
            {
                "name": "CO2 (kg)",
                "val": total_sums["CO2 (kg)"],
                "sr": sr_sums["CO2 (kg)"],
                "mr": mr_sums["CO2 (kg)"],
                "lr": lr_sums["CO2 (kg)"],
            },
            {
                "name": "Seats",
                "val": total_sums["Seats"],
                "sr": sr_sums["Seats"],
                "mr": mr_sums["Seats"],
                "lr": lr_sums["Seats"],
            },
            {
                "name": "CO2 (kg) per ASK",
                "val": total_sums["CO2 (kg)"] / total_sums["ASK"],
                "sr": sr_sums["CO2 (kg)"] / sr_sums["ASK"],
                "mr": mr_sums["CO2 (kg)"] / mr_sums["ASK"],
                "lr": lr_sums["CO2 (kg)"] / lr_sums["ASK"],
            },
            {
                "name": "Energy (MJ) per ASK",
                "val": total_sums["CO2 (kg)"] / total_sums["ASK"] / 3.16 * 44,
                "sr": sr_sums["CO2 (kg)"] / sr_sums["ASK"] / 3.16 * 44,
                "mr": mr_sums["CO2 (kg)"] / mr_sums["ASK"] / 3.16 * 44,
                "lr": lr_sums["CO2 (kg)"] / lr_sums["ASK"] / 3.16 * 44,
            },
            {
                "name": "Share of world ASK (%)",
                "val": total_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
                "sr": sr_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
                "mr": mr_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
                "lr": lr_sums["ASK"] / dataclass.flights_df.ASK.sum() * 100,
            },
            {
                "name": "Share of world Seats (%)",
                "val": total_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
                "sr": sr_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
                "mr": mr_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
                "lr": lr_sums["Seats"] / dataclass.flights_df.Seats.sum() * 100,
            },
            {
                "name": "Share of world CO2 (%)",
                "val": total_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
                "sr": sr_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
                "mr": mr_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
                "lr": lr_sums["CO2 (kg)"] / dataclass.flights_df["CO2 (kg)"].sum() * 100,
            },
        ]

        self.df_metrics = pd.DataFrame(items)
        self.df_metrics.columns = [header["value"] for header in headers]

        self.output_1.items = items

    def _filter_common_code(self, dataclass):
        filtered_departure_airport = self.departure_airport_autocomplete.v_model
        filtered_departure_country = self.departure_country_autocomplete.v_model
        filtered_departure_conti = self.departure_continent_autocomplete.v_model

        filtered_arrival_airport = self.arrival_airport_autocomplete.v_model
        filtered_arrival_country = self.arrival_country_autocomplete.v_model
        filtered_arrival_conti = self.arrival_continent_autocomplete.v_model

        filtered_airline = self.airline_autocomplete.v_model
        filtered_aircraft = self.aircraft_autocomplete.v_model
        filtered_type = self.domestic_autocomplete.v_model

        min_dist = self.range_slider.v_model[0]
        max_dist = self.range_slider.v_model[1]

        self.in_class_flights_df = dataclass.flights_df

        # distance filter
        # drop index before reset_index()
        if "level_0" in self.in_class_flights_df.columns:
            self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
        self.in_class_flights_df = self.in_class_flights_df[
            (self.in_class_flights_df["distance_km"] >= min_dist)
            & (self.in_class_flights_df["distance_km"] <= max_dist)
        ].reset_index()

        # active departure filter
        if filtered_departure_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_departure"].isin(filtered_departure_airport)
            ].reset_index()

        if filtered_departure_country:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["departure_country_name"].isin(filtered_departure_country)
            ].reset_index()

        if filtered_departure_conti:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["departure_continent_name"].isin(filtered_departure_conti)
            ].reset_index()

        # active arrival filter
        if filtered_arrival_airport:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["iata_arrival"].isin(filtered_arrival_airport)
            ].reset_index()

        if filtered_arrival_country:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["arrival_country_name"].isin(filtered_arrival_country)
            ].reset_index()

        if filtered_arrival_conti:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["arrival_continent_name"].isin(filtered_arrival_conti)
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

        # active type filter
        if filtered_type:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["domestic"].isin(filtered_type)
            ].reset_index()

        self._table_update(dataclass)

    def _df_update_dep_arpt(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        if len(self.departure_airport_autocomplete.v_model) == 0:
            self.departure_airport_autocomplete.items = (
                self.in_class_flights_df.iata_departure.unique().tolist()
            )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_dep_ctry(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        if len(self.departure_country_autocomplete.v_model) == 0:
            self.departure_country_autocomplete.items = (
                self.in_class_flights_df.departure_country_name.unique().tolist()
            )
            self.departure_organisation_autocomplete.v_model = list()

        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_orga(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )

        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )

        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_dep_conti(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        if len(self.departure_continent_autocomplete.v_model) == 0:
            self.departure_continent_autocomplete.items = (
                self.in_class_flights_df.departure_continent_name.unique().tolist()
            )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_arr_arpt(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        if len(self.arrival_airport_autocomplete.v_model) == 0:
            self.arrival_airport_autocomplete.items = (
                self.in_class_flights_df.iata_arrival.unique().tolist()
            )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_arr_ctry(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        if len(self.arrival_country_autocomplete.v_model) == 0:
            self.arrival_country_autocomplete.items = (
                self.in_class_flights_df.arrival_country_name.unique().tolist()
            )
            self.arrival_organisation_autocomplete.v_model = list()

        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_arr_conti(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        if len(self.arrival_continent_autocomplete.v_model) == 0:
            self.arrival_continent_autocomplete.items = (
                self.in_class_flights_df.arrival_continent_name.unique().tolist()
            )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_airline(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        if len(self.airline_autocomplete.v_model) == 0:
            self.airline_autocomplete.items = (
                self.in_class_flights_df.airline_iata.unique().tolist()
            )
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_aircraft(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        if len(self.aircraft_autocomplete.v_model) == 0:
            self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_type(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        if len(self.domestic_autocomplete.v_model) == 0:
            self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _df_update_distance(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        self.departure_country_autocomplete.items = (
            self.in_class_flights_df.departure_country_name.unique().tolist()
        )
        self.departure_continent_autocomplete.items = (
            self.in_class_flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            self.in_class_flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            self.in_class_flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = self.in_class_flights_df.domestic.unique().tolist()
        self.airline_autocomplete.items = self.in_class_flights_df.airline_iata.unique().tolist()
        self.aircraft_autocomplete.items = self.in_class_flights_df.acft_icao.unique().tolist()

    def _trigger_download_dataframe(self, dataframe, filename, kind="text/csv"):
        csv_content = dataframe.to_csv(index=False)
        content_b64 = b64encode(csv_content.encode()).decode()
        data_url = f"data:{kind};charset=utf-8;base64,{content_b64}"
        js_code = f"""
            var a = document.createElement('a');
            a.setAttribute('download', '{filename}');
            a.setAttribute('href', '{data_url}');
            a.click()
        """
        with self.download_output:
            clear_output()
            display(HTML(f"<script>{js_code}</script>"))

    def _download_dataframe(self, e=None):
        self._trigger_download_dataframe(self.df_metrics, "dataframe_aeromaps.csv", kind="text/csv")

    def _make_layout(self):
        # h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        row_disclaimer_aeromaps = v.Col(
            # cols='12',  # Adjust the column width as needed
            children=[
                v.CardText(
                    children=[
                        v.Html(
                            tag="div",
                            children=[
                                v.Html(
                                    tag="p",
                                    class_="text-center ma-0",
                                    children=["DISCLAIMER"],
                                ),
                                v.Html(
                                    tag="p",
                                    class_="text-center ma-0",
                                    children=[
                                        "Accuracy is limited (particularly in some regions) in this mode. Data must therefore be used with the necessary precautions. ",
                                    ],
                                ),
                                v.Html(
                                    tag="p",
                                    class_="text-center ma-0",
                                    children=[
                                        "Comparison between aircraft types performances NOT VALID. ",
                                    ],
                                ),
                                v.Html(
                                    tag="p",
                                    class_="text-center ma-0",
                                    children=["See zenodo.org/records/10143773 for more details."],
                                ),
                                v.Html(
                                    tag="p",
                                    class_="text-center ma-0",
                                    children=["All the metrics are for 2019."],
                                ),
                            ],
                        ),
                    ],
                    class_="text-center ma-0 teal--text darken-4",
                    style_="font-size: 16px;",
                ),
            ],
        )

        col_selects_aeromaps = v.Col(
            justify="center",
            align="center",  # Center the components horizontally
            children=[
                row_disclaimer_aeromaps,
                v.Card(
                    class_="ma-2",
                    outlined=True,
                    children=[
                        v.CardTitle(
                            children="Data filters",
                            class_="text-h1 ma-0 d-flex align-center justify-center",
                        ),
                        v.Row(
                            class_="ma-4",
                            align="center",
                            justify="center",
                            # cols='2',  # Adjust the column width as needed
                            children=[
                                v.Col(
                                    children=[
                                        v.CardTitle(
                                            children="Aircraft/Airline/Type",
                                            class_="text-h3 d-flex align-center justify-center",
                                        ),
                                        self.aircraft_autocomplete,
                                        self.airline_autocomplete,
                                        self.domestic_autocomplete,
                                    ]
                                ),
                                v_divider,
                                v.Col(
                                    children=[
                                        v.CardTitle(
                                            children="Departure",
                                            class_="text-h3 d-flex align-center justify-center",
                                        ),
                                        self.departure_airport_autocomplete,
                                        self.departure_country_autocomplete,
                                        self.departure_organisation_autocomplete,
                                        self.departure_continent_autocomplete,
                                    ]
                                ),
                                v_divider,
                                v.Col(
                                    children=[
                                        v.CardTitle(
                                            children="Arrival",
                                            class_="text-h3 d-flex align-center justify-center",
                                        ),
                                        self.arrival_airport_autocomplete,
                                        self.arrival_country_autocomplete,
                                        self.arrival_organisation_autocomplete,
                                        self.arrival_continent_autocomplete,
                                    ]
                                ),
                            ],
                        ),
                        self.range_slider,
                        v.Row(
                            align="center",
                            justify="center",
                            # cols='2',  # Adjust the column width as needed
                            children=[
                                v.Card(
                                    outlined=False,
                                    elevation=0,
                                    style_="height: 100%",
                                    children=[
                                        v.CardText(
                                            children=[
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
                    ],
                ),
            ],
        )

        col_aeromaps = v.Col(
            justify="center",
            align="center",
            no_gutters=False,
            cols="12",
            children=[
                v.CardTitle(
                    children="Summary table for AeroMAPS scenario calibration",
                    class_="text-h3 d-flex align-center justify-center",
                ),
                v.Row(
                    align="center",
                    justify="center",
                    class_="ma-2",
                    children=[
                        self.output_1,
                    ],
                ),
                v.Row(
                    align="center",
                    justify="center",
                    class_="ma-2",
                    children=[
                        self.dl_button,
                    ],
                ),
                v.Row(
                    align="center",
                    justify="center",
                    class_="ma-2",
                    children=[v.Html(tag="div", children=[self.link_with_image])],
                ),
            ],
        )

        self.layout = v.Row(children=[col_selects_aeromaps, col_aeromaps])
