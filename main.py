import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Unemployment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

    /* =========================================
       REMOVE DEFAULT STREAMLIT TOP SPACE
       ========================================= */

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0px;
    }


    /* =========================================
       MAIN BACKGROUND
       ========================================= */

    .stApp {
        background-color: #F5F7FA;
    }


    /* =========================================
       SIDEBAR
       ========================================= */

    section[data-testid="stSidebar"] {
        background-color: #172554;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #172554;
    }


    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }


    /* =========================================
       CUSTOM HEADER
       ========================================= */

    .custom-header {

        background-color: #1E3A8A;

        padding: 18px 30px;

        margin: 0px 0px 25px 0px;

        border-radius: 0px 0px 12px 12px;

    }


    .custom-header h1 {

        color: white !important;

        margin: 0px;

        font-size: 30px;

        font-weight: 700;

    }


    .custom-header p {

        color: #DBEAFE;

        margin: 4px 0px 0px 0px;

        font-size: 14px;

    }


    /* =========================================
       METRIC CARDS
       ========================================= */

    div[data-testid="stMetric"] {

        background-color: #FFFFFF;

        padding: 20px;

        border-radius: 12px;

        border: 1px solid #E2E8F0;

        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.06);

    }


    div[data-testid="stMetricLabel"] {

        color: #64748B !important;

    }


    div[data-testid="stMetricValue"] {

        color: #0F172A !important;

        font-weight: 700;

    }


    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button {

        background-color: #2563EB;

        color: white;

        border: none;

        border-radius: 8px;

        padding: 8px 20px;

        font-weight: 600;

    }


    .stButton > button:hover {

        background-color: #1D4ED8;

        color: white;

    }


    /* =========================================
       HEADINGS
       ========================================= */

    h1, h2, h3 {

        color: #0F172A !important;

    }


    /* =========================================
       DIVIDER
       ========================================= */

    hr {

        border-color: #E2E8F0;

    }


</style>
""", unsafe_allow_html=True)


# =====================================================
# CUSTOM HEADER
# =====================================================

st.markdown("""
<div class="custom-header">

    <h1>📊 Unemployment Analysis</h1>

    <p>
        Explore unemployment trends, COVID-19 impact
        and regional patterns
    </p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# MULTIPAGE NAVIGATION
# =====================================================

