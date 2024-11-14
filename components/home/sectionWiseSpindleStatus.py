import streamlit as st # type: ignore
import pandas as pd # type: ignore

# ================= Spindle Status section ====================================
def sectionWiseSpindleStatus_section():
    with st.container(border=True):
        org_subheading = st.columns([0.4, 1], vertical_alignment="bottom")
        with org_subheading[0]:
            st.subheader(body="Section Wise Spindle Status", anchor=False)

        # Create the DataFrame
        d = {'Section Running Status': ["70%", "50%"],
            'Spindle -1': ["Healthy", "Faulty"],
            'Spindle -2': ["Healthy", "Healthy"],
            'Spindle -3': ["Healthy", "Healthy"],
            'Spindle -4': ["Faulty", "Faulty"],
            'Spindle -5': ["Faulty", "Faulty"],
            'Spindle -6': ["Healthy", "Faulty"],
            'Spindle -7': ["Healthy", "Faulty"],
            'Spindle -8': ["Healthy", "Faulty"],
            'Spindle -9': ["Healthy", "Faulty"],
            'Spindle -10': ["Faulty", "Faulty"]
            }

        df = pd.DataFrame(data=d, index=["Section-1", "Section-2"])

        # Function to color the "Healthy" or "Faulty" cells
        def color_cells(val):
            if val == "Healthy":
                return 'background-color:  #00CC00'
            elif val == "Faulty":
                return 'background-color: #E33025'
            return ''  # For cells that don't match

        # Apply styling to the Spindle columns (ignoring 'Section Running Status')
        styled_df = df.style.map(color_cells, subset=df.columns[1:]) # type: ignore

        # Display the styled dataframe in Streamlit
        st.table(styled_df)