import streamlit as st
import pandas as pd
import numpy as np

#==============styling =======================================
def header():
    st.markdown("""
    <style>

    /* =====================================================
       REMOVE DEFAULT STREAMLIT TOP SPACE
       ===================================================== */

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
    }


    /* =====================================================
       STREAMLIT HEADER
       ===================================================== */

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0px;
    }


    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {
        background-color: #F5F7F2;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #173F35;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #173F35;
    }


    /* Sidebar text */

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }


    /* =====================================================
       SIDEBAR NAVIGATION
       ===================================================== */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }


    /* Navigation links */

    section[data-testid="stSidebar"] ul li a {
        border-radius: 8px;
        transition: 0.2s;
    }


    /* Navigation hover */

    section[data-testid="stSidebar"] ul li a:hover {
        background-color: #24594A;
        color: #FFFFFF !important;
    }


    /* Active navigation item */

    section[data-testid="stSidebar"] ul li a[aria-current="page"] {
        background-color: #2F6B58;
        color: #FFFFFF !important;
    }


    /* =====================================================
       CUSTOM HEADER
       ===================================================== */

    .custom-header {
        background-color: #2F6B58;
        padding: 20px 30px;
        margin: 0px 0px 25px 0px;
        border-radius: 0px 0px 12px 12px;
        box-shadow: 0px 3px 10px rgba(23, 63, 53, 0.15);
    }


    .custom-header h1 {
        color: #FFFFFF !important;
        margin: 0px;
        padding: 0px;
        font-size: 30px;
        font-weight: 700;
    }


    .custom-header p {
        color: #DCEDE6;
        margin: 5px 0px 0px 0px;
        font-size: 14px;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #DDE7E2;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 3px 10px rgba(23, 63, 53, 0.06);
    }


    div[data-testid="stMetricLabel"] {
        color: #60756D !important;
    }


    div[data-testid="stMetricValue"] {
        color: #1F2924 !important;
        font-weight: 700;
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {
        background-color: #3F8068;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        transition: 0.2s;
    }


    .stButton > button:hover {
        background-color: #7DD3FC;
        color: #FFFFFF;
        border: none;
    }


    /* =====================================================
       INPUT FIELDS
       ===================================================== */

    .stTextInput input,
    .stNumberInput input {
        border-radius: 8px;
        border: 1px solid #CBDDD5;
    }


    /* =====================================================
       SELECTBOX
       ===================================================== */

    div[data-baseweb="select"] {
        border-radius: 8px;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1,
    h2,
    h3 {
        color: #1F2924 !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: #DDE7E2;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }


    /* =====================================================
       INFO BOX
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    .streamlit-expanderHeader {
        background-color: #FFFFFF;
        border-radius: 8px;
    }
    .st-key-headerCustom{
       background-color:#173F35 !important;
       color:white !important;
    }
    .st-key-headerCustom h1{
       color:white !important;
    }

    /* =====================================================
       MOBILE HEADER RESPONSIVENESS (CENTER ALIGNED)
       ===================================================== */
    @media (max-width: 768px) {
        .st-key-header [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 12px !important;
        }
        .st-key-header [data-testid="column"] {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
        }
        .st-key-header [data-testid="column"] > div {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        .unemployiq-brand {
            justify-content: center !important;
        }
        .brand-shine {
            font-size: 22px !important;
        }
        .brand-dot {
            font-size: 20px !important;
        }
        div[data-testid="stCaptionContainer"] {
            text-align: center !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)
    with st.container(key="header", vertical_alignment="center"):
        # 3 equal sections
        left, center, right = st.columns(
            [2.4, 2.2, 0.8],
            gap="medium",
            vertical_alignment="center"
        )

        # -------------------------
        # LEFT — BRAND
        # -------------------------
        with left:
            brand_title, brand_caption = st.columns(
                [1.5, 2],
                gap="small",
                vertical_alignment="center"
            )

            # ✨ ANIMATED BRAND
            with brand_title:
                st.markdown(
                    """
                    <div class="unemployiq-brand">
                        <span class="brand-shine">UnemployIQ</span>
                        <span class="brand-dot">•</span>
                    </div>

                    <style>

                    .unemployiq-brand {
                        display: flex;
                        align-items: center;
                        gap: 6px;
                        height: 42px;
                        overflow: visible;
                    }

                    /* =========================
                       BRAND TEXT
                    ========================= */

                    .brand-shine {
                        font-size: 28px;
                        font-weight: 850;
                        letter-spacing: -1px;

                        /* Animated multi-color text */
                        background: linear-gradient(
                            110deg,
                            #0F172A 0%,
                            #334155 22%,
                            #16A34A 42%,
                            #06B6D4 52%,
                            #22C55E 62%,
                            #0F172A 82%
                        );

                        background-size: 300% 100%;

                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;

                        /* Text animation + separate colored glow */
                        animation:
                            brandShimmer 4s linear infinite,
                            brandFloat 3s ease-in-out infinite,
                            brandGlow 2.8s ease-in-out infinite;
                    }


                    /* =========================
                       SHIMMER
                    ========================= */

                    @keyframes brandShimmer {
                        0% {
                            background-position: 200% center;
                        }

                        100% {
                            background-position: -100% center;
                        }
                    }


                    /* =========================
                       FLOAT
                    ========================= */

                    @keyframes brandFloat {
                        0%, 100% {
                            transform: translateY(0px);
                        }

                        50% {
                            transform: translateY(-2px);
                        }
                    }


                    /* =========================
                       COLORED SHADOW / GLOW
                    ========================= */

                    @keyframes brandGlow {

                        0%, 100% {
                            filter:
                                drop-shadow(0 2px 3px rgba(15,23,42,0.18))
                                drop-shadow(0 0 0px rgba(34,197,94,0));
                        }

                        35% {
                            filter:
                                drop-shadow(0 3px 5px rgba(22,163,74,0.28))
                                drop-shadow(0 0 7px rgba(34,197,94,0.30));
                        }

                        70% {
                            filter:
                                drop-shadow(0 3px 6px rgba(6,182,212,0.28))
                                drop-shadow(0 0 9px rgba(6,182,212,0.25));
                        }
                    }


                    /* =========================
                       DOT
                    ========================= */

                    .brand-dot {
                        font-size: 25px;
                        font-weight: 900;

                        color: #22C55E;

                        text-shadow:
                            0 0 5px rgba(34,197,94,0.65),
                            0 0 12px rgba(6,182,212,0.35);

                        animation:
                            dotPulse 1.8s ease-in-out infinite,
                            dotColor 3s linear infinite;
                    }


                    @keyframes dotPulse {

                        0%, 100% {
                            opacity: 0.45;
                            transform: scale(0.8);
                        }

                        50% {
                            opacity: 1;
                            transform: scale(1.15);
                        }
                    }


                    @keyframes dotColor {

                        0%, 100% {
                            color: #22C55E;
                        }

                        50% {
                            color: #06B6D4;
                        }
                    }

                    </style>
                    """,
                    unsafe_allow_html=True
                )

            # Caption
            with brand_caption:
                st.write(" ")
                st.caption("Federal Analytics Core")
        # -------------------------
        # CENTER — ACTIONS
        # -------------------------
        with center:
            download_col, contact_col = st.columns(
                2,
                gap="small",
                vertical_alignment="center"
            )

            with download_col:
                st.write(" ")
                with open("data/Unemployment in India.csv", "rb") as sample:
                    st.download_button(
                        "Export Sample",
                        data=sample,
                        file_name="Unemployment_sample_dataset.csv",
                        type="secondary",
                        use_container_width=True,
                        key="btn1"
                    )

            with contact_col:
                st.write(" ")
                if st.button(
                        "Contact",
                        type="primary",
                        use_container_width=True,
                        key="btn2"
                ):
                    st.switch_page("pages/Contact.py")

        # -------------------------
        # RIGHT — VERSION + PROFILE
        # -------------------------
        with right:
            st.markdown(
                """
                <div style="
                    text-align:right;
                    height:50px;
                    width:50px;
                    border:0.5px solid grey;
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:24px;
                    background:white;
                    margin: 0 auto;
                ">
                    👤
                </div>
                """,
                unsafe_allow_html=True
            )
    st.html("""
    <hr style="
        width: 100%;
        border: none;
        border-top: 1px solid #D1D5DB;
        margin-top: 0px 0;

    ">
    """)

def footer():
    st.divider()

    with st.container(key="footer"):
        c1, c2, c3 = st.columns([2, 6, 2])
        with c2:
            st.text("📊 UnemployIQ | 💻 Built with Python & Streamlit | 💡 Turning Data into Insights",
                    text_alignment="center")