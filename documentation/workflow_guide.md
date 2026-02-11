# Workflow Guide

How to run and maintain the **Nonprofit Impact Reporting Platform** (`audit-impact-reporting`).

## One-time setup

1. **Clone the repo** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. **Raw data:** Place files in `data_raw/` or let the ETL generate sample data (it will bootstrap if raw files are missing).

## Regular workflow

### 1. Run the ETL

```bash
python etl_pipeline.py
```

- **Inputs:** `data_raw/` — `attendance.xlsx`, `crm_export.csv`, `survey_responses.csv`, `program_outcomes.xlsx`.
- **Outputs:** `data_clean/` — cleaned tables, `master_dataset.csv`, `data_quality_report.csv`.

### 2. Run the dashboard

```bash
streamlit run dashboard/app.py
```

- Reads `data_clean/master_dataset.csv`.
- Use sidebar filters (city, program, date range), then review KPIs, charts, and the detail table.

### 3. (Optional) Check data quality

- Open `data_clean/data_quality_report.csv` for row counts and basic quality stats per table.
- Use the dashboard’s **Data quality quick checks** expander for missing-value and duplicate counts on the filtered view.

## Updating data

1. Replace or add files in `data_raw/` with the same expected structure (see [data_dictionary.md](data_dictionary.md)).
2. Re-run `python etl_pipeline.py`.
3. Refresh the dashboard; it uses the updated `master_dataset.csv`.

## Customization

- **ETL:** Edit `etl_pipeline.py` to change cleaning rules, column mappings, or add sources.
- **Dashboard:** Edit `dashboard/app.py` to add metrics, charts, or filters.
- **Schema:** See [sql_schema/](../sql_schema/README.md) for the relational (CRM-style) table definitions and optional SQL implementation.
