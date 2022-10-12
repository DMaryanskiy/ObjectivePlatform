import datetime as dt
import json
import streamlit as st
import pandas as pd
import pydeck as pdk

backend = "http://backend:3000/"

options = json.load(open('options.json'))

@st.cache(suppress_st_warning=True, show_spinner=False)
def all_crimes_process() -> pd.DataFrame:
    """ function returns and caches dataframe with all crimes in Chicago. """
    return pd.read_json(backend)

@st.cache(suppress_st_warning=True, show_spinner=False)
def date_process(date: dt.date) -> pd.DataFrame:
    """ function returns and caches dataframe with crimes filtered by date. """
    if date != dt.date.today() + dt.timedelta(days=1): # default value for which we shouldn't collect data
        return pd.read_json(backend + 'date?date=' + str(date))

@st.cache(suppress_st_warning=True, show_spinner=False)
def type_process(option: str) -> pd.DataFrame:
    """ function returns and caches dataframe with crimes filtered by type. """
    if option != '<select>': # default value for which we shouldn't collect data
        return pd.read_json(backend + 'type?primary_type=' + option.replace(' ', '%20'))

st.title("Task for Objective Platform")

st.write(
    """
    Test task for Objective Platform, which shows you map with
    crimes commited in Chicago. You may filter it by type of crime
    or by date it was commited. Due to weak computer power
    I'll show only crimes, which were commited within the last 30 days 
    (shown blue).
    """
)

date = st.date_input(
    label="Choose the date of crime (will be shown red):",
    value=dt.date.today() + dt.timedelta(days=1)
) # streamlit doesn't support empty values at the moment

df_dates = pd.DataFrame(columns=['latitude', 'longitude'])
df_dates = date_process(date) # dataframe with coords of crimes filtered by date.

option = st.selectbox(
    label="Choose the type of crime (will be shown green):",
    options=options
)

df_types = pd.DataFrame(columns=['latitude', 'longitude'])
df_types = type_process(option) # dataframe with coords of crimes filtered by type.

df_all = all_crimes_process() # dataframe with coords of all crimes.

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=41.88,
            longitude=-87.66,
            zoom=9
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_all,
                get_position=['longitude', 'latitude'],
                get_color=[0, 0, 200, 160],
                get_radius=200,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_dates,
                get_position=['longitude', 'latitude'],
                get_color=[200, 0, 0, 160],
                get_radius=200,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_types,
                get_position=['longitude', 'latitude'],
                get_color=[0, 200, 0, 160],
                get_radius=200,
            ),
        ],
    )
)
