"""TFO Twisting Machine Monitoring Dashboard."""

import streamlit as st
import pytz
from datetime import date, datetime, timedelta, time
from streamlit_autorefresh import st_autorefresh

from utils.anedya import anedya_config
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
    data=anedya_get_latestData("SPRPMNM",st.session_state.Plant,st.session_state.Machine)
    print(data)
    if data[0] is not None:
        st.session_state.nominal_spindle_speed= data[0]
        st.session_state.show_parameters_section = True
    else:
        print("check-1")
        st.session_state.show_parameters_section = False

    data=anedya_get_latestData("SPRPMAC",st.session_state.Plant,st.session_state.Machine)
    if data[0] is not None:
        st.session_state.actual_spindle_speed= data[0]
        st.session_state.show_parameters_section = True
    else:
       st.session_state.show_parameters_section = False

    data=anedya_get_latestData("TPI",st.session_state.Plant,st.session_state.Machine)
    if data[0] is not None:
        st.session_state.twist_per_inch= data[0]
        st.session_state.show_parameters_section = True
    else:
        st.session_state.show_parameters_section = False

    data=anedya_get_latestData("DLRPMNM",st.session_state.Plant,st.session_state.Machine)
    if data[0] is not None:
        st.session_state.nominal_delivery_speed = data[0]
        st.session_state.show_parameters_section = True
    else:
        st.session_state.show_parameters_section = False

    data=anedya_get_latestData("DLRPMAC",st.session_state.Plant,st.session_state.Machine)
    if data[0] is not None:
        st.session_state.actual_delivery_speed = data[0]
        st.session_state.show_parameters_section = True
    else:
        st.session_state.show_parameters_section = False

    spindle_run_status = spindle_running_status(st.session_state.Plant,st.session_state.Machine)

    st.session_state.total_spindle_running_status = spindle_run_status[0]
    
    # Convert epoch time to datetime
    if data[1] is not None:
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
        on=st.button("Refresh")
        if on:
            st.rerun()
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
            index=st.session_state.plant_selectbox_index,
            key="plants"
        )
        if st.session_state.Plant != Plant:
            st.session_state.Plant = Plant
            index=int(Plant.split("-")[1])
            st.session_state.spindle_health_status=None
            st.session_state.plant_selectbox_index=index-1
            st.rerun()
    # Column 2
    with param_selection_cols1[1]:
        Machine = st.selectbox(
            label="Select Machine",
            options=["Machine-1","Machine-2"],
            key="machines",
            index=st.session_state.machine_selectbox_index,           
            placeholder="Select Machine",
        )
        # st.write(Machine)
        if st.session_state.Machine !=Machine :
            st.session_state.Machine = Machine
            index=int(Machine.split("-")[1])
            st.session_state.machine_selectbox_index=index-1
            st.session_state.spindle_health_status=None
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


@st.cache_data(ttl=1, show_spinner=False)
def spindle_running_status(Plant=None,Machine=None) -> list:
    # Retrieve data for Slave 1
    slave_1_data_list = [anedya_get_latestData(f"S1DI{i}",st.session_state.Plant,st.session_state.Machine)[0] for i in range(1, 12)]
    slave_1_assign_health_status_list = [
        "Healthy" if x == 1 else "Faulty" if x == 0 else "No Data" 
        for x in slave_1_data_list
    ]
    
    # Calculate Slave 1 spindle running status
    slave_1_spindle_running_status = sum(1 for x in slave_1_data_list if x == 1)
    slave_1_total_spindles = len(slave_1_data_list)-1
    st.session_state.slave_1_spindles_running_status_percentage = f"{(slave_1_spindle_running_status / slave_1_total_spindles) * 100:.2f}%"

    # Retrieve data for Slave 2
    slave_2_data_list = [anedya_get_latestData(f"S2DI{i}",st.session_state.Plant,st.session_state.Machine)[0] for i in range(1, 12)]
    slave_2_assign_health_status_list = [
        "Healthy" if x == 1 else "Faulty" if x == 0 else "No Data" 
        for x in slave_2_data_list
    ]
    
    # Calculate Slave 2 spindle running status
    slave_2_spindle_running_status = sum(1 for x in slave_2_data_list if x == 1)
    slave_2_total_spindles = len(slave_2_data_list)-1
    st.session_state.slave_2_spindles_running_status_percentage = f"{(slave_2_spindle_running_status / slave_2_total_spindles) * 100:.2f}%"

    # Total spindle running status
    total_spindles_running_status = slave_1_spindle_running_status + slave_2_spindle_running_status
    
    st.session_state.spindle_health_status = [slave_1_assign_health_status_list,slave_2_assign_health_status_list]

    return [total_spindles_running_status]


if __name__ == "__main__":
    main()
