import streamlit as st
import utils.components as cmp

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Contact Us | UnemployIQ",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS (UNEMPLOYIQ GREEN THEME)
# ============================================================

st.html("""
    <style>
        .st-key-infoCont, 
        .st-key-formCont, 
        .st-key-card1, 
        .st-key-card2, 
        .st-key-card3 {
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

        .contact-card-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #eef0f2;
            text-align: center;
            height: 100%;
        }

        .contact-action-btn {
            display: inline-block;
            background-color: #047857;
            color: white !important;
            padding: 8px 18px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            margin-top: 10px;
            transition: 0.3s;
        }

        .contact-action-btn:hover {
            background-color: #064e3b;
        }
    </style>
""")

# Standard UnemployIQ Header Component
cmp.header()

# ============================================================
# PAGE TITLE & HERO
# ============================================================

with st.container():
    col_left, col_right = st.columns([7, 3])
    with col_left:
        st.header("Contact & Support")
        st.caption("Have questions, feedback, or collaboration ideas about UnemployIQ? Reach out to us!")
    with col_right:
        st.write(" ")
        st.info("💬 Developer Response Time: Within 24 Hours")

st.write("")

# ============================================================
# DIRECT CONTACT CARDS
# ============================================================

st.markdown('<div class="section-header-banner">📬 Direct Contact Channels</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(key="card1"):
        st.markdown("""
        <div class="contact-card-box">
            <h2 style="margin:0;">📧</h2>
            <h4 style="color:#0f172a; margin-top:8px;">Email Us</h4>
            <p style="color:#64748b; font-size:14px;">Drop an email for project inquiries or feedback.</p>
            <p style="font-weight:bold; color:#047857;">aadeshupadhyay77@gmail.com</p>
            <a href="mailto:aadeshupadhyay77@gmail.com" class="contact-action-btn">Send Email</a>
        </div>
        """, unsafe_allow_html=True)

with c2:
    with st.container(key="card2"):
        st.markdown("""
        <div class="contact-card-box">
            <h2 style="margin:0;">📱</h2>
            <h4 style="color:#0f172a; margin-top:8px;">Call Directly</h4>
            <p style="color:#64748b; font-size:14px;">Available for quick calls and discussions.</p>
            <p style="font-weight:bold; color:#047857;">+91 9839403018</p>
            <a href="tel:+919839403018" class="contact-action-btn">Make a Call</a>
        </div>
        """, unsafe_allow_html=True)

with c3:
    with st.container(key="card3"):
        st.markdown("""
        <div class="contact-card-box">
            <h2 style="margin:0;">💬</h2>
            <h4 style="color:#0f172a; margin-top:8px;">WhatsApp</h4>
            <p style="color:#64748b; font-size:14px;">Connect instantly over WhatsApp chat.</p>
            <p style="font-weight:bold; color:#047857;">+91 9839403018</p>
            <a href="https://wa.me/919839403018" target="_blank" class="contact-action-btn">Chat on WhatsApp</a>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ============================================================
# INTERACTIVE MESSAGE FORM & DEVELOPER DETAILS
# ============================================================

st.markdown('<div class="section-header-banner">📝 Send Us a Message</div>', unsafe_allow_html=True)

col_form, col_info = st.columns([6, 4], gap="medium")

with col_form:
    with st.container(key="formCont"):
        st.subheader("Get In Touch")
        st.caption("Fill out the form below and we'll get back to you shortly.")

        with st.form(key="contact_form", clear_on_submit=True):
            user_name = st.text_input("Your Full Name", placeholder="e.g. John Doe")
            user_email = st.text_input("Your Email Address", placeholder="name@example.com")
            subject = st.selectbox(
                "Subject / Inquiries",
                ["General Feedback", "Bug Report", "Dataset Inquiry", "Project Collaboration", "Other"]
            )
            user_message = st.text_area("Your Message", placeholder="Type your message here...", height=130)

            submit_btn = st.form_submit_button("🚀 Send Message", use_container_width=True)

            if submit_btn:
                if user_name and user_email and user_message:
                    st.success(f"Thank you, {user_name}! Your message has been recorded successfully.")
                else:
                    st.error("Please fill in all the required fields before submitting.")

with col_info:
    with st.container(key="infoCont"):
        st.subheader("Developer Info")
        st.markdown("""
        **Developer:** Aadesh Upadhyay  
        **Role:** Data Science & Machine Learning Intern  
        **Project:** UnemployIQ Platform  
        **Location:** Uttar Pradesh, India  
        """)

        st.markdown("---")
        st.markdown("**Office Hours:**")
        st.markdown("🕒 Monday – Saturday: 9:00 AM – 7:00 PM (IST)")

st.write("")

cmp.footer()