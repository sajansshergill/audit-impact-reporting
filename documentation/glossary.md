# Glossary

Shared terms for the **Nonprofit Impact Reporting Platform** (audit-impact-reporting).

| Term | Definition |
|------|-------------|
| **Participant** | Individual enrolled in a program; identified by `participant_id`. |
| **Program** | A distinct program or cohort; identified by `program_id`. |
| **Attendance rate** | Proportion of sessions attended (0–1 or 0–100%). |
| **Satisfaction** | Survey-based satisfaction score (e.g. 1–5). |
| **NPS** | Net Promoter Score from surveys. |
| **Outcome delta** | Change in outcome measure (e.g. post_score − pre_score). |
| **Master dataset** | Single table produced by the ETL, joining CRM, attendance, surveys, and outcomes. Written to `data_clean/master_dataset.csv`. |
| **ETL** | Extract, transform, load — the pipeline in `etl_pipeline.py` that cleans and merges raw data into the master dataset. |

See also: [Data dictionary](data_dictionary.md), [Workflow guide](workflow_guide.md).
