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
        nss_value=st.session_state.nominal_spindle_speed
        nss_gauge_topRange=nss_value+50
        if nss_value>100:
            nss_gauge_topRange=nss_value+80
        elif nss_value>500:
            nss_gauge_topRange=nss_value+100
        elif nss_value>1000:
            nss_gauge_topRange=nss_value+250
        elif nss_value>4000:
            nss_gauge_topRange=nss_value+500
        elif nss_value>8000:
            nss_gauge_topRange=nss_value+1000
        elif nss_value>15000:
            nss_gauge_topRange=nss_value+5000

        streamviz.gauge(
            gVal=nss_value,
            gTitle="Nominal Spindle Speed",
            gMode="gauge+number",
            grLow=30000,
            gcLow="#1cf342",
            gSize="MED",
            arBot=0,
            arTop=nss_gauge_topRange,
            sFix="RPM",
        )
    with cols1[1]:
        ass_value=st.session_state.actual_spindle_speed
        ass_gauge_topRange=ass_value+50
        if ass_value>100:
            ass_gauge_topRange=ass_value+80
        elif ass_value>500:
            ass_gauge_topRange=ass_value+100
        elif ass_value>1000:
            ass_gauge_topRange=ass_value+250
        elif ass_value>4000:
            ass_gauge_topRange=ass_value+500
        elif ass_value>8000:
            ass_gauge_topRange=ass_value+1000
        elif ass_value>15000:
            ass_gauge_topRange=ass_value+5000

        streamviz.gauge(
            gVal=st.session_state.actual_spindle_speed,
            gTitle="Actual Spindle Speed",
            gMode="gauge+number",
            gSize="MED",
            grLow=30000,
            gcLow="#1cf342",
            sFix="RPM",
            arBot=0,
            arTop=ass_gauge_topRange,
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
        nds_value=st.session_state.nominal_delivery_speed
        nds_gauge_topRange=nds_value+50
        if nds_value>100:
            nds_gauge_topRange=nds_value+80
        elif nds_value>500:
            nds_gauge_topRange=nds_value+100
        elif nds_value>1000:
            nds_gauge_topRange=nds_value+250
        elif nds_value>4000:
            nds_gauge_topRange=nds_value+500
        elif nds_value>8000:
            nds_gauge_topRange=nds_value+1000
        elif nds_value>15000:
            nds_gauge_topRange=nds_value+5000

        streamviz.gauge(
            gVal=nds_value,
            gTitle="Nominal Delivery Speed",
            gMode="gauge+number",
            gSize="MED",
            grLow=1000,
            gcLow="#1cf342",
            sFix="RPM",
            arBot=0,
            arTop=nds_gauge_topRange,
            cWidth=True,
        )
    with cols2[1]:
        ads_value=st.session_state.actual_delivery_speed
        ads_gauge_topRange=ads_value+50
        if ads_value>100:
            ads_gauge_topRange=ads_value+80
        elif ads_value>500:
            ads_gauge_topRange=ads_value+100
        elif ads_value>1000:
            ads_gauge_topRange=ads_value+250
        elif ads_value>4000:
            ads_gauge_topRange=ads_value+500
        elif ads_value>8000:
            ads_gauge_topRange=ads_value+1000
        elif ads_value>15000:
            ads_gauge_topRange=ads_value+5000

        streamviz.gauge(
            gVal=ads_value,
            gTitle="Actual Delivery Speed",
            gMode="gauge+number",
            gSize="MED",
            grLow=1000,
            gcLow="#1cf342",
            sFix="RPM",
            arBot=0,
            arTop=ads_gauge_topRange,
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
