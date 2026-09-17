import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import utils.components as cmp

st.set_page_config(layout="wide", page_title="Exploratory Data Analysis")

st.html("""
    <style>
        .st-key-filterCont{
            background-color:white !important;
            border-radius:10px;
            padding:16px 20px;
            border: 1px solid #eef0f2;
        }
        .st-key-metricsCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-missingCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-trendCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-regionCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-mapCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-corrCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-previewCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
            border: 1px solid #eef0f2;
        }
        .st-key-cleanCont{
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

# ---- Guard: no dataset loaded ----
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("No dataset loaded yet. Please upload or select a dataset first.")
    if st.button("⬅️ Go to Upload Page"):
        st.switch_page("pages/Upload Data.py")
    st.stop()

df = st.session_state.df.copy()

# ---- Exact schema (same as upload page) ----
REGION_COL = "Region"
DATE_COL = " Date"
FREQUENCY_COL = "Frequency"
RATE_COL = " Estimated Unemployment Rate (%)"
EMPLOYED_COL = " Estimated Employed"
PARTICIPATION_COL = " Estimated Labour Participation Rate (%)"
LAT_COL = " latitude"
LON_COL = " longitude"

area_col = "Area" if "Area" in df.columns else ("Region.1" if "Region.1" in df.columns else None)
rate_col, region_col, date_col = RATE_COL, REGION_COL, DATE_COL

if date_col in df.columns:
    df[date_col] = pd.to_datetime(df[date_col].astype(str).str.strip(), errors="coerce", dayfirst=True)

with st.container():
    col_left, col_right = st.columns([7, 3])
    with col_left:
        st.header("Exploratory Data Analysis")
        st.caption("Inspect data quality, distributions, and unemployment trends before modeling.")
    with col_right:
        st.write(" ")
        st.write(" ")
        st.info(f"Records: {df.shape[0]:,}")

# ---- 1. Filters ----
with st.container(key="filterCont"):
    f1, f2, f3 = st.columns([3, 3, 3])
    filtered_df = df.copy()

    with f1:
        regions = ["All"] + sorted(df[region_col].dropna().unique().tolist())
        sel_region = st.selectbox("Filter by Region", regions)
        if sel_region != "All":
            filtered_df = filtered_df[filtered_df[region_col] == sel_region]

    with f2:
        if pd.api.types.is_datetime64_any_dtype(df[date_col]):
            min_d, max_d = df[date_col].min(), df[date_col].max()
            date_range = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
            if isinstance(date_range, tuple) and len(date_range) == 2:
                filtered_df = filtered_df[
                    (filtered_df[date_col] >= pd.to_datetime(date_range[0])) &
                    (filtered_df[date_col] <= pd.to_datetime(date_range[1]))
                    ]
        else:
            st.caption("Date column could not be parsed.")

    with f3:
        if FREQUENCY_COL in df.columns:
            freqs = ["All"] + sorted(df[FREQUENCY_COL].dropna().unique().tolist())
            sel_freq = st.selectbox("Frequency", freqs)
            if sel_freq != "All":
                filtered_df = filtered_df[filtered_df[FREQUENCY_COL] == sel_freq]

st.write("")

# ---- 2. Overview metrics ----
with st.container(key="metricsCont"):
    st.subheader("Dataset Overview")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Rows", f"{filtered_df.shape[0]:,}")
    m2.metric("Columns", filtered_df.shape[1])
    m3.metric("Missing Values", f"{int(filtered_df.isnull().sum().sum()):,}")
    m4.metric("Duplicate Rows", f"{int(filtered_df.duplicated().sum()):,}")
    m5.metric("Avg Unemployment Rate", f"{filtered_df[rate_col].mean():.2f}%")

    m6, m7 = st.columns(2)
    m6.metric("Avg Labour Participation Rate", f"{filtered_df[PARTICIPATION_COL].mean():.2f}%")
    m7.metric("Total Estimated Employed", f"{filtered_df[EMPLOYED_COL].sum():,.0f}")

st.write("")

# ---- 3. Missing values breakdown ----
with st.container(key="missingCont"):
    st.subheader("Missing Values by Column")
    null_counts = filtered_df.isnull().sum()
    null_counts = null_counts[null_counts > 0].sort_values(ascending=False)

    if null_counts.empty:
        st.success("No missing values in the current filtered view.")
    else:
        fig_null = go.Figure(go.Bar(
            x=null_counts.values,
            y=null_counts.index,
            orientation="h",
            marker_color="#ef4444"
        ))
        fig_null.update_layout(
            height=max(250, 30 * len(null_counts)),
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis_title="Missing Count",
            yaxis_title=""
        )
        st.plotly_chart(fig_null, use_container_width=True)

st.write("")

# ---- 4. Unemployment trend over time ----
if pd.api.types.is_datetime64_any_dtype(filtered_df[date_col]):
    with st.container(key="trendCont"):
        st.subheader("Unemployment Rate Trend")
        trend_df = filtered_df.groupby(date_col, as_index=False)[rate_col].mean().sort_values(date_col)
        fig_trend = px.line(trend_df, x=date_col, y=rate_col, markers=True)
        fig_trend.update_traces(line_color="#ef4444")
        fig_trend.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig_trend, use_container_width=True)
    st.write("")

# ---- 5. Region-wise comparison ----
with st.container(key="regionCont"):
    st.subheader("Average Unemployment Rate by Region")
    region_avg = (
        filtered_df.groupby(region_col, as_index=False)[rate_col]
        .mean()
        .sort_values(rate_col, ascending=False)
        .head(15)
    )
    fig_region = px.bar(region_avg, x=region_col, y=rate_col, color=rate_col,
                        color_continuous_scale=["#fde68a", "#ef4444"])
    fig_region.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=340, coloraxis_showscale=False)
    st.plotly_chart(fig_region, use_container_width=True)

st.write("")

# ---- 6. Geographic map of unemployment rate ----
if LAT_COL in filtered_df.columns and LON_COL in filtered_df.columns:
    with st.container(key="mapCont"):
        st.subheader("Unemployment Rate by Location")
        geo_df = (
            filtered_df.groupby([region_col, LAT_COL, LON_COL], as_index=False)[rate_col]
            .mean()
        )
        fig_map = px.scatter_mapbox(
            geo_df, lat=LAT_COL, lon=LON_COL, size=rate_col, color=rate_col,
            hover_name=region_col, color_continuous_scale="Reds", zoom=3,
            mapbox_style="carto-positron", size_max=30
        )
        fig_map.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig_map, use_container_width=True)
    st.write("")

# ---- 7. Correlation heatmap ----
numeric_df = filtered_df.select_dtypes(include="number")
if numeric_df.shape[1] >= 2:
    with st.container(key="corrCont"):
        st.subheader("Correlation Between Numeric Features")
        corr = numeric_df.corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
        fig_corr.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
    st.write("")

# ---- 8. Filtered data preview + download ----
with st.container(key="previewCont"):
    p1, p2 = st.columns([8, 2])
    with p1:
        st.subheader("Filtered Data Preview")
    with p2:
        st.write("")
        st.download_button(
            "⬇️ Download CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="filtered_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )
    st.dataframe(filtered_df.head(50), use_container_width=True)

st.write("")

# ---- 9. Data Cleaning Section ----
with st.container(key="cleanCont"):
    st.subheader("Data Cleaning & Preprocessing")
    st.caption("Clean missing values, drop duplicates, and export the processed dataset.")

    c1, c2, c3 = st.columns(3)
    with c1:
        drop_dups = st.checkbox("Remove Duplicate Rows", value=True)
    with c2:
        missing_strategy = st.selectbox("Missing Value Strategy",
                                        ["Keep As Is", "Drop Rows with Missing Values", "Fill Numerical with Mean"])
    with c3:
        strip_whitespace = st.checkbox("Strip Column Names Whitespace", value=True)

    if st.button("🧹 Clean & Save Dataset", use_container_width=True):
        cleaned_df = filtered_df.copy()

        if strip_whitespace:
            cleaned_df.columns = cleaned_df.columns.str.strip()

        if drop_dups:
            cleaned_df = cleaned_df.drop_duplicates()

        if missing_strategy == "Drop Rows with Missing Values":
            cleaned_df = cleaned_df.dropna()
        elif missing_strategy == "Fill Numerical with Mean":
            num_cols = cleaned_df.select_dtypes(include="number").columns
            cleaned_df[num_cols] = cleaned_df[num_cols].fillna(cleaned_df[num_cols].mean())

        st.session_state.cleaned_df = cleaned_df

        # Save dataset to local 'data' folder
        os.makedirs("data", exist_ok=True)
        cleaned_path = os.path.join("data", "cleaned_dataset.csv")
        cleaned_df.to_csv(cleaned_path, index=False)
        st.success(f"Successfully cleaned dataset ({cleaned_df.shape[0]} rows) and saved to `{cleaned_path}`!")

st.write("")

# ---- 10. Proceed to next stage ----
col_a, col_b, col_c, _ = st.columns([2, 2, 2, 4])
with col_a:
    if st.button("⬅️ Back to Upload", use_container_width=True):
        st.switch_page("pages/Upload Data.py")
with col_b:
    if st.button("📊 Go to Visualization", use_container_width=True):
        st.session_state.viz_df = st.session_state.get("cleaned_df", filtered_df)
        st.switch_page("pages/visualization.py")
with col_c:
    if st.button("➡️ Proceed to Modeling", use_container_width=True):
        st.session_state.eda_df = st.session_state.get("cleaned_df", filtered_df)
        st.switch_page("pages/modeling.py")

cmp.footer()