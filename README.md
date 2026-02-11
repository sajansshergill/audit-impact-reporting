# Nonprofit Data Systems Audit Impact Reporting Platform

## Overview

The project simulates a real-world nonprofit data systems audit and redesign.
The goal is to transform fragmented program data into a standardized, documented, and reportable system that supports organizationsl learning and decision-making.

Many nonprofit collect data across spreadsheets, surveys, and CRM exports, but lack standardized workflows, documentation, and reporting infrastructure. This project demonstrates how to:

- Audit messy data processes
- Identify gaps and redundancies
- Standardize data inputs
- Document workflows
- Build an impact reporting dashboard
- Create a share organizational data glossary

The project mirrors the responsibilities of a data systems analyst working in nonprofit operations.

---

## Problem Statement

A mid-sized nonprofit runs youth education programs across multiple cities. Each program team tracks attendance, outcomes, and participat surveys differently using Excel files, survey tools, and CRM exports. Leadership struggles to generate reliable impact reports due to:

- inconsistent field naming
- duplicate records
- missing data
- redundant data entry
- unclear reporting standards
- lack of documentation

This project redesigns the data system from the ground up.

---

## Objectives

- Map existing data collection processes
- Audit raw datasets for inconsistencies
- Standdardize schema and field definitions
- Build a clean master dataset
- Document workflows and data strategy
- Create an impact dashboard
- Develop a shared data glossary

---

## Tech Stack

- Python (pandas, numpy)
- SQL (SQLite / Postgres schema design)
- Excel / CSV data workflows
- Tableau / Power BI / Streamlit dashboard
- Markdown documentation
- Data modeling & process mapping

No machine learning is used - this is a data systems and operations analytics project.

---

## Project Structure

```
nonprofit-data-system/
│
├── data_raw/              # messy program data (simulated)
├── data_clean/            # standardized datasets
├── etl_pipeline.py        # cleaning & transformation scripts
│
├── sql_schema/            # CRM-style relational schema
├── dashboard/             # impact dashboard files
│
├── documentation/
│   ├── data_dictionary.md
│   ├── workflow_guide.md
│   ├── glossary.md
│
├── impact_report.pdf      # executive summary
└── README.md
```

---

## Phase 1: Data Systems Audit

Simulated raw program datasets intentionally include:

- inconsistent column naming
- duplicate participant IDs
- mized date formats
- missing survey responses
- redundant tracking fields

The audit identifies structural issues and proposes improvements.

Deliverables:
- Gap analysis report
- Process map
- Redundancy assessment
- Recommendations memo

---

## Phase 2: Data Standardization

A unified schema is designed to replace fragmented tracking.

The ETL pipeline:

- cleans participant records
- standardizes program IDs
- normalizes dates and categorical fields
- merges datasets into a master table
- validates missing values

Deliverables:
- Clean master dataset
- Autmomated cleaning pipeline
- Data dictionary

---

## Phase 3: CRM Workflow Simulation

A Salesforce-style relational structure is created using SQL:

Tables include:

- Partcipants
- Programs
- Attendance
- Outcomes
- Surveys

This phase documents:

- table relationships
- field definitions
- workflow diagrams
- staff-facing usage instructions

Deliverables:
- relational schema
- workflow documentation
- system usage guide

---

## Phase 4: Impact Dashboard

A dashboard summarizes program performance:

Metrics include:

- completion rates
- attendance trends
- outcome improvements
- demographic breakdowns
- city-level comparisons

The dashboad supoorts internal learning and decision-making.

Deliverables:
- visual charts
- summary tables
- executuve impact report

---

## Phase 5: Organizational Data Glossary

A shared glossary defines:

- program KPIs
- impact metrics
- participant terminology
- reporting standards
- data entry rules

This creates a common language across teams.

Deliverable:
- Nonprofit Data Playbook

---

## Key Skills Demonstrated

- Data system auditing
- Process documentation
- Data cleaning & validation
- Schema design
- Workflow standardization
- Dashboard reporting
- Cross-team communication
- Organizational anlaytical thinking

---

## How to Run the Pipeline

1. Clone repository

```
git clone https://github.com/yourusername/nonprofit-data-system
cd nonprofit-data-system
```

2. Install dependencies

```
pip install pandas numpy
```

3. Run ETL pipeline

```
python etl_pipeline.py
```

4. Explore clean datasets and dashboard outputs

---

## Real-World Relevance

This project reflects work commly done by:

- nonprofit data analysts
- operations analysts
- impact measurement teams
- CRM administrators
- program evaluation specialists

It emphasizes structure, documentation, and organizational clarity - not just code.
