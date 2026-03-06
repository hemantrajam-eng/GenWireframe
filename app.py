import streamlit as st
from xml_parser import parse_layout_xml
from wireframe_generator import generate_wireframe

st.set_page_config(layout="wide")

st.title("AI Layout → Wireframe Generator")

page_type = st.selectbox(
    "Select Page Type",
    ["Detail Page","Edit Page","Summary Page","Object Home"]
)

uploaded_xml = st.file_uploader(
    "Upload Layout XML",
    type="xml"
)

if uploaded_xml:

    # Load XML only first time
    if "layout_df" not in st.session_state:

        df = parse_layout_xml(uploaded_xml)

        df["DemoValue"] = df["DemoValue"].astype(str)

        st.session_state.layout_df = df


    st.subheader("Editable Demo Data")

    edited_df = st.data_editor(
        st.session_state.layout_df,
        key="demo_editor",
        use_container_width=True,
        num_rows="dynamic"
    )

    # Save updated values
    st.session_state.layout_df = edited_df

    st.subheader("Generated Wireframe")

    generate_wireframe(edited_df, page_type)