import streamviz
import streamlit as st


def parameters_section():
    # ================= Parameter Listing section ====================================
    with st.container(border=True):
        org_subheading = st.columns([0.27, 1, 1], vertical_alignment="bottom")
        with org_subheading[0]:
            st.subheader(body="Parameters", anchor=False)
        with org_subheading[1]:
            st.write(st.session_state.last_updated_parameters_timestamps)

        # -------------------Parameters Selection section -------------------------------------
        param_selection_cols1 = st.columns(
            [1, 1, 1, 0.5], gap="medium", vertical_alignment="center"
        )
        # Column 1
        with param_selection_cols1[0]:
            projects = st.selectbox(
                label="Select Plants",
                placeholder="Select Plant",
                options=["Plant 1"],
                index=0,
            )
            Project = projects.split()
            if st.session_state.Project != (int(Project[1]) - 1):
                st.session_state.Project = int(Project[1]) - 1
                st.rerun()
        # Column 2
        with param_selection_cols1[1]:
            machines = st.selectbox(
                label="Select Machine",
                options=["Machine 1", "Machine 2"],
                index=0,
                placeholder="Select Machine",
            )
            machine = machines.split()
            if st.session_state.Node != int(machine[1]):
                st.session_state.Node = int(machine[1])
                st.rerun()
        # with param_selection_cols1[3]:
        #     show_charts = st.toggle(
        #         label="Show Charts",
        #         key="show_charts",
        #         value=st.session_state.show_charts,
        #         label_visibility="visible",
        #     )

        # -------------------Parameters Gauge section -------------------------------------
        cols1 = st.columns([1, 1, 1], gap="medium", vertical_alignment="center")
        with cols1[0]:
            streamviz.gauge(
                gVal=st.session_state.nominal_spindle_speed,
                gTitle="Nominal Spindle Speed",
                gMode="gauge+number",
                gSize="MED",
                grLow=30,
                gcLow="blue",
                grMid=60,
                gcMid="green",
                gcHigh="red",
                arBot=0,
                arTop=100,
                sFix="RPM",
            )
        with cols1[1]:
            streamviz.gauge(
                gVal=st.session_state.actual_spindle_speed,
                gTitle="Actual Spindle Speed",
                gMode="gauge+number",
                gSize="MED",
                grLow=40,
                gcLow="green",
                grMid=50,
                gcMid="orange",
                gcHigh="red",
                sFix="RPM",
                arBot=0,
                arTop=100,
                cWidth=True,
            )
        with cols1[2]:
            streamviz.gauge(
                gVal=st.session_state.twist_per_inch,
                gTitle="Twist Per Inch(TPI)",
                gMode="gauge+number",
                gSize="MED",
                grLow=4,
                gcLow="red",
                grMid=9,
                gcMid="green",
                gcHigh="red",
                sFix="RPM",
                arBot=0,
                arTop=12,
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
                grLow=60,
                gcLow="green",
                grMid=50,
                gcMid="orange",
                gcHigh="red",
                sFix="RPM",
                arBot=0,
                arTop=100,
                cWidth=True,
            )
        with cols2[1]:
            streamviz.gauge(
                gVal=st.session_state.actual_delivery_speed,
                gTitle="Actual Delivery Speed",
                gMode="gauge+number",
                gSize="MED",
                grLow=60,
                gcLow="green",
                grMid=50,
                gcMid="orange",
                gcHigh="red",
                sFix="RPM",
                arBot=0,
                arTop=100,
                cWidth=True,
            )
        with cols2[2]:
            streamviz.gauge(
                gVal=st.session_state.total_spindle_running_status,
                gTitle="Total Spindle Running Status ",
                gMode="number",
                gSize="MED",
                grLow=7,
                gcLow="red",
                grMid=14,
                gcMid="orange",
                gcHigh="green",
                sFix="/20",
                arBot=0,
                arTop=100,
                cWidth=True,
            )
