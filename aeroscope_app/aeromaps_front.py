# @Time : 07/12/2023 17:25
# @Author : a.salgas
# @File : aeromaps_front.py
# @Software: PyCharm
import ipyvuetify as v
import ipywidgets
import pandas as pd
from ipywidgets import Output, widgets, HTML
from IPython.display import display, clear_output
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
            v_model=[0, aeroscopedataclass.flights_df.distance_km.max() + 50],
            max=aeroscopedataclass.flights_df.distance_km.max() + 50,
            min=0,
            step=50,
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

        self.dl_button = ipywidgets.Button(
            description="Download table", button_style="info"
        )

        self.link_with_image = widgets.HTML(
            f'<a href="https://aeromaps.isae-supaero.fr/" target="_blank">'
            f'<img src="logo/aeromaps.png" alt="Logo" style="width: 120px; height: 100px;">'
            "</a>"
        )
        self.download_output = Output()
        display(self.download_output)

        self._render_initial_table(aeroscopedataclass)
        self._make_connections(aeroscopedataclass)
        self._make_layout()

    def _make_connections(self, dataclass):
        self.reset_all_button.on_event(
            "click", partial(self._reset_all, dataclass=dataclass)
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
        self.departure_continent_autocomplete.observe(
            partial(self._df_update_dep_conti, dataclass=dataclass), names="v_model"
        )
        self.arrival_airport_autocomplete.observe(
            partial(self._df_update_arr_arpt, dataclass=dataclass), names="v_model"
        )
        self.arrival_country_autocomplete.observe(
            partial(self._df_update_arr_ctry, dataclass=dataclass), names="v_model"
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

    def _reset_all(self, widget, event, data, dataclass):
        self.departure_airport_autocomplete.v_model = list()
        self.departure_country_autocomplete.v_model = list()
        self.departure_continent_autocomplete.v_model = list()
        self.arrival_airport_autocomplete.v_model = list()
        self.arrival_country_autocomplete.v_model = list()
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
        self.departure_continent_autocomplete.items = (
            dataclass.flights_df.departure_continent_name.unique().tolist()
        )
        self.arrival_airport_autocomplete.items = (
            dataclass.flights_df.iata_arrival.unique().tolist()
        )
        self.arrival_country_autocomplete.items = (
            dataclass.flights_df.arrival_country_name.unique().tolist()
        )
        self.arrival_continent_autocomplete.items = (
            dataclass.flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = (
            dataclass.flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            dataclass.flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            dataclass.flights_df.acft_icao.unique().tolist()
        )
        self.range_slider.v_model = [0, dataclass.flights_df.distance_km.max() + 50]

    def _render_initial_table(self, dataclass):
        headers = [
            {"text": "Metric", "value": "name"},
            {"text": "Value (Total)", "value": "val"},
            {"text": "Value (SR)", "value": "sr"},
            {"text": "Value (MR)", "value": "mr"},
            {"text": "Value (LR)", "value": "lr"},
        ]

        total_sums = self.in_class_flights_df[["co2", "ask", "seats"]].sum()
        sr_sums = self.in_class_flights_df[
            self.in_class_flights_df.distance_km <= 1500
        ][["co2", "ask", "seats"]].sum()
        mr_sums = self.in_class_flights_df[
            (self.in_class_flights_df.distance_km > 1500)
            & (self.in_class_flights_df.distance_km <= 4000)
        ][["co2", "ask", "seats"]].sum()
        lr_sums = self.in_class_flights_df[self.in_class_flights_df.distance_km > 4000][
            ["co2", "ask", "seats"]
        ].sum()

        items = [
            {
                "name": "ASK",
                "val": total_sums["ask"],
                "sr": sr_sums["ask"],
                "mr": mr_sums["ask"],
                "lr": lr_sums["ask"],
            },
            {
                "name": "CO2 (kg)",
                "val": total_sums["co2"],
                "sr": sr_sums["co2"],
                "mr": mr_sums["co2"],
                "lr": lr_sums["co2"],
            },
            {
                "name": "Seats",
                "val": total_sums["seats"],
                "sr": sr_sums["seats"],
                "mr": mr_sums["seats"],
                "lr": lr_sums["seats"],
            },
            {
                "name": "CO2 per ask",
                "val": total_sums["co2"] / total_sums["ask"],
                "sr": sr_sums["co2"] / sr_sums["ask"],
                "mr": mr_sums["co2"] / mr_sums["ask"],
                "lr": lr_sums["co2"] / lr_sums["ask"],
            },
            {
                "name": "Share of world ASK (%)",
                "val": total_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
                "sr": sr_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
                "mr": mr_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
                "lr": lr_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
            },
            {
                "name": "Share of world Seats (%)",
                "val": total_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
                "sr": sr_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
                "mr": mr_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
                "lr": lr_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
            },
            {
                "name": "Share of world CO2 (%)",
                "val": total_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
                "sr": sr_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
                "mr": mr_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
                "lr": lr_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
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
        total_sums = self.in_class_flights_df[["co2", "ask", "seats"]].sum()
        sr_sums = self.in_class_flights_df[
            self.in_class_flights_df.distance_km <= 1500
        ][["co2", "ask", "seats"]].sum()
        mr_sums = self.in_class_flights_df[
            (self.in_class_flights_df.distance_km > 1500)
            & ((self.in_class_flights_df.distance_km <= 4000))
        ][["co2", "ask", "seats"]].sum()
        lr_sums = self.in_class_flights_df[self.in_class_flights_df.distance_km > 4000][
            ["co2", "ask", "seats"]
        ].sum()

        items = [
            {
                "name": "ASK",
                "val": total_sums["ask"],
                "sr": sr_sums["ask"],
                "mr": mr_sums["ask"],
                "lr": lr_sums["ask"],
            },
            {
                "name": "CO2 (kg)",
                "val": total_sums["co2"],
                "sr": sr_sums["co2"],
                "mr": mr_sums["co2"],
                "lr": lr_sums["co2"],
            },
            {
                "name": "Seats",
                "val": total_sums["seats"],
                "sr": sr_sums["seats"],
                "mr": mr_sums["seats"],
                "lr": lr_sums["seats"],
            },
            {
                "name": "CO2 per ask",
                "val": total_sums["co2"] / total_sums["ask"],
                "sr": sr_sums["co2"] / sr_sums["ask"],
                "mr": mr_sums["co2"] / mr_sums["ask"],
                "lr": lr_sums["co2"] / lr_sums["ask"],
            },
            {
                "name": "Share of world ASK (%)",
                "val": total_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
                "sr": sr_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
                "mr": mr_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
                "lr": lr_sums["ask"] / dataclass.flights_df.ask.sum() * 100,
            },
            {
                "name": "Share of world Seats (%)",
                "val": total_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
                "sr": sr_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
                "mr": mr_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
                "lr": lr_sums["seats"] / dataclass.flights_df.seats.sum() * 100,
            },
            {
                "name": "Share of world CO2 (%)",
                "val": total_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
                "sr": sr_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
                "mr": mr_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
                "lr": lr_sums["co2"] / dataclass.flights_df.co2.sum() * 100,
            },
        ]
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
                self.in_class_flights_df["iata_departure"].isin(
                    filtered_departure_airport
                )
            ].reset_index()

        if filtered_departure_country:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["departure_country_name"].isin(
                    filtered_departure_country
                )
            ].reset_index()

        if filtered_departure_conti:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["departure_continent_name"].isin(
                    filtered_departure_conti
                )
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
                self.in_class_flights_df["arrival_country_name"].isin(
                    filtered_arrival_country
                )
            ].reset_index()

        if filtered_arrival_conti:
            if "level_0" in self.in_class_flights_df.columns:
                self.in_class_flights_df.drop("level_0", axis=1, inplace=True)
            self.in_class_flights_df = self.in_class_flights_df[
                self.in_class_flights_df["arrival_continent_name"].isin(
                    filtered_arrival_conti
                )
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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

    def _df_update_dep_ctry(self, change, dataclass):
        self._filter_common_code(dataclass=dataclass)

        self.departure_airport_autocomplete.items = (
            self.in_class_flights_df.iata_departure.unique().tolist()
        )
        if len(self.departure_country_autocomplete.v_model) == 0:
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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.arrival_continent_autocomplete.items = (
            self.in_class_flights_df.arrival_continent_name.unique().tolist()
        )
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        if len(self.airline_autocomplete.v_model) == 0:
            self.airline_autocomplete.items = (
                self.in_class_flights_df.airline_iata.unique().tolist()
            )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        if len(self.aircraft_autocomplete.v_model) == 0:
            self.aircraft_autocomplete.items = (
                self.in_class_flights_df.acft_icao.unique().tolist()
            )

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
            self.domestic_autocomplete.items = (
                self.in_class_flights_df.domestic.unique().tolist()
            )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
        self.domestic_autocomplete.items = (
            self.in_class_flights_df.domestic.unique().tolist()
        )
        self.airline_autocomplete.items = (
            self.in_class_flights_df.airline_iata.unique().tolist()
        )
        self.aircraft_autocomplete.items = (
            self.in_class_flights_df.acft_icao.unique().tolist()
        )

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
            print("trig1")
            display(HTML(f"<script>{js_code}</script>"))

    def _download_dataframe(self, e=None):
        self._trigger_download_dataframe(
            self.df_metrics, "dataframe_aeromaps.csv", kind="text/csv"
        )

    def _make_layout(self):
        h_divider = v.Divider(vertical=False)
        v_divider = v.Divider(vertical=True)
        row_disclaimer_aeromaps = v.Col(
            # cols='12',  # Adjust the column width as needed
            children=[
                v.CardText(
                    children=[
                        "Caution: Accuracy is limited (particularly in some regions) in this mode. Data must therefore be used with the necessary precautions.",
                        "Comparison between aircraft types performances NOT VALID",
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
                                                    _metadata={
                                                        "mount_id": "link_button"
                                                    },
                                                    href="https://www.iata.org/en/publications/directories/code-search/",
                                                    target="_blank",
                                                    color="light-blue-darken-4",
                                                    class_="ma-2",
                                                ),
                                                v.Btn(
                                                    children=["ICAO code?"],
                                                    _metadata={
                                                        "mount_id": "link_button"
                                                    },
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
