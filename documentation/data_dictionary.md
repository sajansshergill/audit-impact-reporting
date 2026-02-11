# Data Dictionary

Definitions for key fields in the **master dataset** (`data_clean/master_dataset.csv`) produced by the ETL pipeline in **audit-impact-reporting**.

## Identifiers

| Field | Type | Description |
|-------|------|-------------|
| `participant_id` | string | Unique participant identifier (e.g. P-000001). |
| `program_id` | string | Program identifier (e.g. PRG-001). |
| `email` | string | Participant email; may be missing. |

## Location

| Field | Type | Description |
|-------|------|-------------|
| `city` | string | Program site / city (e.g. Boston, New York). Missing values normalized to "Unknown". |

## Attendance

| Field | Type | Description |
|-------|------|-------------|
| `sessions_total` | numeric | Total sessions for the participant in the program. |
| `sessions_attended` | numeric | Sessions attended. |
| `attendance_rate` | numeric | `sessions_attended / sessions_total` (0–1). |
| `first_session` | date | First session date. |
| `last_session` | date | Last session date. |

## Surveys

| Field | Type | Description |
|-------|------|-------------|
| `avg_satisfaction` | numeric | Average satisfaction score (e.g. 1–5 scale). |
| `avg_nps` | numeric | Average Net Promoter Score. |
| `survey_responses` | numeric | Count of survey responses. |
| `last_survey` | date | Date of most recent survey. |

## Outcomes

| Field | Type | Description |
|-------|------|-------------|
| `pre_score` | numeric | Pre-program outcome score. |
| `post_score` | numeric | Post-program outcome score. |
| `outcome_delta` | numeric | Change in outcome (e.g. post − pre). |

## Source tables

- **CRM** → participant_id, program_id, city, email.
- **Attendance** → sessions, dates, attendance_rate.
- **Surveys** → satisfaction, NPS, last_survey.
- **Outcomes** → pre_score, post_score, outcome_delta.

The ETL standardizes column names, normalizes dates and numerics, and merges these sources into the master dataset. See the [workflow guide](workflow_guide.md) for how to run the pipeline.
