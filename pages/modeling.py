import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import utils.components as cmp

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Predictive Modeling | UnemployIQ",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS (UNEMPLOYIQ GREEN/DARK BANNER THEME)
# ============================================================

st.html(
    """
    <style>
        .st-key-configCont, 
        .st-key-metricsCont, 
        .st-key-chartCont, 
        .st-key-predictCont {
            background-color: white !important;
            border-radius: 10px;
            padding: 20px 25px;
            border: 1px solid #eef0f2;
        }

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

        div[data-testid="stMetric"] {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 12px;
            border: 1px solid #eef0f2;
        }
    </style>
"""
)

# Standard UnemployIQ Header Component
cmp.header()

# ============================================================
# DATA LOAD (FALLBACK SYSTEM)
# ============================================================

df = None
if "eda_df" in st.session_state and st.session_state.eda_df is not None:
    df = st.session_state.eda_df.copy()
elif "cleaned_df" in st.session_state and st.session_state.cleaned_df is not None:
    df = st.session_state.cleaned_df.copy()
elif os.path.exists("data/cleaned_dataset.csv"):
    df = pd.read_csv("data/cleaned_dataset.csv")

if df is None:
    st.warning("⚠️ No dataset found! Please load and clean the dataset first.")
    if st.button("⬅️ Go to Upload Data"):
        st.switch_page("pages/Upload Data.py")
    st.stop()


# Helper function to trim whitespaces in columns
def get_col(name_options):
    for option in name_options:
        for c in df.columns:
            if c.strip() == option.strip():
                return c
    return None


RATE_COL = get_col(
    [
        "Estimated Unemployment Rate (%)",
        "Unemployment Rate",
        "Estimated Unemployment Rate",
    ]
)
EMPLOYED_COL = get_col(["Estimated Employed", "Employed"])
PARTICIPATION_COL = get_col(
    [
        "Estimated Labour Participation Rate (%)",
        "Labour Participation Rate",
        "Labour Participation Rate (%)",
    ]
)
REGION_COL = get_col(["Region", "State"])
AREA_COL = get_col(["Area"])
DATE_COL = get_col(["Date"])

# Clean whitespace from column names if present
df.columns = df.columns.str.strip()
RATE_COL = "Estimated Unemployment Rate (%)" if RATE_COL else None
EMPLOYED_COL = "Estimated Employed" if EMPLOYED_COL else None
PARTICIPATION_COL = (
    "Estimated Labour Participation Rate (%)" if PARTICIPATION_COL else None
)
REGION_COL = "Region" if REGION_COL else None
AREA_COL = "Area" if AREA_COL else None
DATE_COL = "Date" if DATE_COL else None

# Clean NaN values for safety
df = df.dropna(subset=[RATE_COL] if RATE_COL else df.columns)

# ============================================================
# PAGE HEADER
# ============================================================

with st.container():
    col_l, col_r = st.columns([7, 3])
    with col_l:
        st.header("Predictive Modeling & Forecasting")
        st.caption(
            "Train machine learning regression models to predict unemployment rates."
        )
    with col_r:
        st.write(" ")
        st.info(f"Available Rows for Training: {df.shape[0]:,}")

st.write("")

# ============================================================
# 1. MODEL CONFIGURATION & PREPROCESSING
# ============================================================

st.markdown(
    '<div class="section-header-banner">⚙️ Model Configuration & Setup</div>',
    unsafe_allow_html=True,
)

with st.container(key="configCont"):
    m1, m2, m3 = st.columns(3)

    with m1:
        model_choice = st.selectbox(
            "Select Machine Learning Model",
            ["Random Forest Regressor", "Linear Regression"],
        )

    with m2:
        test_size = st.slider(
            "Test Dataset Split Size (%)",
            min_value=10,
            max_value=40,
            value=20,
            step=5,
        )

    with m3:
        random_state = st.number_input("Random State Seed", value=42, step=1)

    # Feature Engineering (One-Hot Encoding categorical features)
    feature_df = df.copy()

    # Process Date into Month & Year if exists
    if DATE_COL and DATE_COL in feature_df.columns:
        feature_df[DATE_COL] = pd.to_datetime(
            feature_df[DATE_COL].astype(str).str.strip(),
            errors="coerce",
            dayfirst=True,
        )
        feature_df["Month"] = feature_df[DATE_COL].dt.month
        feature_df["Year"] = feature_df[DATE_COL].dt.year
        feature_df = feature_df.drop(columns=[DATE_COL])

    # Convert Categorical variables (Region, Area, Frequency)
    cat_cols = feature_df.select_dtypes(include=["object"]).columns.tolist()
    encoded_df = pd.get_dummies(feature_df, columns=cat_cols, drop_first=True)

    X = encoded_df.drop(columns=[RATE_COL])
    y = encoded_df[RATE_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=(test_size / 100), random_state=random_state
    )

    train_btn = st.button("🚀 Train & Evaluate Model", use_container_width=True)

