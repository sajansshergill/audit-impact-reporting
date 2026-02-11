from __future__ import annotations

import io
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data_clean" / "master_dataset.csv"

# Design system: teal accent, warm neutrals, Plus Jakarta Sans
PAGE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    :root {
        --accent: #0d9488;
        --accent-light: #ccfbf1;
        --bg: #fafaf9;
        --card: #ffffff;
        --text: #1c1917;
        --text-muted: #57534e;
        --border: #e7e5e4;
        --sidebar: #1c1917;
        --sidebar-text: #fafaf9;
        --radius: 12px;
        --shadow: 0 1px 3px rgba(0,0,0,0.06);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
    }
    
    .stApp {
        background: var(--bg) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }
    
    .block-container {
        padding: 2rem 2.5rem 3rem !important;
        max-width: 1320px !important;
    }
    
    /* Hero header */
    .dashboard-header {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--border);
    }
    .dashboard-header h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.85rem !important;
        color: var(--text) !important;
        letter-spacing: -0.03em !important;
        margin: 0 !important;
    }
    .dashboard-header .tagline {
        font-size: 0.95rem;
        color: var(--text-muted);
        margin-top: 0.35rem;
    }
    .dashboard-header .accent-bar {
        width: 48px;
        height: 4px;
        background: var(--accent);
        border-radius: 2px;
        margin-top: 0.5rem;
    }
    
    /* Metrics: card style with accent */
    div[data-testid="stMetric"] {
        background: var(--card) !important;
        padding: 1.25rem 1.5rem !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        border-left: 4px solid var(--accent) !important;
        box-shadow: var(--shadow) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    
    /* Tabs: pill style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: var(--card);
        padding: 6px;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.6rem 1.25rem;
        border-radius: 8px;
        font-weight: 500;
        color: var(--text-muted);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent) !important;
        color: white !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--sidebar) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #a8a29e !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        color: var(--sidebar-text) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background: #292524 !important;
        color: #fafaf9 !important;
        border-radius: 6px;
    }
    [data-testid="stSidebar"] hr {
        border-color: #292524 !important;
    }
    [data-testid="stSidebar"] .stCaption {
        color: #78716c !important;
    }
    
    /* Subheaders */
    h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        margin-top: 1.25rem !important;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: var(--radius);
        overflow: hidden;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    /* Buttons */
    .stDownloadButton button {
        background: var(--accent) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stDownloadButton button:hover {
        background: #0f766e !important;
        color: white !important;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        background: var(--card);
    }
    
    /* Info / tip: soft style */
    [data-testid="stAlert"] div[data-baseweb="notification"] {
        background: var(--accent-light) !important;
        border: 1px solid #99f6e4 !important;
        color: #134e4a !important;
        border-radius: var(--radius);
    }
    
    /* Errors */
    [data-testid="stException"], [data-testid="stAlert"]:has([data-baseweb="notification"][kind="error"]) {
        border-radius: var(--radius);
    }
    
    hr {
        margin: 1.5rem 0 !important;
        border-color: var(--border) !important;
    }
</style>
"""


def pct(x: float) -> str:
    if pd.isna(x):
        return "—"
    return f"{x * 100:.1f}%"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for c in ["first_session", "last_session", "last_survey"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ["sessions_total", "sessions_attended", "attendance_rate", "avg_satisfaction", "avg_nps", "pre_score", "post_score", "outcome_delta"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "city" in df.columns:
        df["city"] = df["city"].fillna("Unknown").astype(str).str.strip()
        df.loc[df["city"] == "", "city"] = "Unknown"
    return df


def safe_mean(series: pd.Series) -> float:
    series = pd.to_numeric(series, errors="coerce")
    return float(series.dropna().mean()) if series.dropna().shape[0] else np.nan


def make_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str,
    sort_asc: bool = False,
    top_n: int | None = 20,
) -> alt.Chart:
    df = data.sort_values(y, ascending=sort_asc)
    if top_n:
        df = df.head(top_n)
    return (
        alt.Chart(df, title=title)
        .mark_bar(size=24)
        .encode(
            x=alt.X(x, sort=None, title="", axis=alt.Axis(labelFont="Plus Jakarta Sans")),
            y=alt.Y(y, title="", axis=alt.Axis(labelFont="Plus Jakarta Sans")),
            tooltip=[x, y],
            color=alt.value(color),
        )
        .interactive()
        .properties(height=300)
        .configure_axis(labelFontSize=11, titleFontSize=12)
        .configure_view(strokeWidth=0)
    )


def main():
    st.set_page_config(
        page_title="Impact Dashboard | Nonprofit Reporting",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    # Header
    st.markdown(
        '<div class="dashboard-header">'
        '<h1>Impact Dashboard</h1>'
        '<p class="tagline">Program performance from standardized ETL data</p>'
        '<div class="accent-bar"></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not DATA_PATH.exists():
        st.error(
            "**Missing data.** Run the ETL first: `python etl_pipeline.py`"
        )
        st.stop()

    df = load_data(DATA_PATH)

    # ----- Sidebar -----
    st.sidebar.header("Filters")
    cities = sorted(df["city"].dropna().unique().tolist()) if "city" in df.columns else []
    programs = sorted(df["program_id"].dropna().unique().tolist()) if "program_id" in df.columns else []
    city_sel = st.sidebar.multiselect("City", options=cities, default=cities, placeholder="All")
    if not city_sel:
        city_sel = cities
    program_sel = st.sidebar.multiselect("Program", options=programs, default=programs, placeholder="All")
    if not program_sel:
        program_sel = programs

    min_date = df["first_session"].min() if "first_session" in df.columns else pd.NaT
    max_date = df["last_session"].max() if "last_session" in df.columns else pd.NaT
    use_dates = pd.notna(min_date) and pd.notna(max_date)
    if use_dates:
        try:
            min_d, max_d = min_date.date(), max_date.date()
            date_range = st.sidebar.date_input("Session date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
            if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            else:
                d = date_range if hasattr(date_range, "year") else date_range[0]
                start_date = end_date = pd.to_datetime(d)
        except Exception:
            start_date, end_date = None, None
    else:
        start_date, end_date = None, None

    st.sidebar.divider()
    st.sidebar.caption("Refine results")
    min_att = st.sidebar.slider("Min attendance (%)", 0, 100, 0, 5) / 100.0
    min_sat = st.sidebar.slider("Min satisfaction (1–5)", 0.0, 5.0, 0.0, 0.5)
    chart_top_n = st.sidebar.slider("Max bars in charts", 5, 50, 15)

    # ----- Apply filters -----
    f = df.copy()
    if "city" in f.columns and city_sel:
        f = f[f["city"].isin(city_sel)]
    if "program_id" in f.columns and program_sel:
        f = f[f["program_id"].isin(program_sel)]
    if use_dates and start_date is not None and end_date is not None and "first_session" in f.columns and "last_session" in f.columns:
        f = f[
            (f["first_session"].isna() | (f["first_session"] <= end_date))
            & (f["last_session"].isna() | (f["last_session"] >= start_date))
        ]
    if "attendance_rate" in f.columns and min_att > 0:
        f = f[f["attendance_rate"].fillna(0) >= min_att]
    if "avg_satisfaction" in f.columns and min_sat > 0:
        f = f[f["avg_satisfaction"].fillna(0) >= min_sat]

    st.sidebar.divider()
    st.sidebar.caption(f"**{len(df):,}** total → **{len(f):,}** after filters")

    # ----- KPIs -----
    participants = f["participant_id"].nunique() if "participant_id" in f.columns else len(f)
    programs_count = f["program_id"].nunique() if "program_id" in f.columns else np.nan
    avg_att_rate = safe_mean(f["attendance_rate"]) if "attendance_rate" in f.columns else np.nan
    avg_sat = safe_mean(f["avg_satisfaction"]) if "avg_satisfaction" in f.columns else np.nan
    avg_delta = safe_mean(f["outcome_delta"]) if "outcome_delta" in f.columns else np.nan

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Participants", f"{participants:,}")
    c2.metric("Programs", f"{int(programs_count):,}" if pd.notna(programs_count) else "—")
    c3.metric("Avg attendance", pct(avg_att_rate))
    c4.metric("Avg satisfaction", f"{avg_sat:.2f}" if pd.notna(avg_sat) else "—")
    c5.metric("Avg outcome Δ", f"{avg_delta:.2f}" if pd.notna(avg_delta) else "—")

    st.divider()

    # ----- Tabs -----
    tab_overview, tab_charts, tab_data, tab_quality = st.tabs(["Overview", "Charts", "Data", "Quality"])

    with tab_overview:
        st.subheader("Summary")
        n_prog = int(programs_count) if pd.notna(programs_count) else 0
        st.markdown(
            f"Current filters show **{participants:,}** participants across **{n_prog}** program(s). "
            "Switch to **Charts** for interactive visuals, **Data** to explore or download the table, and **Quality** for data checks."
        )
        st.caption("Tip: Use the sidebar to filter by city, program, date range, and min attendance or satisfaction. All tabs update live.")

    with tab_charts:
        st.subheader("Charts")
        sort_asc = st.radio("Sort order", ["Highest first", "Lowest first"], horizontal=True) == "Lowest first"
        left_c, right_c = st.columns(2)
        with left_c:
            if "attendance_rate" in f.columns and "program_id" in f.columns:
                prog_att = (
                    f.groupby("program_id", as_index=False)
                    .agg(
                        participants=("participant_id", "nunique"),
                        avg_attendance_rate=("attendance_rate", "mean"),
                        sessions_total=("sessions_total", "sum"),
                    )
                    .sort_values("avg_attendance_rate", ascending=sort_asc)
                )
                prog_att["avg_attendance_pct"] = (prog_att["avg_attendance_rate"] * 100).round(1)
                chart_att = make_bar_chart(
                    prog_att, "program_id", "avg_attendance_pct",
                    "Attendance by program (%)", "#0d9488", sort_asc=sort_asc, top_n=chart_top_n
                )
                st.altair_chart(chart_att, use_container_width=True)
                with st.expander("View table"):
                    st.dataframe(prog_att, use_container_width=True, hide_index=True)
            else:
                st.info("Attendance data not available.")
        with right_c:
            if "outcome_delta" in f.columns and "city" in f.columns:
                city_impact = (
                    f.groupby("city", as_index=False)
                    .agg(
                        participants=("participant_id", "nunique"),
                        avg_outcome_delta=("outcome_delta", "mean"),
                        avg_satisfaction=("avg_satisfaction", "mean"),
                    )
                    .sort_values("avg_outcome_delta", ascending=sort_asc)
                )
                chart_city = make_bar_chart(
                    city_impact, "city", "avg_outcome_delta",
                    "Impact by city (outcome Δ)", "#b45309", sort_asc=sort_asc, top_n=chart_top_n
                )
                st.altair_chart(chart_city, use_container_width=True)
                with st.expander("View table"):
                    st.dataframe(city_impact, use_container_width=True, hide_index=True)
            else:
                st.info("Outcome data not available.")

    with tab_data:
        st.subheader("Program detail")
        search = st.text_input("Search", placeholder="Participant ID, program ID, or city…", label_visibility="collapsed")
        show_cols = [c for c in [
            "participant_id", "program_id", "city",
            "sessions_total", "sessions_attended", "attendance_rate",
            "avg_satisfaction", "avg_nps", "pre_score", "post_score", "outcome_delta",
            "first_session", "last_session", "last_survey", "email"
        ] if c in f.columns]
        sort_cols = ["program_id", "city"] if "city" in f.columns else ["program_id"]
        table_df = f[show_cols].sort_values(sort_cols)
        if search and search.strip():
            q = search.strip().lower()
            mask = (
                table_df["participant_id"].astype(str).str.lower().str.contains(q, na=False)
                | table_df["program_id"].astype(str).str.lower().str.contains(q, na=False)
            )
            if "city" in table_df.columns:
                mask = mask | table_df["city"].astype(str).str.lower().str.contains(q, na=False)
            table_df = table_df[mask]
        st.caption(f"{len(table_df):,} rows")
        st.dataframe(table_df, use_container_width=True, hide_index=True)
        buf = io.StringIO()
        table_df.to_csv(buf, index=False)
        st.download_button("Download as CSV", buf.getvalue(), file_name="impact_export.csv", mime="text/csv")

    with tab_quality:
        st.subheader("Data quality")
        checks = []
        if "attendance_rate" in f.columns:
            checks.append(("Attendance rate missing", int(f["attendance_rate"].isna().sum())))
        if "avg_satisfaction" in f.columns:
            checks.append(("Satisfaction missing", int(f["avg_satisfaction"].isna().sum())))
        if "outcome_delta" in f.columns:
            checks.append(("Outcome delta missing", int(f["outcome_delta"].isna().sum())))
        checks.append(("Duplicate rows", int(f.duplicated().sum())))
        st.dataframe(pd.DataFrame(checks, columns=["Check", "Count"]), use_container_width=True, hide_index=True)
        st.caption("Counts for the current filtered dataset.")

    st.divider()
    st.caption("Nonprofit Impact Reporting · Built with Streamlit · Data from ETL pipeline")


if __name__ == "__main__":
    main()
