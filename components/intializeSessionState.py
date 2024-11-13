import streamlit as st

def initializeSessionState():
    # Initialize the log in state if does not exist
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    # Initialize the Project setting in state if does not exist
    if "Project" not in st.session_state:
        st.session_state.Project = 0

    # Initialize the Node setting in state if does not exist
    if "Node" not in st.session_state:
        st.session_state.Node = 1

    # helper variable
    if "counter" not in st.session_state:
        st.session_state.counter = 0

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