import streamlit as st

def initializeSessionState():
    # Initialize the log in state if does not exist
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    # Initialize the Project setting in state if does not exist
    if "plant_selectbox_index" not in st.session_state:
        st.session_state.plant_selectbox_index = 0
    if "Plant" not in st.session_state:
        st.session_state.Plant = "Plant-1"

    # Initialize the Node setting in state if does not exist
    if "machine_selectbox_index" not in st.session_state:
        st.session_state.machine_selectbox_index = 0
    if "Machine" not in st.session_state:
        st.session_state.Machine = "Machine-1"

    # helper variable
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "clear_cache" not in st.session_state:
        st.session_state.clear_cache=False

    # Store Device Status
    if "device_status" not in st.session_state:
        st.session_state.device_status = "Offline"
    

    # ============ TFO Twisting Machine Parameters ===============
    
    # ----- Settings ----
    if "show_charts" not in st.session_state:
        st.session_state.show_charts = True

    # ----- Varables -----
    if "last_updated_parameters_timestamps" not in st.session_state:
        st.session_state.last_updated_parameters_timestamps =0

    if "nominal_spindle_speed" not in st.session_state:
        st.session_state.nominal_spindle_speed = 0

    if "actual_spindle_speed" not in st.session_state:
        st.session_state.actual_spindle_speed = 0

    if "twist_per_inch" not in st.session_state:
        st.session_state.twist_per_inch = 0

    if "nominal_delivery_speed" not in st.session_state:
        st.session_state.nominal_delivery_speed = 0

    if "actual_delivery_speed" not in st.session_state:
        st.session_state.actual_delivery_speed = 0

    if "total_spindle_running_status" not in st.session_state:
        st.session_state.total_spindle_running_status = 0
    
    # Spindle Running Status
    if "slave_1_spindles_running_status_percentage" not in st.session_state:
        st.session_state.slave_1_spindles_running_status_percentage = ""

    if "slave_2_spindles_running_status_percentage" not in st.session_state:
        st.session_state.slave_2_spindles_running_status_percentage = ""

    if "spindle_health_status" not in st.session_state:
        st.session_state.spindle_health_status = []



    # *************** Settings ********************************

    if "show_parameters_section" not in st.session_state:
        st.session_state.show_parameters_section = True

    if "show_section_wise_spindle_status_section" not in st.session_state:
        st.session_state.show_section_wise_spindle_status_section = True

    
