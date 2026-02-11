# Nonprofit Impact Reporting Platform

**Repository:** `audit-impact-reporting`

End-to-end **data systems** project: audit messy program data, run a single **ETL pipeline**, and explore results in a **modern Streamlit dashboard**. Built to demonstrate data engineering, documentation, and impact reporting—suitable for portfolio and technical interviews.

**Strong fit for roles in:** data systems & process improvement, nonprofit impact/operations, CRM & documentation support, and data analysis & visualization (e.g. mapping data collection processes, standardizing inputs for scorecards, staff-facing documentation, glossaries, and dashboards for internal decision-making). Raw data simulates **Excel, survey, and CRM-style exports** (e.g. Salesforce-style participant/program data).

---

## What This Project Does

- **Audits messy data** — Simulates real-world issues (inconsistent column names, duplicates, mixed date formats, missing values) across attendance, CRM, surveys, and outcomes.
- **Standardizes with ETL** — One Python pipeline that cleans, normalizes, and merges multiple sources into a single master dataset.
- **Documents the system** — Data dictionary, workflow guide, and glossary in `documentation/`.
- **Delivers a dashboard** — Streamlit app: filters (city, program, date range), KPIs, charts, and detail tables.

No ML—focused on **data systems, cleaning, and reporting**.

---

## Screenshot

Add a screenshot as `assets/dashboard-screenshot.png`, then uncomment the next line in this README to display it.

<!-- ![Dashboard](assets/dashboard-screenshot.png) -->

---

## Tech Stack

| Layer     | Tools |
|----------|--------|
| Language | Python 3.10+ |
| ETL/Data | pandas, numpy |
| Dashboard | Streamlit, Altair (interactive charts) |
| Data I/O | CSV, Excel (openpyxl) |
| Docs     | Markdown |

---

## Project Structure

```
audit-impact-reporting/
├── data_raw/                 # Raw inputs (attendance, CRM, surveys, outcomes)
├── data_clean/               # ETL outputs (cleaned tables + master_dataset.csv)
├── dashboard/
│   └── app.py                # Streamlit impact dashboard
├── documentation/
│   ├── data_dictionary.md    # Master dataset field definitions
│   ├── workflow_guide.md     # How to run ETL and dashboard
│   └── glossary.md           # Shared terminology
├── sql_schema/               # Relational schema (CRM-style tables + SQL DDL)
│   ├── README.md             # Schema overview and ETL alignment
│   └── schema.sql            # CREATE TABLE / VIEW (SQLite-compatible)
├── assets/                   # Optional: dashboard screenshot for README
├── etl_pipeline.py           # End-to-end ETL (clean, merge, quality report)
├── requirements.txt
└── README.md
```

---

## Quick Start

**1. Clone and enter the repo**

```bash
git clone https://github.com/<your-username>/audit-impact-reporting.git
cd audit-impact-reporting
```

**2. Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the ETL pipeline**

Reads from `data_raw/`, writes to `data_clean/`. If raw files are missing, the pipeline generates sample data so you can run immediately.

```bash
python etl_pipeline.py
```

**5. Launch the dashboard**

```bash
streamlit run dashboard/app.py
```

Open the URL in the terminal (e.g. `http://localhost:8501`).

---

## Dashboard

The app uses a **teal-and-neutral** design system, **Plus Jakarta Sans** typography, and a tabbed layout:

- **Overview** — Summary of filtered results and how to use the app.
- **Charts** — Interactive Altair bar charts (attendance by program, impact by city) with sort order and configurable bar limit; hover tooltips and zoom/pan.
- **Data** — Searchable table and **Download as CSV** for the current view.
- **Quality** — Missing-value and duplicate counts for the filtered dataset.

**Sidebar:** City and program multiselect, date range, min attendance %, min satisfaction, and max bars in charts. All views update as you change filters. A footer at the bottom credits the stack and data source.

---

## Data Sources (Simulated)

