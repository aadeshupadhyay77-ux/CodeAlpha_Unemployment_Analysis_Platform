import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import utils.components as cmp

st.set_page_config(layout="wide", page_title="Data Visualization")

# ---- Styles matching existing theme ----
st.html("""
    <style>
        .st-key-filterCont{
            background-color:white !important;
            border-radius:10px;
            padding:16px 20px;
            border: 1px solid #eef0f2;
        }
        .st-key-kpiCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-chartCont1{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-chartCont2{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-chartCont3{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        div[data-testid="stMetric"]{
            background-color:#f8f9fa;
            border-radius:10px;
            padding:12px;
            border:1px solid #eef0f2;
        }
    </style>
""")

cmp.header()

# ---- Load Dataset (from state or saved cleaned CSV) ----
df = None
if "viz_df" in st.session_state and st.session_state.viz_df is not None:
    df = st.session_state.viz_df.copy()
elif "cleaned_df" in st.session_state and st.session_state.cleaned_df is not None:
    df = st.session_state.cleaned_df.copy()
elif os.path.exists("data/cleaned_dataset.csv"):
    df = pd.read_csv("data/cleaned_dataset.csv")

if df is None:
    st.warning("No cleaned dataset found. Please run EDA and data cleaning first.")
    col_a, _ = st.columns([2, 8])
    with col_a:
        if st.button("⬅️ Go to EDA Page", use_container_width=True):
            st.switch_page("pages/EDA.py")
    st.stop()


# ---- Helper for flexible column naming (whitespace stripped or unstripped) ----
def find_col(possible_names):
    for name in possible_names:
        for col in df.columns:
            if col.strip() == name.strip():
                return col
    return None


REGION_COL = find_col(["Region", "Region.1", "Area"])
DATE_COL = find_col(["Date", " Date"])
RATE_COL = find_col(["Estimated Unemployment Rate (%)", " Estimated Unemployment Rate (%)", "Unemployment Rate"])
EMPLOYED_COL = find_col(["Estimated Employed", " Estimated Employed", "Employed"])
PARTICIPATION_COL = find_col(["Estimated Labour Participation Rate (%)", " Estimated Labour Participation Rate (%)",
                              "Labour Participation Rate"])
AREA_COL = find_col(["Area", "Region.1"])
LAT_COL = find_col(["latitude", " latitude"])
LON_COL = find_col(["longitude", " longitude"])

# Format date column if present
if DATE_COL and DATE_COL in df.columns:
    df[DATE_COL] = pd.to_datetime(df[DATE_COL].astype(str).str.strip(), errors="coerce", dayfirst=True)

# ---- Page Header ----
with st.container():
    col_l, col_r = st.columns([7, 3])
    with col_l:
        st.header("Interactive Data Visualization")
        st.caption("Deep-dive visual analytics generated from your cleaned dataset.")
    with col_r:
        st.write(" ")
        st.write(" ")
        st.info(f"Cleaned Records: {df.shape[0]:,} | Features: {df.shape[1]}")

# ---- 1. Filters Section ----
with st.container(key="filterCont"):
    f1, f2, f3 = st.columns(3)
    filtered_df = df.copy()

    with f1:
        if REGION_COL:
            regions = ["All"] + sorted(filtered_df[REGION_COL].dropna().astype(str).unique().tolist())
            sel_region = st.selectbox("Select Region", regions)
            if sel_region != "All":
                filtered_df = filtered_df[filtered_df[REGION_COL] == sel_region]

    with f2:
        if AREA_COL and AREA_COL in filtered_df.columns:
            areas = ["All"] + sorted(filtered_df[AREA_COL].dropna().astype(str).unique().tolist())
            sel_area = st.selectbox("Select Area Type", areas)
            if sel_area != "All":
                filtered_df = filtered_df[filtered_df[AREA_COL] == sel_area]

    with f3:
        if DATE_COL and pd.api.types.is_datetime64_any_dtype(filtered_df[DATE_COL]):
            min_d, max_d = filtered_df[DATE_COL].min(), filtered_df[DATE_COL].max()
            if pd.notnull(min_d) and pd.notnull(max_d):
                date_range = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
                if isinstance(date_range, tuple) and len(date_range) == 2:
                    filtered_df = filtered_df[
                        (filtered_df[DATE_COL] >= pd.to_datetime(date_range[0])) &
                        (filtered_df[DATE_COL] <= pd.to_datetime(date_range[1]))
                        ]

st.write("")

# ---- 2. Executive KPI Summary Cards ----
with st.container(key="kpiCont"):
    st.subheader("Key Performance Highlights")
    k1, k2, k3, k4 = st.columns(4)

    avg_rate = filtered_df[RATE_COL].mean() if RATE_COL and RATE_COL in filtered_df else 0
    avg_part = filtered_df[PARTICIPATION_COL].mean() if PARTICIPATION_COL and PARTICIPATION_COL in filtered_df else 0
    total_emp = filtered_df[EMPLOYED_COL].sum() if EMPLOYED_COL and EMPLOYED_COL in filtered_df else 0
    max_rate = filtered_df[RATE_COL].max() if RATE_COL and RATE_COL in filtered_df else 0

    k1.metric("Avg Unemployment Rate", f"{avg_rate:.2f}%")
    k2.metric("Peak Unemployment Rate", f"{max_rate:.2f}%")
    k3.metric("Avg Labour Participation Rate", f"{avg_part:.2f}%")
    k4.metric("Total Employed (Sum)", f"{total_emp:,.0f}")

