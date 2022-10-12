import datetime as dt
import streamlit as st
import pandas as pd
import pydeck as pdk

backend = "http://127.0.0.1:3000/"

options = (
    '<select>',
    'HOMICIDE',
    'CRIM SEXUAL ASSAULT',
    'CRIMINAL SEXUAL ASSAULT',
    'ROBBERY',
    'BATTERY',
    'PUBLIC PEACE VIOLATION',
    'ASSAULT',
    'STALKING',
    'BURGLARY',
    'THEFT',
    'MOTOR VEHICLE THEFT',
    'ARSON',
    'HUMAN TRAFFICKING',
    'DECEPTIVE PRACTICE',
    'CRIMINAL DAMAGE',
    'CRIMINAL TRESPASS',
    'WEAPONS VIOLATION',
    'CONCEALED CARRY LICENSE VIOLATION',
    'PROSTITUTION',
    'SEX OFFENSE',
    'OFFENSE INVOLVING CHILDREN',
    'GAMBLING',
    'NARCOTICS',
    'LIQUOR LAW VIOLATION',
    'OTHER OFFENSE',
    'INTERFERENCE WITH PUBLIC OFFICER',
    'INTIMIDATION',
    'KIDNAPPING',
    'NON-CRIMINAL',
    'OBSCENITY',
    'OTHER NARCOTIC VIOLATION',
    'PUBLIC INDECENCY',
    'NON - CRIMINAL',
    'NON-CRIMINAL (SUBJECT SPECIFIED)',
    'RITUALISM',
    'DOMESTIC VIOLENCE'
)

@st.cache(suppress_st_warning=True)
def all_crimes_process() -> pd.DataFrame:
    """ function returns and caches dataframe with all crimes in Chicago. """
    return pd.read_json(backend)

@st.cache(suppress_st_warning=True)
def date_process(date: dt.date) -> pd.DataFrame:
    """ function returns and caches dataframe with crimes filtered by date. """
    if date != dt.date.today() + dt.timedelta(days=1):
        return pd.read_json(backend + 'date?date=' + str(date))

@st.cache(suppress_st_warning=True)
def type_process(option: str) -> pd.DataFrame:
    """ function returns and caches dataframe with crimes filtered by type. """
    if option != '<select>':
        return pd.read_json(backend + 'type?primary_type=' + option.replace(' ', '%20'))

st.title("Task for Objective Platform")

st.write(
    """
    Test task for Objective Platform, which shows you map with
    crimes commited in Chicago. You may filter it by type of crime
    or by date it was commited.
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
            zoom=7
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_all,
                get_position=['longitude', 'latitude'],
                get_color=[0, 0, 200, 160],
                get_radius=800,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_dates,
                get_position=['longitude', 'latitude'],
                get_color=[200, 0, 0, 160],
                get_radius=800,
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
