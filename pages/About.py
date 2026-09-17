import os
import streamlit as st
from streamlit_carousel import carousel
import utils.components as cmp

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="About Developer | UnemployIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS (GREEN BANNER & UNEMPLOYIQ THEME)
# ============================================================

st.html("""
    <style>
        .st-key-aboutCont, 
        .st-key-objectiveCont, 
        .st-key-visionCont, 
        .st-key-devCont, 
        .st-key-contactCont {
            background-color: white !important;
            border-radius: 10px;
            padding: 20px 25px;
            border: 1px solid #eef0f2;
        }

        /* Green Background Section Header Banner */
        .section-header-banner {
            background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
            border-left: #10b981 6px solid;
            color: #ffffff;
            font-size: 20px;
            font-weight: 700;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
        }

        .badge-tag {
            background-color: #f8f9fa;
            color: #1f2937;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.88rem;
            margin: 4px;
            display: inline-block;
            border: 1px solid #e2e8f0;
            font-weight: 500;
        }

        .contact-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 16px;
            border: 1px solid #eef0f2;
            text-align: center;
        }
    </style>
""")

# Standard UnemployIQ Header Component
cmp.header()

# ============================================================
# PAGE TITLE / HERO BANNER
# ============================================================

with st.container():
    col_left, col_right = st.columns([7, 3])
    with col_left:
        st.header("About UnemployIQ")
        st.caption(
            "Empowering economic insights through data analytics, exploratory visualization, and predictive modeling.")
    with col_right:
        st.write(" ")
        st.info("💡 Project Stage: EDA & Predictive Analytics")

st.write("")

# ============================================================
# ABOUT UNEMPLOYIQ SECTION (WITH UNSPLASH CAROUSEL)
# ============================================================

st.markdown('<div class="section-header-banner">📊 About The Platform</div>', unsafe_allow_html=True)

with st.container(key="aboutCont"):
    col_car, col_txt = st.columns([5, 5], gap="medium")

    with col_car:
        # Unsplash images relevant to Data Analytics, Jobs & Economy
        slides = [
            {
                "title": "Data Analytics",
                "text": "Inspecting economic distributions and workforce trends.",
                "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=800&fit=crop"
            },
            {
                "title": "Employment Metrics",
                "text": "Tracking labor participation and employment rates.",
                "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=800&fit=crop"
            },
            {
                "title": "Predictive Forecasting",
                "text": "Building ML models to forecast future labor trends.",
                "img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&h=800&fit=crop"
            }
        ]

        carousel(items=slides, key="unemployiq_carousel")

    with col_txt:
        st.markdown("""
        **UnemployIQ** is an advanced data-driven platform built to inspect, clean, visualize, and forecast unemployment trends across various regions and demographics.

        By transforming raw labor statistics into interactive dashboards, **UnemployIQ** simplifies complex economic indicators—such as **Estimated Unemployment Rate (%)**, **Labour Participation Rate (%)**, and **Estimated Employed workforce**.

        It helps analysts, researchers, and decision-makers uncover underlying employment patterns quickly and make informed data-driven decisions.
        """)

st.write("")

# ============================================================
# OBJECTIVE & VISION
# ============================================================

col_obj, col_vis = st.columns(2)

with col_obj:
    st.markdown('<div class="section-header-banner">🎯 Our Objective</div>', unsafe_allow_html=True)
    with st.container(key="objectiveCont"):
        st.markdown("""
        * Provide an end-to-end workspace from **Data Ingestion** to **Preprocessing** and **Predictive Modeling**.
        * Enable intuitive region-wise and time-series exploration of labor statistics.
        * Help analysts and researchers uncover underlying employment patterns quickly.
        """)

with col_vis:
    st.markdown('<div class="section-header-banner">🚀 Our Vision</div>', unsafe_allow_html=True)
    with st.container(key="visionCont"):
        st.markdown("""
        To bridge the gap between complex economic datasets and actionable insights through interactive visualizations, machine learning workflows, and streamlined dataset pipelines.
        """)

st.write("")

# ============================================================
# DEVELOPER SECTION
# ============================================================

st.markdown('<div class="section-header-banner">👨‍💻 About the Developer</div>', unsafe_allow_html=True)

with st.container(key="devCont"):
    dev_col1, dev_col2 = st.columns([3, 7], gap="medium")

    with dev_col1:
        img_path = "images/aadesh_photo.png"
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.info("Image file `images/aadu.jpeg` not found.")

    with dev_col2:
        st.subheader("Aadesh Upadhyay")
        st.caption("B.Tech ECE Student | Data Science & ML Intern")

        st.markdown("""
        Hi, I'm **Aadesh Upadhyay**. I am passionate about transforming raw economic and structural data into meaningful insights using Python, Streamlit, Pandas, Scikit-learn, and interactive charting libraries.

        Currently gaining hands-on experience as a **Data Science Intern at Code Alpha**, focusing on building real-world machine learning applications and analytical dashboards like **UnemployIQ**.
        """)

        st.write("")
        st.markdown("**Areas of Expertise:**")
        st.markdown("""
        <span class="badge-tag">📊 Exploratory Data Analysis</span>
        <span class="badge-tag">🧹 Data Cleaning & Preprocessing</span>
        <span class="badge-tag">📈 Time-Series Visualizations</span>
        <span class="badge-tag">🤖 Machine Learning</span>
        <span class="badge-tag">🐍 Python Development</span>
        """, unsafe_allow_html=True)

st.write("")

# ============================================================
# CONTACT SECTION (EMAIL & PHONE ONLY)
# ============================================================

st.markdown('<div class="section-header-banner">📞 Contact Information</div>', unsafe_allow_html=True)

with st.container(key="contactCont"):
    c1, c2 = st.columns(2)

    with c1:
        with st.container():
            st.markdown("""
            <div class="contact-box">
                <h4>📧 Email</h4>
                <p><a href="mailto:aadeshupadhyay77@gmail.com" style="color:#047857; font-weight:bold; text-decoration:none;">aadeshupadhyay77@gmail.com</a></p>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        with st.container():
            st.markdown("""
            <div class="contact-box">
                <h4>📱 Phone</h4>
                <p><a href="tel:+919839403018" style="color:#047857; font-weight:bold; text-decoration:none;">+91 9839403018</a></p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

cmp.footer()