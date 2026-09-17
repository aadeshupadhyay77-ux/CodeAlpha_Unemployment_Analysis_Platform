import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from streamlit_extras import metric_cards

#=====================Page Configuration=================================
st.set_page_config(page_title="Dashboard",layout="wide",initial_sidebar_state="expanded")

#=====================Header Section=====================================


st.set_page_config(
    page_title="Unemployment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    box-shadow:
        0px 3px 10px rgba(23, 63, 53, 0.15);

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

    box-shadow:
        0px 3px 10px rgba(23, 63, 53, 0.06);

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


</style>
""", unsafe_allow_html=True)
#=======================styling metric cards================================
st.markdown("""
<style>

/* =====================================================
   METRIC CARDS — BASE
   ===================================================== */

div[data-testid="stMetric"] {
    position: relative !important;
    background: #FFFFFF !important;

    border: 1px solid #DDE7E2 !important;
    border-bottom: 4px solid #2F6B58 !important;

    border-radius: 12px !important;

    padding: 20px !important;

    box-shadow: 0 3px 10px rgba(23, 63, 53, 0.06) !important;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-bottom-color 0.25s ease !important;
}


/* =====================================================
   HOVER EFFECT
   ===================================================== */

div[data-testid="stMetric"]:hover {

    transform: translateY(-7px) !important;

    box-shadow:
        0 12px 25px rgba(23, 63, 53, 0.16) !important;

}


/* =====================================================
   CARD 1 — BLUE
   ===================================================== */

div[data-testid="stHorizontalBlock"]
> div:nth-child(1)
div[data-testid="stMetric"] {

    border-bottom-color: #0EA5E9 !important;
}

div[data-testid="stHorizontalBlock"]
> div:nth-child(1)
div[data-testid="stMetric"]:hover {

    box-shadow:
        0 12px 25px rgba(14, 165, 233, 0.22) !important;
}


/* =====================================================
   CARD 2 — PURPLE
   ===================================================== */

div[data-testid="stHorizontalBlock"]
> div:nth-child(2)
div[data-testid="stMetric"] {

    border-bottom-color: #8B5CF6 !important;
}

div[data-testid="stHorizontalBlock"]
> div:nth-child(2)
div[data-testid="stMetric"]:hover {

    box-shadow:
        0 12px 25px rgba(139, 92, 246, 0.22) !important;
}


/* =====================================================
   CARD 3 — GREEN
   ===================================================== */

div[data-testid="stHorizontalBlock"]
> div:nth-child(3)
div[data-testid="stMetric"] {

    border-bottom-color: #22C55E !important;
}

div[data-testid="stHorizontalBlock"]
> div:nth-child(3)
div[data-testid="stMetric"]:hover {

    box-shadow:
        0 12px 25px rgba(34, 197, 94, 0.22) !important;
}


/* =====================================================
   CARD 4 — ORANGE
   ===================================================== */

div[data-testid="stHorizontalBlock"]
> div:nth-child(4)
div[data-testid="stMetric"] {

    border-bottom-color: #F59E0B !important;
}

div[data-testid="stHorizontalBlock"]
> div:nth-child(4)
div[data-testid="stMetric"]:hover {

    box-shadow:
        0 12px 25px rgba(245, 158, 11, 0.22) !important;
}


/* =====================================================
   SMOOTH METRIC CONTENT
   ===================================================== */

div[data-testid="stMetricLabel"] {
    transition: transform 0.25s ease !important;
}

div[data-testid="stMetricValue"] {
    transition: transform 0.25s ease !important;
}

div[data-testid="stMetric"]:hover
div[data-testid="stMetricValue"] {

    transform: translateY(-2px) !important;
}

</style>
""", unsafe_allow_html=True)
#===================buttons hover effect=====================================
st.markdown("""
<style>

/* ===== ALL BUTTONS BASE ===== */

.stButton > button {
    transition: all 0.25s ease !important;
}


/* ===== BTN 1 : EXPORT SAMPLE ===== */

div[data-testid="stButton"] button[kind="secondary"]:hover {
    background-color: orange !important;
    color: #075985 !important;
    border-color: #0EA5E9 !important;
    box-shadow: 0 0 15px rgba(14,165,233,0.35) !important;
}


/* ===== BTN 2 : CONTACT ===== */

div[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: #06B6D4 !important;
    color: white !important;
    border-color: #0891B2 !important;
    box-shadow: 0 0 15px rgba(6,182,212,0.40) !important;
}


/* ===== ANALYZE EVERYTHING ===== */

.st-key-btn3 button:hover {
    background-color: #BAE6FD !important;
    color: #075985 !important;
    border-color: #0EA5E9 !important;
    box-shadow: 0 0 18px rgba(14,165,233,0.35) !important;
}
.st-key-trendChart{
    background-color:white !important;
    padding:7px !important;
    border-radius:10px !important;
     box-shadow: 0 4px 12px rgba(217, 119, 6, 0.10) !important;

    transition: all 0.5s ease !important;
}
.st-key-trendChart:hover{
    background-color:white !important;
    padding:7px !important;
    transform: translateX(-7px) !important;

    
       box-shadow: 0 14px 28px rgba(22, 101, 52, 0.22) !important;

    border-color: #059669 !important;
     
    
}
.st-key-progressCont{
    background-color:white !important;
    padding:7px !important;
    border-radius:10px !important;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.10) !important;

    transition: all 0.5s ease !important;

}
.st-key-progressCont:hover{
    background-color:white !important;
    padding:7px !important;
    transform: translateX(7px) !important;

    box-shadow: 0 14px 28px rgba(124, 58, 237, 0.22) !important;

    border-color: #059669 !important;
     
    
}

