# @Time : 02/10/2023 09:17
# @Author : a.salgas
# @File : preprocess.py
# @Software: PyCharm
import pandas as pd
import random


def preprocess(filename="../03_routes_schedule/data/final_12_12.csv"):
    load_factor = 0.83
    flights_df = pd.read_csv(
        filename, keep_default_na=False, na_values=["", "NaN"], index_col=0
    ).dropna(subset=["departure_lon", "arrival_lon"])
    flights_df["acft_icao"] = flights_df["acft_icao"].fillna("Unknown Aircraft")
    flights_df["airline_iata"] = flights_df["airline_iata"].fillna("Unknown Airline")
    flights_df["acft_class"] = flights_df["acft_class"].fillna("Unknown Aircraft")
    flights_df["CO2 (Mt)"] = flights_df["co2"] / 1e9
    flights_df["ASK (Bn)"] = flights_df["ask"] / 1e9
    flights_df["Seats (Mn)"] = flights_df["seats"] / 1e6
    flights_df["CO2 Ppax"] = flights_df["co2"] / (flights_df["seats"] * load_factor)

    ### Aestethics
    continent_codes = {
        "AF": "Africa",
        "AS": "Asia",
        "EU": "Europe",
        "NA": "North America",
        "SA": "South America",
        "OC": "Oceania",
        "AN": "Antarctica",
    }

    color_discrete_map = {
        "AS": "#EE9B00",
        "AF": "#E9D8A6",
        "EU": "#005F73",
        "NA": "#9B2226",
        "OC": "#94D2BD",
        "SA": "#BB3E03",
        "(?)": "lightgrey",
    }

    flights_df["departure_continent_name"] = flights_df["departure_continent"].map(
        continent_codes
    )
    flights_df["arrival_continent_name"] = flights_df["arrival_continent"].map(
        continent_codes
    )

    country_codes = pd.read_csv(
        "../03_routes_schedule/data/country_codes.csv",
        keep_default_na=False,
        na_values=["", "NaN"],
        index_col=0,
    )

    flights_df = (
        flights_df.merge(
            country_codes[
                ["Country_Name", "Two_Letter_Country_Code", "Three_Letter_Country_Code"]
            ],
            left_on="departure_country",
            right_on="Two_Letter_Country_Code",
            how="left",
        )
        .rename(
            columns={
                "Country_Name": "departure_country_name",
                "Three_Letter_Country_Code": "departure_ISO3",
            }
        )
        .drop(columns={"Two_Letter_Country_Code"})
    )
    flights_df = (
        flights_df.merge(
            country_codes[
                ["Country_Name", "Two_Letter_Country_Code", "Three_Letter_Country_Code"]
            ],
            left_on="arrival_country",
            right_on="Two_Letter_Country_Code",
            how="left",
        )
        .rename(
            columns={
                "Country_Name": "arrival_country_name",
                "Three_Letter_Country_Code": "arrival_ISO3",
            }
        )
        .drop(columns={"Two_Letter_Country_Code"})
    )

    # adding a bilateral continent columns (e.g. AF-> EU ==> AF-EU; EU-> AF ==> AF-EU)
    flights_df_conti = flights_df.copy()
    flights_df_conti.dropna(
        subset={"departure_continent", "arrival_continent"}, inplace=True
    )
    flights_df_conti["group_col"] = flights_df_conti[
        ["departure_continent", "arrival_continent"]
    ].apply(lambda x: tuple(sorted(x)), axis=1)

    # Groupping flights keeping the directions
    continental_flows = (
        flights_df_conti.groupby(
            [
                "departure_continent",
                "departure_continent_name",
                "arrival_continent",
                "arrival_continent_name",
            ]
        )[["seats", "ask", "fuel_burn", "co2", "CO2 (Mt)", "ASK (Bn)", "Seats (Mn)"]]
        .sum()
        .reset_index()
    )

    # Groupping flights without the directions
    continental_flows_non_dir = (
        flights_df_conti.groupby(["group_col"])[
            ["seats", "ask", "fuel_burn", "co2", "CO2 (Mt)", "ASK (Bn)", "Seats (Mn)"]
        ]
        .sum()
        .reset_index()
    )

    ## Adding continent coordinates for plots

    conti_data = {
        "AF": {"lat": 11.5024338, "lon": 17.7578122},
        "AS": {"lat": 51.2086975, "lon": 89.2343748},
        "EU": {"lat": 51.0, "lon": 10.0},
        "NA": {"lat": 51.0000002, "lon": -109.0},
        "SA": {"lat": -21.0002179, "lon": -61.0006565},
        "OC": {"lat": -12.7725835, "lon": 173.7741688},
        "AN": {"lat": -79.4063075, "lon": 0.3149312},
    }

    continental_flows["dep_lon"] = continental_flows.apply(
        lambda row: conti_data[row.departure_continent]["lon"], axis=1
    )
    continental_flows["dep_lat"] = continental_flows.apply(
        lambda row: conti_data[row.departure_continent]["lat"], axis=1
    )
    continental_flows["arr_lon"] = continental_flows.apply(
        lambda row: conti_data[row.arrival_continent]["lon"] - 10, axis=1
    )
    continental_flows["arr_lat"] = continental_flows.apply(
        lambda row: conti_data[row.arrival_continent]["lat"], axis=1
    )

    continental_flows_non_dir["dep_lon"] = continental_flows_non_dir.apply(
        lambda row: conti_data[row.group_col[0]]["lon"], axis=1
    )
    continental_flows_non_dir["dep_lat"] = continental_flows_non_dir.apply(
        lambda row: conti_data[row.group_col[0]]["lat"], axis=1
    )
    continental_flows_non_dir["arr_lon"] = continental_flows_non_dir.apply(
        lambda row: conti_data[row.group_col[1]]["lon"], axis=1
    )
    continental_flows_non_dir["arr_lat"] = continental_flows_non_dir.apply(
        lambda row: conti_data[row.group_col[1]]["lat"], axis=1
    )

    continental_flows_non_dir[["AV1", "AV2"]] = (
        continental_flows_non_dir["group_col"].copy().apply(lambda x: pd.Series(x))
    )

    # Creating a nother df to compute the flights remainign in and going out of a continent for plotting

    sub = continental_flows.copy()
    sub["inside"] = sub["departure_continent"] == sub["arrival_continent"]
    conti_scatter = (
        sub.groupby(
            [
                "departure_continent",
                "departure_continent_name",
                "inside",
                "dep_lon",
                "dep_lat",
            ]
        )[["seats", "ask", "fuel_burn", "co2", "CO2 (Mt)", "ASK (Bn)", "Seats (Mn)"]]
        .sum()
        .reset_index()
    )

    ## Countries df
    country_flows = (
        flights_df.groupby(
            [
                "departure_country",
                "arrival_country",
                "departure_country_name",
                "arrival_country_name",
                "departure_ISO3",
                "arrival_ISO3",
            ]
        )[["seats", "ask", "fuel_burn", "co2", "CO2 (Mt)", "ASK (Bn)", "Seats (Mn)"]]
        .sum()
        .reset_index()
    )

    country_fixed = (
        flights_df.groupby(
            ["departure_country", "departure_country_name", "departure_ISO3"]
        )
        .agg(
            {
                "seats": "sum",
                "ask": "sum",
                "fuel_burn": "sum",
                "co2": "sum",
                "CO2 (Mt)": "sum",
                "ASK (Bn)": "sum",
                "Seats (Mn)": "sum",
                "domestic": "mean",  # Calculate the share of 'domestic'
            }
        )
        .reset_index()
    )

    ## ADD country coordinates for better plots -> source:
    # https: // gist.github.com / metal3d / 5
    # b925077e66194551df949de64e910f6
    country_coord = pd.read_csv(
        "data/country-coord.csv",
        keep_default_na=False,
        na_values=["", "NaN"],
        index_col=0,
    )
    country_coord = country_coord[
        ["Alpha-3 code", "Latitude (average)", "Longitude (average)"]
    ]

    country_flows = country_flows.merge(
        country_coord, left_on="departure_ISO3", right_on="Alpha-3 code", how="left"
    )
    country_flows.rename(
        columns={
            "Latitude (average)": "departure_lat",
            "Longitude (average)": "departure_lon",
        },
        inplace=True,
    )
    country_flows.drop(columns={"Alpha-3 code"}, inplace=True)

    country_flows = country_flows.merge(
        country_coord, left_on="arrival_ISO3", right_on="Alpha-3 code", how="left"
    )
    country_flows.rename(
        columns={
            "Latitude (average)": "arrival_lat",
            "Longitude (average)": "arrival_lon",
        },
        inplace=True,
    )
    country_flows.drop(columns={"Alpha-3 code"}, inplace=True)

    # Create a set of unique departure countries
    unique_ctry = set(country_flows["departure_country"])

    colors_discrete_ctry = [
        "#FF0000",
        "#FF00FF",
        "#00FF00",
        "#0000FF",
        "#FFFF00",
        "#FF7D00",
        "#FF7D7D",
        "#7DFF7D",
        "#00FFFF",
        "#7D00FF",
        "#7D7DFF",
        "#007DFF",
        "#007D00",
        "#7D0000",
        "#7D007D",
        "#00007D",
        "#99FFFF",
        "#FF99FF",
        "#99FF99",
        "#9999FF",
    ]

    # Create a random color mapping for each unique departure country
    color_mapping = {ctry: random.choice(colors_discrete_ctry) for ctry in unique_ctry}

    # Add a new column 'color' to the DataFrame with the random colors
    country_flows["color"] = country_flows["departure_country"].map(color_mapping)

    country_fixed = country_fixed.merge(
        country_coord, left_on="departure_ISO3", right_on="Alpha-3 code", how="left"
    )
    country_fixed.rename(
        columns={
            "Latitude (average)": "departure_lat",
            "Longitude (average)": "departure_lon",
        },
        inplace=True,
    )
    country_fixed.drop(columns={"Alpha-3 code"}, inplace=True)

    # ### Add country socioeco data
    # world_bank_data= pd.read_csv('../02_airport_features/data/world_bank_data.csv')

    # save continental level data
    continental_flows.to_csv("./plot_files/continental_flows.csv")
    continental_flows_non_dir.to_csv("./plot_files/continental_flows_non_dir.csv")
    conti_scatter.to_csv("./plot_files/conti_scatter.csv")

    # save country level data
    country_flows.to_csv("./plot_files/country_flows.csv")
    country_fixed.to_csv("./plot_files/country_fixed.csv")

    # save flight_level_data
    flights_df.to_csv("./plot_files/flights_df.zip", compression="zip")