| Source            | Path | Purpose |
|-------------------|------|---------|
| Attendance        | `data_raw/attendance.xlsx` | Session-level attendance |
| CRM export        | `data_raw/crm_export.csv`  | Participants, programs, contact info |
| Survey responses  | `data_raw/survey_responses.csv` | Satisfaction, NPS |
| Program outcomes  | `data_raw/program_outcomes.xlsx` | Pre/post scores, outcome deltas |

The ETL produces **master_dataset.csv** in `data_clean/`, which the dashboard reads.

---

## Skills Demonstrated

- **Data systems auditing** — Identifying inconsistencies and designing a unified schema.
- **ETL design** — Cleaning, normalizing, and merging multi-source data.
- **Process documentation** — Data dictionary, workflow guide, glossary.
- **Dashboard development** — Streamlit UI with filters, metrics, and charts.
- **Reproducibility** — Pinned dependencies, clear run instructions, optional bootstrap data.

---

## For Recruiters

- **Role fit:** Data analyst, operations analyst, impact measurement, CRM/data systems, data & process documentation.
- **Deliverables:** Working ETL, documented schema, interactive dashboard, and supporting docs.
- **Run from scratch:** Clone → `pip install -r requirements.txt` → `python etl_pipeline.py` → `streamlit run dashboard/app.py`.

---

## How This Project Maps to Common JD Requirements

| JD area | How this project demonstrates it |
|--------|-----------------------------------|
| **Map & document data collection processes** | Workflow guide and data dictionary document how data flows from raw sources (Excel, CSV, surveys) into a single master dataset. |
| **Review sources for gaps, redundancies, inconsistencies** | ETL pipeline audits and cleans multiple sources; data quality report and dashboard Quality tab surface missing values and duplicates. |
| **Standardize data inputs for scorecards** | Master dataset is a single, standardized source; dashboard provides scorecard-style KPIs (participants, attendance, satisfaction, outcome delta). |
| **Document workflows, field definitions, staff-facing process docs** | `documentation/`: data dictionary (field definitions), workflow guide (how to run ETL and dashboard), glossary (shared terms). `sql_schema/`: relational (CRM-style) tables and SQL DDL. |
| **Data cleaning, validation, preparation for reporting** | ETL does cleaning, normalization, and validation; outputs feed the dashboard. |
| **Charts, tables, visual summaries for internal learning** | Dashboard: interactive Altair charts, tables, filters, and CSV export for decision-making. |
| **Collaborative glossary of data/program/impact terms** | `documentation/glossary.md` defines participant, program, attendance rate, outcome delta, NPS, ETL, etc. |
| **Spreadsheets & structured data** | pandas, Excel (openpyxl), CSV throughout; schema and column mapping in ETL. |
| **Dashboards / data visualization** | Streamlit dashboard with filters, metrics, and Altair charts. |
| **CRM-style data** | Raw data includes a CRM export (participants, programs, contact info); approach transfers to Salesforce or similar exports. |

---

## Interview Talking Points

Use these when walking through the project in an interview:

- **Problem:** Nonprofits often have fragmented data (Excel, CRM, surveys) with inconsistent schemas, so leadership can’t get reliable impact reports.
- **Approach:** Audited raw sources, designed a unified schema, and built one ETL pipeline that cleans and merges into a single master dataset.
- **Dashboard:** Streamlit app with a clear design system (teal accent, Plus Jakarta Sans), tabbed layout (Overview, Charts, Data, Quality), interactive Altair charts, search, and CSV export—all driven by the same filters.
- **Documentation:** Data dictionary, workflow guide, and glossary so the system is understandable and maintainable.
- **Reproducibility:** Pinned dependencies, clear Quick Start, and optional bootstrap data so the project runs from a fresh clone.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Data dictionary](documentation/data_dictionary.md) | Field definitions for the master dataset |
| [Workflow guide](documentation/workflow_guide.md)   | How to run and maintain the pipeline |
| [Glossary](documentation/glossary.md)              | Shared terminology |
| [SQL schema](sql_schema/README.md)                 | Relational (CRM-style) schema and DDL |