.st-key-regionChart{
    background-color:white !important;
    padding:7px !important;
    border-radius:10px !important;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.10) !important;

    transition: all 0.5s ease !important;

}
.st-key-regionChart:hover{
    background-color:white !important;
    padding:7px !important;
    transform: translateY(-7px) !important;

    box-shadow:
        0 14px 28px rgba(5, 150, 105, 0.22) !important;

    border-color: #059669 !important;
    
    
}


/* =====================================================
   LAST 3 METRIC CARDS
   ===================================================== */

.st-key-regionMetric {
    background: #FFFFFF !important;
    border: 1px solid #D1FAE5 !important;
    border-left: 5px solid #059669 !important;
    border-radius: 14px !important;
    padding: 18px !important;

    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.10) !important;

    transition: all 0.25s ease !important;
}

.st-key-regionMetric:hover {
    transform: translateY(-7px) !important;

    box-shadow:
        0 14px 28px rgba(5, 150, 105, 0.22) !important;

    
}


/* ================= AVG EMPLOYED ================= */

.st-key-avgEmployeeMetric {
    background: #FFFFFF !important;
    border: 1px solid #FEF3C7 !important;
    border-left: 5px solid #D97706 !important;
    border-radius: 14px !important;
    padding: 18px !important;

    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.10) !important;

    transition: all 0.25s ease !important;
}

.st-key-avgEmployeeMetric:hover {
    transform: translateY(-7px) !important;

    box-shadow:
        0 14px 28px rgba(217, 119, 6, 0.22) !important;

    border-color: #D97706 !important;
}


/* ================= MAX EMPLOYED ================= */

.st-key-maxEmployeeMetric {
    background: #FFFFFF !important;
    border: 1px solid #EDE9FE !important;
    border-left: 5px solid #7C3AED !important;
    border-radius: 14px !important;
    padding: 18px !important;

    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.10) !important;

    transition: all 0.25s ease !important;
}

.st-key-maxEmployeeMetric:hover {
    transform: translateY(-7px) !important;

    box-shadow:
        0 14px 28px rgba(124, 58, 237, 0.22) !important;

    border-color: #7C3AED !important;
}


/* ================= CONTENT ================= */

.st-key-regionMetric [data-testid="stMetricLabel"],
.st-key-avgEmployeeMetric [data-testid="stMetricLabel"],
.st-key-maxEmployeeMetric [data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600 !important;
}