st.write("")

# ============================================================
# 2. MODEL TRAINING & EVALUATION METRICS
# ============================================================

if train_btn or "model_trained" in st.session_state:
    st.session_state.model_trained = True

    if model_choice == "Random Forest Regressor":
        model = RandomForestRegressor(
            n_estimators=100, random_state=random_state
        )
    else:
        model = LinearRegression()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metrics calculation
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    st.markdown(
        '<div class="section-header-banner">📊 Model Evaluation Metrics</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="metricsCont"):
        e1, e2, e3, e4 = st.columns(4)
        e1.metric("R² Score (Accuracy)", f"{r2:.3f}")
        e2.metric("Mean Absolute Error (MAE)", f"{mae:.2f}%")
        e3.metric("Root Mean Sq Error (RMSE)", f"{rmse:.2f}%")
        e4.metric("Test Data Points", f"{len(y_test):,}")

    st.write("")

    # Visualizing Actual vs Predicted
    st.markdown(
        '<div class="section-header-banner">📈 Prediction Performance Plots</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="chartCont"):
        ch1, ch2 = st.columns(2)

        with ch1:
            st.subheader("Actual vs Predicted Unemployment Rate")
            pred_df = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
            fig_scat = px.scatter(
                pred_df,
                x="Actual",
                y="Predicted",
                trendline="ols",
                color_discrete_sequence=["#047857"],
            )
            fig_scat.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_scat, use_container_width=True)

        with ch2:
            st.subheader("Residuals Distribution Error")
            residuals = y_test - y_pred
            fig_hist = px.histogram(
                residuals,
                nbins=25,
                color_discrete_sequence=["#ef4444"],
                labels={"value": "Error (Residual)"},
            )
            fig_hist.update_layout(
                height=350, margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    st.write("")

    # ============================================================
    # 3. INTERACTIVE PREDICTION FORM
    # ============================================================

    st.markdown(
        '<div class="section-header-banner">🔮 Interactive Rate Predictor</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="predictCont"):
        st.caption("Select custom input parameters to predict Unemployment Rate.")

        p1, p2, p3 = st.columns(3)

        with p1:
            input_employed = st.number_input(
                "Estimated Employed Workforce",
                value=float(
                    df[EMPLOYED_COL].mean() if EMPLOYED_COL else 10000000
                ),
            )

        with p2:
            input_part = st.number_input(
                "Labour Participation Rate (%)",
                value=float(
                    df[PARTICIPATION_COL].mean() if PARTICIPATION_COL else 40.0
                ),
            )

        with p3:
            if REGION_COL and REGION_COL in df.columns:
                input_region = st.selectbox(
                    "Select Region", sorted(df[REGION_COL].unique().tolist())
                )
            else:
                input_region = None

        if st.button("🎯 Predict Rate", use_container_width=True):
            # Create dummy vector matching training columns
            input_data = pd.DataFrame(0, index=[0], columns=X.columns)

            if EMPLOYED_COL in input_data.columns:
                input_data[EMPLOYED_COL] = input_employed
            if PARTICIPATION_COL in input_data.columns:
                input_data[PARTICIPATION_COL] = input_part

            # One hot column matching for Region
            reg_col_name = f"{REGION_COL}_{input_region}"
            if reg_col_name in input_data.columns:
                input_data[reg_col_name] = 1

            single_pred = model.predict(input_data)[0]

            st.success(
                f"### 🔮 Predicted Unemployment Rate: **{single_pred:.2f}%**"
            )

# ============================================================
# NAVIGATION CONTROLS
# ============================================================

st.write("")
col_a, col_b, _ = st.columns([2, 2, 6])
with col_a:
    if st.button("⬅️ Back to Visualization", use_container_width=True):
        st.switch_page("pages/visualization.py",width="stretch")
with col_b:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Dashboard.py",width="stretch")