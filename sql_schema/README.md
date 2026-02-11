# Relational Schema (CRM-Style)

This folder defines a **normalized relational schema** that matches the data model used by the ETL pipeline and the master dataset. It is intended for documentation, system design, or implementation in a database (e.g. SQLite, PostgreSQL) or CRM (e.g. Salesforce) when moving from flat files to a relational store.

## Purpose

- **Document** tables, fields, and relationships in one place.
- **Align** with the cleaned ETL outputs (`data_clean/*.csv`) and the [data dictionary](../documentation/data_dictionary.md).
- **Support** staff-facing docs and CRM-style workflows (participants, programs, attendance, outcomes, surveys).

## How It Relates to the ETL

| ETL output | Schema table(s) |
|------------|-----------------|
| `crm_clean.csv` | `participants` |
| `attendance_clean.csv` | `attendance_events` (raw) or `attendance_summary` (aggregated) |
| `surveys_clean.csv` | `survey_responses` (raw) or `survey_summary` (aggregated) |
| `outcomes_clean.csv` | `outcomes` |
| `master_dataset.csv` | Denormalized view joining all of the above (participant-program grain) |

The ETL currently reads/writes CSV. This schema describes how the same data would look in a relational database. The **master dataset** is equivalent to a single denormalized reporting table built from these tables.

## Entity Relationship (Text)

```
participants (1) ──< (N) attendance_events  >── (N) programs
participants (1) ──< (N) survey_responses    >── (N) programs
participants (1) ──< (N) outcomes           >── (N) programs
```

- **participants** — One row per participant (from CRM).
- **programs** — One row per program (e.g. PRG-001, PRG-002).
- **attendance_events** — One row per session; links participant + program + date + attended.
- **survey_responses** — One row per survey response; links participant + program + date + satisfaction/NPS.
- **outcomes** — One row per participant-program outcome (pre_score, post_score, outcome_delta).

Aggregated tables (`attendance_summary`, `survey_summary`) can be views or materialized tables for reporting and for building a scorecard/master view.

## Files

| File | Description |
|------|-------------|
| [schema.sql](schema.sql) | `CREATE TABLE` statements (SQLite-compatible). |
| [README.md](README.md) | This file — overview and relationship to ETL. |

## Usage

- **Documentation only:** Use this to explain the data model to staff or in process docs.
- **Implement in a database:** Run `schema.sql` in SQLite (or adapt for PostgreSQL/MySQL), then load `data_clean/*.csv` into the corresponding tables.
- **Salesforce/CRM:** Use the table and field list as a reference when mapping to Objects and Fields (e.g. Contact ↔ participants, Program__c ↔ programs, custom objects for attendance/outcomes/surveys).
