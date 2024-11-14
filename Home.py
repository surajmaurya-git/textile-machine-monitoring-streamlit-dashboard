"""TFO Twisting Machine Monitoring Dashboard."""

import streamlit as st
import pandas as pd
import os
import pytz
from datetime import date, datetime, timedelta, time
from streamlit_autorefresh import st_autorefresh

from utils.anedya import anedya_config
from utils.anedya import anedya_sendCommand
from utils.anedya import anedya_getValue
from utils.anedya import anedya_setValue
from utils.anedya import fetchHumidityData
from utils.anedya import fetchTemperatureData
from utils.anedya import anedya_get_latestData
from utils.anedya import anedya_getDeviceStatus

from components.intializeSessionState import initializeSessionState   # Initialize Session State
from components.home.parameters import parameters_section
from components.home.sectionWiseSpindleStatus import sectionWiseSpindleStatus_section

st.set_page_config(page_title="Anedya IoT Dashboard", layout="wide")

refresh_interval = 30000
st_autorefresh(interval=refresh_interval, limit=None, key="auto-refresh-handler")

# --------------- HELPER FUNCTIONS -----------------------
def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")

def main():
    initializeSessionState()

    # Manage Anedya Connection Credentials
    API_KEY=st.secrets[st.session_state.Plant]["API_KEY"]
    NODE_ID=st.secrets[st.session_state.Plant][st.session_state.Machine]

    # ---------------------- UI -----------------------
    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        success = anedya_config(API_KEY=API_KEY,NODE_ID=NODE_ID)
        # API_KEY=st.secrets.anedya_connection_credentials.API_KEY
        # NODE_ID=st.secrets.anedya_connection_credentials.NODE_ID
        # success = anedya_config(API_KEY=API_KEY,NODE_ID=NODE_ID)
        if not success:
            st.stop()
        else:
            drawDashboard()



def drawLogin():
    cols = st.columns([1, 1, 1], gap="small")
    with cols[0]:
        pass
    with cols[1]:
        st.title("TFO Twisting Machine Monitoring", anchor=False)
        username_inp = st.text_input("Username")
        password_inp = st.text_input("Password", type="password")
        submit_button = st.button(label="Submit")

        if submit_button:
            if username_inp == "admin" and password_inp == "admin":
                st.session_state.LoggedIn = True
                st.rerun()
            else:
                st.error("Invalid Credential!")
    with cols[2]:
        print()


def drawDashboard():

    deviceState = anedya_getDeviceStatus()
    if deviceState[1]:
        if deviceState[0]:
            st.session_state.device_status = "Online"
        else:
            st.session_state.device_status = "Offline"

    # ============ Update Parameters ===============
    data=anedya_get_latestData("SPRPMNM")
    st.session_state.nominal_spindle_speed= data[0]
    st.session_state.actual_spindle_speed= 12.78
    st.session_state.twist_per_inch= 5.6
    st.session_state.nominal_delivery_speed = 56.56
    st.session_state.actual_delivery_speed = 89.45
    st.session_state.total_spindle_running_status = 9
    
    # Convert epoch time to datetime
    epoch_time =data[1]
    indian_time_zone = pytz.timezone('Asia/Kolkata')
    unforamted_current_temp_data_datetime = datetime.fromtimestamp(epoch_time, indian_time_zone)
    st.session_state.last_updated_parameters_timestamps=unforamted_current_temp_data_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')

    headercols = st.columns([1, 0.1, 0.1, 0.1], gap="small")
    with headercols[0]:
        st.title("TFO Twisting Machine Monitoring", anchor=False)
    with headercols[1]:
        st.button(label=st.session_state.device_status)
    with headercols[2]:
        st.button("Refresh")
    with headercols[3]:
        logout = st.button("Logout")

    if logout:
        st.session_state.LoggedIn = False
        st.rerun()
    st.markdown("This dashboard provides real-time insight of TFO Twisting Machine.")
    
    # -------------------Select Project and Machine -------------------------------------
    param_selection_cols1 = st.columns(
        [1, 1, 1, 0.5], gap="medium", vertical_alignment="center"
    )
    # Column 1
    with param_selection_cols1[0]:
        Plant = st.selectbox(
            label="Select Plants",
            placeholder="Select Plant",
            options=["Plant-1"],
            index=0,
        )
        if st.session_state.Plant != Plant:
            st.session_state.Plant = Plant
            st.rerun()
    # Column 2
    with param_selection_cols1[1]:
        Machine = st.selectbox(
            label="Select Machine",
            options=["Machine-1"],
            index=0,
            placeholder="Select Machine",
        )
        if st.session_state.Machine !=Machine :
            st.session_state.Machine = Machine
            st.rerun()
    # with param_selection_cols1[3]:
    #     show_charts = st.toggle(
    #         label="Show Charts",
    #         key="show_charts",
    #         value=st.session_state.show_charts,
    #         label_visibility="visible",
    #     )

    # =================== Parameters Section ===================
    parameters_section()

    # =================== Section Wise Spindle Status Section ===================
    sectionWiseSpindleStatus_section()