.st-key-regionMetric [data-testid="stMetricValue"],
.st-key-avgEmployeeMetric [data-testid="stMetricValue"],
.st-key-maxEmployeeMetric [data-testid="stMetricValue"] {
    color: #1F2924 !important;
    font-weight: 750 !important;
}
.st-key-f{
    background-color:#E6FFE6!important;
    border-radius:10px !important;
    color:black;
    font-weight:bold;
}
.st-key-w{
    background-color:#FFF5EE !important;
    border-radius:10px !important;
    color:black;
    font-weight:bold;
}
.st-key-featureCont{
    background-color:white !important;
    padding:10px !important;
    border-radius:10px !important;
}

</style>
""", unsafe_allow_html=True)




# =========================
# HEADER
# =========================
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
with st.container(key="description"):
    colLeft,colRight=st.columns([7,3],gap="medium")
    with colLeft:
        st.header("National Unemployment & Labor Force Executive Dashboard")
        st.caption("Real-time statistical indicators,demographic impact metrics and state wise volatility index.")
    with colRight:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        if st.button("Analyze Everything",width="stretch",type="secondary",key="btn3"):
            st.switch_page("pages/Upload Data.py")

#====================Last uploaded Dataset====================
dataset=pd.read_csv("data/Unemployment_Rate_upto_11_2020.csv")
st.info(f"✔ Last Updated : { pd.Timestamp.now().date()}")

#======================metric card===============================================
with st.container(key="metricContainer"):
    m1,m2,m3,m4=st.columns(4)
    m1.metric("Total Records",value=dataset.shape[0],width="stretch",border=True,height="stretch",chart_type="bar",chart_data=dataset[" Estimated Unemployment Rate (%)"])
    m2.metric("Total Columns",value=dataset.shape[1],width="stretch",border=True,height="stretch",chart_type="bar",chart_data=dataset[" Estimated Unemployment Rate (%)"])
    m3.metric("Avg Unemployment %",value=round(dataset[" Estimated Unemployment Rate (%)"].mean(),2),width="stretch",border=True,height="stretch",chart_type="line",chart_data=dataset[" Estimated Unemployment Rate (%)"])
    m4.metric("Max Unemployment %",value=dataset[" Estimated Unemployment Rate (%)"].max(),width="stretch",border=True,height="stretch",chart_type="area",chart_data=dataset[" Estimated Unemployment Rate (%)"])
#=====================Unemployment trend ========================================
with st.container(key="trendContainer"):
    col_left,col_right=st.columns([7,3])
    with col_left:
        with st.container(key="trendChart"):
            st.subheader("Yearly Unemployment Trend (2019-2024)")
            st.caption("National rate comparison with pre-pandemic steady line and cyclical stress test zone")
            fig, ax = plt.subplots()

            sb.lineplot(
                data=dataset,
                x=" Date",
                y=" Estimated Unemployment Rate (%)",
                marker="o",
                linewidth=2.5,
                color="#047857",  # Deep Emerald
                markerfacecolor="#D1FAE5",
                markeredgecolor="#047857",
                ax=ax
            )

            ax.set_title("5-Year Unemployment Trajectory", fontsize=14, fontweight="bold")
            ax.set_xlabel("")
            ax.set_ylabel("Unemployment Rate (%)")
            ax.grid(axis="y", alpha=0.2)
            plt.xticks(rotation=45, ha="right")

            plt.tight_layout()

            st.pyplot(fig, use_container_width=True)

with col_right:
        with st.container(key="progressCont"):
            st.subheader("Regional Employment filter")
            datasetcol=list(dataset["Region"].unique())
            regionSelect=st.selectbox("Select Region",options=datasetcol,width="stretch")
            searchbtn=st.button("Search By Region",type="primary",width="stretch")
            filterdata=dataset[dataset["Region"]==regionSelect]
            if searchbtn:
                st.dataframe(filterdata)
            else:
                st.table(dataset.head(4))
with st.container():
    c1,c2=st.columns([3,7])
    with c1:
        with st.container(key="valueCont"):
            st.metric("Total Regions",value=dataset["Region"].value_counts().sum(),height="stretch")
            st.metric("Average Estimated Employed", value=round(dataset[" Estimated Employed"].mean(),1),height="stretch")
            st.metric("Maximum Estimated Employed ", value=dataset[" Estimated Employed"].max(),height="stretch")
            st.metric("Minimum Estimated Employed ", value=dataset[" Estimated Employed"].min(),height="stretch")

    with c2:
        with st.container(key="RegionChart"):
            fig, ax = plt.subplots()

            sb.countplot(
                data=dataset,
                x="Region",
                color="#BE123C",

                ax=ax
            )

            ax.set_title(
                "Records by Region",
                fontsize=14,
                fontweight="bold",
                color="#064E3B"
            )

            ax.set_xlabel("")
            ax.set_ylabel("Number of Records")

            ax.grid(axis="y", alpha=0.2)

            plt.xticks(rotation=45, ha="right")

            plt.tight_layout()

            st.pyplot(fig, use_container_width=True)
            st.button("Summary and Distribution",type="secondary",width="stretch")

#==========================Features=================================================
with st.container(key="featureCont"):
    with st.expander(
        label="Features",
        expanded=True,
        key="f"
    ):
        st.success("""
        ### Key Features

