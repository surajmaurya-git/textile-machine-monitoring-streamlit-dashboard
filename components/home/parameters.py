import streamviz
import streamlit as st


def parameters_section():
    # ================= Parameter Listing section ====================================
    with st.container(border=True):
        org_subheading = st.columns([0.27, 1, 1], vertical_alignment="bottom")
        with org_subheading[0]:
            st.subheader(body="Parameters", anchor=False)
        with org_subheading[1]:
            if st.session_state.show_parameters_section :
                st.write(st.session_state.last_updated_parameters_timestamps)
        if st.session_state.show_parameters_section :
            draw_gauge()
        else:
            st.warning("No Data Found")

def draw_gauge():
    # -------------------Parameters Gauge section -------------------------------------
    cols1 = st.columns([1, 1, 1], gap="medium", vertical_alignment="center")
    with cols1[0]:
        streamviz.gauge(
            gVal=st.session_state.nominal_spindle_speed,
            gTitle="Nominal Spindle Speed",
            gMode="gauge+number",
            grLow=30000,
            gcLow="#1cf342",
            gSize="MED",
            arBot=0,
            arTop=(
                st.session_state.actual_spindle_speed+50),
            sFix="RPM",
        )
    with cols1[1]:
        streamviz.gauge(
            gVal=st.session_state.actual_spindle_speed,
            gTitle="Actual Spindle Speed",
            gMode="gauge+number",
            gSize="MED",
            grLow=30000,
            gcLow="#1cf342",
            sFix="RPM",
            arBot=0,
            arTop=(
                st.session_state.actual_spindle_speed+50),
            cWidth=True,
        )
    with cols1[2]:
        streamviz.gauge(
            gVal=st.session_state.twist_per_inch,
            gTitle="Twist Per Inch(TPI)",
            gMode="number",
            gSize="MED",
            cWidth=True,
        )
    # Column 2
    cols2 = st.columns([1, 1, 1], gap="medium", vertical_alignment="center")
    with cols2[0]:
        streamviz.gauge(
            gVal=st.session_state.nominal_delivery_speed,
            gTitle="Nominal Delivery Speed",
            gMode="gauge+number",
            gSize="MED",
            grLow=1000,
            gcLow="#1cf342",
            sFix="RPM",
            arBot=0,
            arTop=(
                st.session_state.actual_delivery_speed+10),
            cWidth=True,
        )
    with cols2[1]:
        streamviz.gauge(
            gVal=st.session_state.actual_delivery_speed,
            gTitle="Actual Delivery Speed",
            gMode="gauge+number",
            gSize="MED",
            grLow=1000,
            gcLow="#1cf342",
            sFix="RPM",
            arBot=0,
            arTop=(
                st.session_state.actual_delivery_speed+10),
            cWidth=True,
        )
    with cols2[2]:
        streamviz.gauge(
            gVal=st.session_state.total_spindle_running_status,
            gTitle="Total Spindle Running Status ",
            gMode="number",
            gSize="MED",
            sFix="/20",
        )