st.write("")

# ---- 3. Row 1: Time Series & Distributions ----
with st.container(key="chartCont1"):
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Unemployment Rate Dynamics")
        if DATE_COL and RATE_COL and pd.api.types.is_datetime64_any_dtype(filtered_df[DATE_COL]):
            # Dynamic grouping by date & region/area
            color_var = REGION_COL if REGION_COL and sel_region == "All" else AREA_COL

            if color_var and color_var in filtered_df.columns:
                ts_df = filtered_df.groupby([DATE_COL, color_var], as_index=False)[RATE_COL].mean()
                fig_ts = px.line(ts_df, x=DATE_COL, y=RATE_COL, color=color_var,
                                 labels={RATE_COL: "Unemployment Rate (%)"},
                                 color_discrete_sequence=px.colors.qualitative.Set2)
            else:
                ts_df = filtered_df.groupby(DATE_COL, as_index=False)[RATE_COL].mean()
                fig_ts = px.line(ts_df, x=DATE_COL, y=RATE_COL, markers=True)
                fig_ts.update_traces(line_color="#ef4444")

            fig_ts.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350)
            st.plotly_chart(fig_ts, use_container_width=True)
        else:
            st.info("Time series visualization requires a valid date column.")

    with c2:
        st.subheader("Distribution of Unemployment Rates")
        if RATE_COL and RATE_COL in filtered_df:
            fig_dist = px.histogram(filtered_df, x=RATE_COL, nbins=30, marginal="box",
                                    color_discrete_sequence=["#ef4444"],
                                    labels={RATE_COL: "Unemployment Rate (%)"})
            fig_dist.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350, yaxis_title="Count")
            st.plotly_chart(fig_dist, use_container_width=True)

st.write("")

# ---- 4. Row 2: Regional Rankings & Urban vs Rural Analysis ----
with st.container(key="chartCont2"):
    c3, c4 = st.columns([6, 4])

    with c3:
        st.subheader("Top Regions by Unemployment Rate")
        if REGION_COL and RATE_COL:
            top_regions = (
                filtered_df.groupby(REGION_COL, as_index=False)[RATE_COL]
                .mean()
                .sort_values(RATE_COL, ascending=True)
                .tail(12)
            )
            fig_bar = px.bar(top_regions, x=RATE_COL, y=REGION_COL, orientation="h",
                             color=RATE_COL, color_continuous_scale="Reds",
                             labels={RATE_COL: "Avg Rate (%)", REGION_COL: ""})
            fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=360, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    with c4:
        st.subheader("Urban vs. Rural Comparison")
        if AREA_COL and RATE_COL and AREA_COL in filtered_df.columns:
            area_summary = filtered_df.groupby(AREA_COL, as_index=False)[RATE_COL].mean()
            fig_pie = px.pie(area_summary, names=AREA_COL, values=RATE_COL, hole=0.4,
                             color_discrete_sequence=["#3b82f6", "#ef4444"])
            fig_pie.update_traces(textinfo="percent+label")
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=360)
            st.plotly_chart(fig_pie, use_container_width=True)
        elif PARTICIPATION_COL and RATE_COL:
            # Fallback scatter plot if Area column is absent
            fig_scat = px.scatter(filtered_df, x=PARTICIPATION_COL, y=RATE_COL,
                                  color=RATE_COL, color_continuous_scale="Reds",
                                  labels={PARTICIPATION_COL: "Labour Participation (%)",
                                          RATE_COL: "Unemployment Rate (%)"})
            fig_scat.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=360)
            st.plotly_chart(fig_scat, use_container_width=True)

st.write("")

# ---- 5. Row 3: Multidimensional Scatter & Geographic Visuals ----
with st.container(key="chartCont3"):
    if EMPLOYED_COL and PARTICIPATION_COL and RATE_COL:
        st.subheader("Employment vs. Labour Participation Relationship")
        scatter_color = REGION_COL if REGION_COL in filtered_df.columns else RATE_COL
        fig_scatter = px.scatter(
            filtered_df,
            x=PARTICIPATION_COL,
            y=RATE_COL,
            size=EMPLOYED_COL,
            color=scatter_color,
            hover_name=REGION_COL if REGION_COL in filtered_df else None,
            size_max=35,
            labels={PARTICIPATION_COL: "Labour Participation Rate (%)", RATE_COL: "Unemployment Rate (%)"}
        )
        fig_scatter.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

st.write("")

# ---- 6. Navigation Controls ----
col_a, col_b, col_c= st.columns(3)
with col_a:
    if st.button("⬅️ Back to EDA", width="stretch"):
        st.switch_page("pages/EDA.py")
with col_b:
    if st.button("⬅️ Back to Upload", width="stretch"):
        st.switch_page("pages/Upload Data.py")
with col_c:
    if st.button("➡️ Proceed to Modeling", width="stretch"):
        st.session_state.eda_df = filtered_df
        st.switch_page("pages/modeling.py")

cmp.footer()