@st.cache_data(ttl=4, show_spinner=False)
def GetFanStatus() -> list:
    value = anedya_getValue("Fan")
    if value[1] == 1:
        on = value[0]
        if on:
            st.session_state.FanState = True
            st.session_state.FanButtonText = "Turn Fan Off!"
        else:
            st.session_state.FanState = False
            st.session_state.FanButtonText = "Turn Fan On!"
    return value


@st.cache_data(ttl=4, show_spinner=False)
def GetLightStatus() -> list:
    value = anedya_getValue("Light")
    if value[1] == 1:
        on = value[0]
        if on:
            st.session_state.LightState = True
            st.session_state.LightButtonText = "Turn Light Off!"
        else:
            st.session_state.LightState = False
            st.session_state.LightButtonText = "Turn Light On!"
    return value


def auto_update_time_range(param_hold_or_start: bool = True):
    # st.session_state.counter=st.session_state.counter+1
    # st.write(st.session_state.counter)
    if param_hold_or_start:
        st.session_state.var_auto_update_time_range = True
    else:
        st.session_state.var_auto_update_time_range = False


def is_within_tolerance(time1, time2, tolerance=timedelta(seconds=60)):
    datetime1 = datetime.combine(date.min, time1)
    datetime2 = datetime.combine(date.min, time2)
    return abs((datetime1 - datetime2).total_seconds()) <= tolerance.total_seconds()


def get_default_time_range():

    # Get the current date and time in the Indian time zone
    indian_time_zone = pytz.timezone("Asia/Kolkata")
    current_date = datetime.now(indian_time_zone)

    # Extract the year, month, and day
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    # Create a date object
    current_date_object = date(current_year, current_month, current_day)
    # st.session_state.to_date = current_date_object

    # Extract the hour and minute
    hour = current_date.hour
    minute = current_date.minute
    # Create a time object
    current_time_object = time(hour, minute)
    # Assuming `st` is your Streamlit session state
    # st.session_state.to_time = current_time_object

    # Extract the year, month, and day
    reset_date = current_date - timedelta(hours=3.8)
    hour = reset_date.hour
    minute = reset_date.minute
    # Create a date object
    from_time_object = time(hour, minute)
    # st.session_state.from_time = from_time_object

    # Subtract one day to get yesterday's date
    yesterday_date = current_date - timedelta(days=1)
    # Extract the year, month, and day
    yesterday_year = yesterday_date.year
    yesterday_month = yesterday_date.month
    yesterday_day = yesterday_date.day
    # Create a date object for yesterday
    yesterday_date_object = date(yesterday_year, yesterday_month, yesterday_day)
    # st.session_state.from_date = yesterday_date_object

    return [
        current_date_object,
        current_time_object,
        yesterday_date_object,
        from_time_object,
    ]


def reset_time_range():

    default_time_range = get_default_time_range()

    st.session_state.to_date = default_time_range[0]
    st.session_state.to_time = default_time_range[1]
    st.session_state.from_date = default_time_range[2]
    st.session_state.from_time = default_time_range[3]
    # st.write(st.session_state.to_date, st.session_state.to_time, st.session_state.from_date, st.session_state.from_time)
    # st.rerun()


st.cache_data(ttl=10, show_spinner=False)


def update_time_range():
    st.session_state.var_auto_update_time_range = True
    reset_time_range()
    return 0


if __name__ == "__main__":
    main()
