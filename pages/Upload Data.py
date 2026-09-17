import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import utils.components as cmp

st.set_page_config(layout="wide", page_title="Upload Dataset")

st.html("""
    <style>
        [data-testid="stElementContainer"]:has(div[key="upload1"]) {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 2.5rem;
            border: 1px dashed #cfd8dc;
            text-align: center;
        }
        [data-testid="stElementContainer"]:has(div[key="upload1"]) img {
            width: 30px !important;
            height: 30px !important;
            object-fit: contain;
            margin: 0 auto;
        }
        .st-key-uploaderCont{
            background-color:white !important;
            border-radius:10px;
            padding:20px;
        }
        .st-key-upload1{
            background-color:#f8f9fa !important;
            border-radius:10px;
            padding:10px;
        }
        .st-key-metricsCont{
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
        .st-key-existingCont{
            background-color:white !important;
            border-radius:10px;
            padding:16px 20px;
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

with st.container():
    col_left, col_right = st.columns([7, 3])
    with col_left:
        st.header("Dataset Ingestion & Data Pipeline Manager")
        st.caption(
            "Upload Custom CSV, Excel datasets for automated cleaning, schema validation, missing values imputation, and pipeline execution.")
    with col_right:
        st.write(" ")
        st.write(" ")
        st.info(f"Dataset Validation {pd.Timestamp.now().date()}")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ---- Required schema for an unemployment dataset ----
# Each group is a set of keywords — the dataset needs at least one column
# matching each group to be considered a valid unemployment dataset.
REQUIRED_COLUMN_GROUPS = {
    "Unemployment Rate": ["unemploy"],
    "Region/State/Area": ["region", "state", "area", "district", "location"],
    "Date/Year/Period": ["year", "date", "period", "month"],
}


def find_matching_column(df, keywords):
    for col in df.columns:
        low = col.lower()
        if any(k in low for k in keywords):
            return col
    return None


def validate_unemployment_dataset(df):
    """Returns (is_valid, matched_columns_dict, missing_groups_list)."""
    matched = {}
    missing = []
    for group_name, keywords in REQUIRED_COLUMN_GROUPS.items():
        col = find_matching_column(df, keywords)
        if col:
            matched[group_name] = col
        else:
            missing.append(group_name)
    return len(missing) == 0, matched, missing


# ---- 2. Main styled upload card ----
with st.container(key="uploaderCont"):
    with st.container(key="upload1"):
        c1, c2, c3 = st.columns([3, 6, 3])
        with c2:
            st.image("images/upload.png", width=50)
            st.subheader('Drag & drop federal labor microdata or benchmark files')
            st.caption("Streamlit dynamic buffer reads raw bytes-streams straight into memory pipeline")
            upload = st.file_uploader("Browse Local files", type=["CSV", "xlsx"], label_visibility="collapsed")
            if upload:
                st.session_state.uploaded = upload
                st.session_state.df = None          # force re-read for the new file
                st.session_state.pop("saved_path", None)
                st.session_state.pop("validation", None)

# ---- 3. Pick up an already-saved dataset if nothing was just uploaded ----
existing_files = sorted(f for f in os.listdir(DATA_DIR) if f.lower().endswith((".csv", ".xlsx")))

if "uploaded" not in st.session_state and existing_files:
    with st.container(key="existingCont"):
        e1, e2, e3 = st.columns([6, 2, 2])
        with e1:
            st.markdown("**No new upload yet — load a previously saved dataset instead:**")
            choice = st.selectbox("Existing datasets", existing_files, label_visibility="collapsed")
        with e2:
            st.write("")
            st.write("")
            if st.button("📂 Load Selected", use_container_width=True):
                path = os.path.join(DATA_DIR, choice)
                st.session_state.df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
                st.session_state.saved_path = path
                st.session_state.pop("validation", None)
                st.rerun()
        with e3:
            st.write("")
            st.write("")
            if st.button("➡️ Proceed to EDA", use_container_width=True, key="proceed_existing"):
                path = os.path.join(DATA_DIR, choice)
                check_df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
                is_valid, _, missing = validate_unemployment_dataset(check_df)
                if is_valid:
                    st.session_state.df = check_df
                    st.session_state.saved_path = path
                    st.switch_page("pages/eda.py")
                else:
                    st.error(f"Cannot proceed — missing: {', '.join(missing)}")

# ---- 4. Run validation whenever a dataset is loaded ----
if "uploaded" in st.session_state and st.session_state.get("df") is None:
    f = st.session_state.uploaded
    st.session_state.df = pd.read_csv(f) if f.name.lower().endswith(".csv") else pd.read_excel(f)

df = st.session_state.get("df")

if df is not None and "validation" not in st.session_state:
    st.session_state.validation = validate_unemployment_dataset(df)

# ---- 5. Validation banner + Save / Proceed buttons ----
if "uploaded" in st.session_state:
    is_valid, matched, missing = st.session_state.validation

    if is_valid:
        st.success(
            f"✅ Valid unemployment dataset — detected columns: "
            + ", ".join(f"**{k}** → `{v}`" for k, v in matched.items())
        )
    else:
        st.error(
            f"❌ This doesn't look like a valid unemployment dataset. "
            f"Missing required field(s): {', '.join(missing)}. "
            f"Detected instead: {', '.join(matched.values()) if matched else 'none'}."
        )

    btn_col1, btn_col2, _ = st.columns([2, 2, 6])
    with btn_col1:
        if st.button("💾 Save Dataset", use_container_width=True, disabled=not is_valid):
            save_path = os.path.join(DATA_DIR, st.session_state.uploaded.name)
            with open(save_path, "wb") as f:
                f.write(st.session_state.uploaded.getbuffer())
            st.session_state.saved_path = save_path
            st.success(f"Saved to {save_path}")

    with btn_col2:
        if st.button("➡️ Proceed to EDA", use_container_width=True, disabled=not is_valid, key="proceed_upload"):
            if "saved_path" not in st.session_state:
                st.warning("Please save the dataset first.")
            else:
                st.switch_page("pages/EDA.py")

    st.divider()

# ---- 6. Metrics + Donut chart / Preview — only for a validated dataset ----
if df is not None and st.session_state.get("validation", (False,))[0]:
    with st.container(key="metricsCont"):
        m_col, chart_col = st.columns([6, 4])

        with m_col:
            st.subheader("Dataset Quality Snapshot")
            r1c1, r1c2, r1c3 = st.columns(3)
            r1c1.metric("Total Rows", f"{df.shape[0]:,}")
            r1c2.metric("Total Columns", df.shape[1])
            r1c3.metric("Null Values", f"{int(df.isnull().sum().sum()):,}")

            r2c1, r2c2, r2c3 = st.columns(3)
            r2c1.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
            r2c2.metric("Numeric Columns", df.select_dtypes(include="number").shape[1])
            r2c3.metric("Categorical Columns", df.select_dtypes(include="object").shape[1])

        with chart_col:
            st.subheader("Unemployment Rate")
            rate_col = st.session_state.validation[1].get("Unemployment Rate")

            if rate_col:
                avg_rate = df[rate_col].mean()
                employed_pct = 100 - avg_rate
                fig = go.Figure(data=[go.Pie(
                    labels=["Unemployed", "Employed"],
                    values=[avg_rate, employed_pct],
                    hole=0.65,
                    marker=dict(colors=["#ef4444", "#e5e7eb"]),
                    textinfo="none"
                )])
                fig.update_layout(
                    showlegend=True,
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=260,
                    annotations=[dict(text=f"{avg_rate:.1f}%", x=0.5, y=0.5, font_size=22, showarrow=False)]
                )
                st.plotly_chart(fig, use_container_width=True)

    st.write("")

    with st.container(key="previewCont"):
        st.subheader("Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)

elif df is None:
    # ---- 7. Empty state — nothing uploaded, nothing saved yet ----
    st.write("")
    with st.container(key="previewCont"):
        e_col1, e_col2, e_col3 = st.columns([1, 2, 1])
        with e_col2:
            st.markdown(
                "<div style='text-align:center; padding:2rem 0;'>"
                "<h4>No dataset loaded yet</h4>"
                "<p style='color:#6b7280;'>Upload a CSV/Excel file above, or load a previously saved one "
                "once you have one, to see quality metrics and a preview here.</p>"
                "</div>",
                unsafe_allow_html=True
            )
cmp.footer()