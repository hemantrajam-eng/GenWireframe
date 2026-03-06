import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* App background */
    .main {
        background-color:#f5f6f7;
    }

    /* Header card */
    .header-card{
        background:white;
        padding:15px;
        border-radius:6px;
        margin-bottom:15px;
        box-shadow:0 1px 3px rgba(0,0,0,0.1);
    }

    .header-title{
        font-size:18px;
        font-weight:600;
    }

    .header-value{
        color:#0097a7;
        font-weight:500;
    }

    /* Section Title */
    .section-title{
        font-size:22px;
        font-weight:600;
        margin-top:20px;
        margin-bottom:10px;
    }

    /* Field label */
    .field-label{
        font-weight:600;
        color:#444;
        font-size:15px;
    }

    /* Field value */
    .field-value{
        color:#0097a7;
        font-size:15px;
    }

    /* Sidebar */
    .sidebar {
        background:#0aa89e;
        height:100vh;
        padding-top:20px;
    }

    .sidebar-icon{
        font-size:22px;
        text-align:center;
        margin:25px 0;
        color:white;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"]{
        font-size:16px;
        font-weight:500;
        padding-bottom:10px;
    }

    .stTabs [aria-selected="true"]{
        border-bottom:3px solid red;
    }

    </style>
    """, unsafe_allow_html=True)


def render_header(df):

    header_fields = ["Case Number", "Sub Category", "Raised On Date", "Customer Closure Date"]

    header_data = df[df["Label"].isin(header_fields)]

    if header_data.empty:
        return

    st.markdown("<div class='header-card'>", unsafe_allow_html=True)

    cols = st.columns(len(header_data))

    for i, row in enumerate(header_data.itertuples()):

        with cols[i]:

            st.markdown(
                f"""
                <div class="header-title">{row.Label}</div>
                <div class="header-value">{row.DemoValue}</div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():

    with st.sidebar:

        st.markdown("<div class='sidebar'>", unsafe_allow_html=True)

        icons = ["🏠","📂","📊","🧾","📎","⚙"]

        for icon in icons:

            st.markdown(
                f"<div class='sidebar-icon'>{icon}</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)


def render_control(field):

    label = field["Label"]
    value = field["DemoValue"]
    ftype = field["FieldType"]
    key = field["FieldId"]

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

    elif ftype in ["Comments","LongText"]:
        return st.text_area(label, value=value, key=key)

    elif ftype == "Check":
        return st.checkbox(label, key=key)

    else:
        return st.text_input(label, value=value, key=key)


def render_detail_field(field):

    label = field.get("Label","")
    value = field.get("DemoValue","")

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

    render_sidebar()

    render_header(df)

    tabs = df["Tab"].dropna().unique().tolist()

    tab_objects = st.tabs(tabs)

    for i, tab in enumerate(tabs):

        with tab_objects[i]:

            tab_df = df[df["Tab"] == tab]

            sections = tab_df["Section"].dropna().unique().tolist()

            for section in sections:

                st.markdown(
                    f"<div class='section-title'>{section}</div>",
                    unsafe_allow_html=True
                )

                sec_df = tab_df[tab_df["Section"] == section]

                rows = sec_df["Row"].unique()

                for r in rows:

                    row_df = sec_df[sec_df["Row"] == r]

                    fields = row_df.to_dict("records")

                    fields = [
                        f for f in fields
                        if f["FieldId"] and str(f["FieldId"]).lower() != "blankcell"
                    ]

                    if not fields:
                        continue

                    total_span = sum(int(f.get("ColSpan",1)) for f in fields)

                    cols = st.columns(total_span)

                    col_index = 0

                    for field in fields:

                        span = int(field.get("ColSpan",1))

                        with cols[col_index]:

                            if page_type == "Detail Page":
                                render_detail_field(field)

                            else:
                                render_control(field)

                        col_index += span

                st.divider()