1. **Interactive Dashboard** – Unemployment data ko visually explore karne ke liye interactive dashboard.

2. **KPI Metrics** – Total records, average unemployment rate, maximum unemployment rate aur employment statistics display karta hai.

3. **Unemployment Trend Analysis** – Time ke saath unemployment rate ke trends ko line charts ke through analyze karta hai.

4. **Region-wise Analysis** – Different regions/states ke unemployment records aur variations ko compare karta hai.

5. **COVID-19 Impact Analysis** – COVID-19 period ke during unemployment changes ko identify aur analyze karta hai.

6. **Interactive Region Filter** – User kisi specific region ko select karke uska data filter kar sakta hai.

7. **Statistical Visualization** – Seaborn aur Matplotlib ke through charts aur graphs provide karta hai.

8. **Data Cleaning & Processing** – Pandas aur NumPy ka use karke dataset ko clean aur process karta hai.

9. **Dataset Upload & Analysis** – User apna unemployment dataset upload karke analysis kar sakta hai.

10. **Data Export** – Sample dataset ko download/export karne ki facility.

11. **Responsive UI** – Streamlit-based clean, modern aur responsive dashboard interface.

12. **Data-driven Insights** – Unemployment patterns, regional variations aur employment indicators se meaningful insights generate karta hai.

        """)

    with st.expander(label="workflow",key="w"):
        st.error("""
        ### Working of the Project

1. **Dataset Collection** – Unemployment in India ka dataset collect kiya jata hai.

2. **Data Loading** – CSV dataset ko Pandas ke through Streamlit application mein load kiya jata hai.

3. **Data Cleaning** – Missing values, incorrect data types aur unnecessary data ko identify karke clean kiya jata hai.

4. **Data Processing** – NumPy aur Pandas ka use karke unemployment aur employment-related statistics calculate kiye jate hain.

5. **KPI Calculation** – Total records, average unemployment rate, maximum unemployment rate aur employment statistics calculate kiye jate hain.

6. **Trend Analysis** – Date-wise unemployment data ko analyze karke unemployment trends identify kiye jate hain.

7. **Regional Analysis** – Region-wise data filter aur analyze karke different regions ke unemployment patterns compare kiye jate hain.

8. **COVID-19 Analysis** – COVID-19 period ke data ko analyze karke unemployment rate mein changes observe kiye jate hain.

9. **Data Visualization** – Matplotlib aur Seaborn ka use karke line charts, bar charts aur other visualizations create kiye jate hain.

10. **Interactive Filtering** – User region select karke specific region ka data dynamically view kar sakta hai.

11. **Insights Generation** – Visualizations aur statistical results ke basis par important unemployment patterns aur observations identify kiye jate hain.

12. **Dashboard Presentation** – Final results ko Streamlit ke interactive dashboard par clear aur user-friendly format mein present kiya jata hai.

        """)

st.divider()

with st.container(key="footer"):
    c1,c2,c3=st.columns([2,6,2])
    with c2:
        st.text("📊 UnemployIQ | 💻 Built with Python & Streamlit | 💡 Turning Data into Insights",text_alignment="center")


