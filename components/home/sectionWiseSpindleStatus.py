import streamlit as st # type: ignore
import pandas as pd # type: ignore

# ================= Spindle Status section ====================================
def sectionWiseSpindleStatus_section():
    with st.container(border=True):
        org_subheading = st.columns([0.4, 1], vertical_alignment="bottom")
        with org_subheading[0]:
            st.subheader(body="Section Wise Spindle Status", anchor=False)

        spindle_health_status=st.session_state.spindle_health_status
        if spindle_health_status is None:
            
            st.stop()
        # Create the DataFrame
        d = {'Section Running Status': [st.session_state.slave_1_spindles_running_status_percentage, st.session_state.slave_2_spindles_running_status_percentage],
            'Spindle -1': [spindle_health_status[0][0], spindle_health_status[1][0]],
            'Spindle -2': [spindle_health_status[0][1], spindle_health_status[1][1]],
            'Spindle -3': [spindle_health_status[0][2], spindle_health_status[1][2]],
            'Spindle -4': [spindle_health_status[0][3], spindle_health_status[1][3]],
            'Spindle -5': [spindle_health_status[0][4], spindle_health_status[1][4]],
            'Spindle -6': [spindle_health_status[0][5], spindle_health_status[1][5]],
            'Spindle -7': [spindle_health_status[0][6], spindle_health_status[1][6]],
            'Spindle -8': [spindle_health_status[0][7], spindle_health_status[1][7]],
            'Spindle -9': [spindle_health_status[0][8], spindle_health_status[1][8]],
            'Spindle -10': [spindle_health_status[0][9], spindle_health_status[1][9]],
            }

        df = pd.DataFrame(data=d, index=["Section-1", "Section-2"])

        # Function to color the "Healthy" or "Faulty" cells
        def color_cells(val):
            if val.find("%") != -1:
                value=int(val.split(".")[0])
                if value<100:
                    return 'background-color: #E33025'
                elif value==100:
                    return 'background-color: #00CC00'
            elif val == "Healthy":
                return 'background-color:  #00CC00'
            elif val == "Faulty":
                return 'background-color: #E33025'
            
            return ''  # For cells that don't match

        # Apply styling to the Spindle columns (ignoring 'Section Running Status')
        styled_df = df.style.map(color_cells, subset=df.columns[0:]) # type: ignore

        # Display the styled dataframe in Streamlit
        st.table(styled_df)