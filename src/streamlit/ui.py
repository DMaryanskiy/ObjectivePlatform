import datetime as dt
import json
import streamlit as st
import pandas as pd
import pydeck as pdk

backend = "http://backend:3000/" # url for API.

options = json.load(open('options.json')) # getting type of crimes from JSON file.

@st.cache(suppress_st_warning=True, show_spinner=False)
def all_crimes_process() -> pd.DataFrame:
    """ function returns and caches dataframe with all crimes in Chicago. """
    return pd.read_json(backend)

@st.cache(suppress_st_warning=True, show_spinner=False)
def date_process(date: dt.date) -> pd.DataFrame:
    """ function returns and caches dataframe with crimes filtered by date. """
    return pd.read_json(backend + 'date?date=' + str(date))

@st.cache(suppress_st_warning=True, show_spinner=False)
def type_process(option: str) -> pd.DataFrame:
    """ function returns and caches dataframe with crimes filtered by type. """
    return pd.read_json(backend + 'type?primary_type=' + option.replace(' ', '%20'))

# adding attributes to store values of last interaction.
if 'option' not in st.session_state:
    st.session_state.option = '<select>'

if 'date' not in st.session_state:
    st.session_state.date = dt.date.today() + dt.timedelta(days=1)

# showing title and description.
st.title("Task for Objective Platform")

st.write(
    """
    Test task for Objective Platform, which shows you map with
    crimes commited in Chicago. You may filter it by type of crime
    or by date it was commited. Due to weak computer power
    I'll show only crimes, which were commited within the last year.
    """
)

# adding input widgets.
date = st.date_input(
    label="Choose the date of crime:",
    value=dt.date.today() + dt.timedelta(days=1)
) # streamlit doesn't support empty values at the moment.

option = st.selectbox(
    label="Choose the type of crime:",
    options=options
)

merge_df = st.checkbox(label="Show crimes filtered by date and type simultaneously")

df = all_crimes_process() # dataframe with coords of all crimes.

# checking input and getting necessary data using API.
if date < st.session_state.date:
    st.session_state.date = date
    df = date_process(date) # dataframe with coords of crimes filtered by date.
else:
    st.session_state.date = dt.date.today() + dt.timedelta(days=1)

if option != st.session_state.option:
    st.session_state.option = option
    df = type_process(option) # dataframe with coords of crimes filtered by type.
else:
    st.session_state.option = '<select>'

if merge_df:
    # data gets out of cache, so it doesn't take much time.
    df = pd.merge(date_process(date), type_process(option), "outer")

# adding map.
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
                data=df,
                get_position=['longitude', 'latitude'],
                get_color=[200, 0, 0, 160],
                get_radius=200,
            ),
        ],
    )
)
