import streamlit as st
def load_css():

    st.markdown("""
    <style>

    /* Section Title */
    .section-title{
        font-size:22px;
        font-weight:600;
        margin-top:25px;
        margin-bottom:10px;
    }

    /* Label styling */
    .field-label{
        font-weight:600;
        color:#0097a7;
        font-size:15px;
    }

    /* Value styling */
    .field-value{
        color:#444;
        font-size:15px;
        padding-top:2px;
    }

    /* Field row spacing */
    .field-row{
        margin-bottom:10px;
    }

    /* Tabs style */
    .stTabs [data-baseweb="tab"]{
        font-size:16px;
        font-weight:500;
    }

    </style>
    """, unsafe_allow_html=True)

def render_control(field):

    label = field["Label"]
    value = field.get("DemoValue", "")
    ftype = field.get("FieldType", "Text")
    key = field.get("FieldId", label)

    if ftype == "Text":
        return st.text_input(label, value=value, key=key)

    elif ftype == "Number":
        try:
            value = int(value)
        except:
            value = 0
        return st.number_input(label, value=value, key=key)

    elif ftype == "Amount":
        try:
            value = float(str(value).replace(",", ""))
        except:
            value = 0.0
        return st.number_input(label, value=value, key=key)

    elif ftype == "Date":
        return st.date_input(label, key=key)

    elif ftype == "Email":
        return st.text_input(label, value=value, key=key)

    elif ftype == "Phone":
        return st.text_input(label, value=value, key=key)

    elif ftype in ["Comments", "LongText"]:
        return st.text_area(label, value=value, key=key)

    elif ftype == "Check":
        return st.checkbox(label, key=key)

    else:
        return st.text_input(label, value=value, key=key)

def render_detail_field(field):

    label = field.get("Label", "")
    value = field.get("DemoValue", "")

    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown(
            f"<div class='field-label'>{label}</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"<div class='field-value'>{value}</div>",
            unsafe_allow_html=True
        )

def generate_wireframe(df, page_type):

    load_css()
    tabs = df["Tab"].dropna().unique().tolist()

    if not tabs:
        tabs = ["Summary"]

    tab_objects = st.tabs(tabs)

    for i, tab in enumerate(tabs):

        with tab_objects[i]:

            tab_df = df[df["Tab"] == tab]

            sections = tab_df["Section"].dropna().unique().tolist()

            for section in sections:

                st.subheader(section)

                sec_df = tab_df[tab_df["Section"] == section]

                rows = sec_df["Row"].unique()

                for r in rows:

                    row_df = sec_df[sec_df["Row"] == r]

                    fields = row_df.to_dict("records")

                    # Remove blank layout placeholders
                    fields = [
                        f for f in fields
                        if f.get("FieldId") and str(f["FieldId"]).lower() != "blankcell"
                    ]

                    if not fields:
                        continue

                    # Single field row
                    if len(fields) == 1:

                        if page_type == "Detail Page":
                            render_detail_field(fields[0])
                        else:
                            render_control(fields[0])

                    # Two column row
                    elif len(fields) >= 2:

                        col1, col2 = st.columns(2)

                        with col1:

                            if page_type == "Detail Page":
                                render_detail_field(fields[0])
                            else:
                                render_control(fields[0])

                        with col2:

                            if page_type == "Detail Page":
                                render_detail_field(fields[1])
                            else:
                                render_control(fields[1])

                st.divider()