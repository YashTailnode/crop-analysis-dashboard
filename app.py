import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng


df = pd.read_csv(
    "/home/yash/Repositories/crop-analysis-dashboard/data/India Agriculture Crop Production.csv"
)


DF_COLUMNS = [
    "State",
    "District",
    "Crop",
    "Year",
    "Season",
    "Area",
    "Area Units",
    "Production",
    "Production Units",
    "Yield",
]
# print(df['year'].unique())
unique_year_options = df["Year"].unique()
unique_state_options = df["State"].unique()
unique_crop_options = df["Crop"].unique()
unique_district_options = df["District"].unique()
unique_season_options = df["Season"].unique()
# //convert tabs to horizontal tabs
tab1, tab2 = st.tabs(["Dashboard", "Map View"], width="stretch")


with tab1:
    st.header("Crop Production Yeild Dashboard")
    years = st.multiselect(
        "Select Year(s)",
        unique_year_options,
        default=[
            "2001-02",
            "2002-03",
            "2003-04",
            #  '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21'
        ],
    )
    crops = st.multiselect(
        "Select Crop(s)",
        unique_crop_options,
        # default=["Wheat"],
    )
    states = st.multiselect(
        "Select State(s)",
        unique_state_options,
        default=["Maharashtra", "Jharkhand", "Gujarat", "Punjab", "Haryana"],
    )
    districts = st.multiselect(
        "Select District(s)",
        df[df["State"].isin(states)]["District"].unique(),
        # default=["2001-02"],
    )
    seasons = st.multiselect(
        "Select Season(s)",
        unique_season_options,
        # default=["2001-02"],
    )

    # filter dataframe based on selections
    df_filtered = df[
        (df["Year"].isin(years) if years else True)
        & (df["Crop"].isin(crops) if crops else True)
        & (df["State"].isin(states) if states else True)
        & (df["District"].isin(districts) if districts else True)
        & (df["Season"].isin(seasons) if seasons else True)
    ]

    # MATRIX
    corr_cols = ["Area", "Production", "Yield"]
    correlation = df_filtered[corr_cols].corr()
    st.subheader(f"Correlation Matrix between {', '.join(corr_cols)}")
    if not df_filtered.empty:
        st.dataframe(correlation)
    else:
        st.write("No data!")

    # PRODUCTION , YEILD OVER YEARS
    st.subheader("Production and Yield VS Years")

    if not df_filtered.empty:
        production_yield_over_years = (
            df_filtered.groupby("Year")[["Production", "Yield"]].sum().reset_index()
        )
        production_yield_over_years["normalized_production"] = (
            production_yield_over_years["Production"]
            / production_yield_over_years["Production"].max()
        )
        production_yield_over_years["normalized_yield"] = (
            production_yield_over_years["Yield"]
            / production_yield_over_years["Yield"].max()
        )
        # st.dataframe(production_yield_over_years)
        st.bar_chart(
            production_yield_over_years,
            x="Year",
            y=["normalized_production", "normalized_yield"],
            color=["#FF0000", "#0000FF"],
        )
    else:
        st.write("No data!")

    # TOP Producting Districts
    st.subheader("TOP Producing Districts")

    if not df_filtered.empty:
        production_for_districts = (
            df_filtered.groupby("District")["Production"].sum().reset_index()
        )
        top_10_production_districts = production_for_districts.sort_values(
            "Production", ascending=False
        ).head(10)
        # st.dataframe(production_for_districts)
        st.bar_chart(
            top_10_production_districts,
            x="District",
            y="Production",
            color=["#FF0000"],
        )
    else:
        st.write("No data!")

    # Yeild Vs Area
    st.subheader("Yield Vs Production Area")

    if not df_filtered.empty:
        # production_for_districts = (
        #     df_filtered.groupby("District")["Production"].sum().reset_index()
        # )
        # top_10_production_districts = production_for_districts.sort_values(
        #     "Production", ascending=False
        # ).head(10)
        # st.dataframe(production_for_districts)
        yeild_production_area = df_filtered[["Area", "Yield"]]
        st.scatter_chart(
            yeild_production_area,
        )
    else:
        st.write("No data!")

    # CROPWISE YEARLY PRODUCTION
    st.subheader("Crop-wise Production")

    if not df_filtered.empty:
        yearly_crop_production = (
            df_filtered.groupby(["Year", "Crop"])[["Production"]].sum().reset_index()
        )
        yearly_crop_production["crop_year"] = (
            yearly_crop_production["Crop"]
            + " - "
            + yearly_crop_production["Year"].astype(str)
        )
        # production_yield_over_years["normalized_production"] = (
        #     production_yield_over_years["Production"]
        #     / production_yield_over_years["Production"].max()
        # )
        # production_yield_over_years["normalized_yield"] = (
        #     production_yield_over_years["Yield"]
        #     / production_yield_over_years["Yield"].max()
        # )
        # st.dataframe(yearly_crop_production)
        st.bar_chart(
            yearly_crop_production,
            x="crop_year",
            y=["Production"],
            # color=["#FF0000", "#0000FF"],
        )
    else:
        st.write("No data!")

    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("Crop Production Yeild Dashboard")
    # st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
# with tab3:
# st.header("An owl")
# st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
