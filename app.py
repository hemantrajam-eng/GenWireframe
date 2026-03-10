import streamlit as st
import pandas as pd

from prompt_to_layout import generate_layout_from_prompt
from layout_to_df import layout_json_to_df
from wireframe_generator import generate_wireframe

st.title("AI Wireframe Generator")

page_type = st.selectbox(
    "Page Type",
    ["Detail Page","New/Edit Page"]
)

st.subheader("Prompt Based Layout")

user_prompt = st.text_area(
    "Describe your screen",
    height=150,
    placeholder="""
Create a CRM case detail page.

Tabs: Summary, Attachments

Summary Tab
Section: Case Information
Fields:
Case Number
Assigned To
Customer Name
CIF
"""
)

if st.button("Generate Wireframe"):

    layout_json = generate_layout_from_prompt(user_prompt)

    df = layout_json_to_df(layout_json)

    st.success("Layout Generated")

    generate_wireframe(df, page_type)
