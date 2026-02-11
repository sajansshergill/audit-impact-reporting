-- Nonprofit Impact Reporting — Relational Schema (SQLite-compatible)
-- Aligns with ETL outputs: crm_clean, attendance_clean, surveys_clean, outcomes_clean, master_dataset.
-- Run this in SQLite (or adapt for PostgreSQL/MySQL) to create the tables.

-- ---------------------------------------------------------------------------
-- Core entities
-- ---------------------------------------------------------------------------

-- One row per participant (from CRM export).
CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    email          TEXT,
    city           TEXT,
    dob            DATE,
    created_at     TEXT DEFAULT (datetime('now'))
);

-- One row per program (sites/cohorts).
CREATE TABLE IF NOT EXISTS programs (
    program_id TEXT PRIMARY KEY,
    city       TEXT,
    name       TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------------
-- Attendance: one row per session (grain of attendance_clean.csv).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS attendance_events (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT NOT NULL,
    program_id     TEXT NOT NULL,
    event_date     DATE NOT NULL,
    attended       INTEGER NOT NULL CHECK (attended IN (0, 1)),
    city           TEXT,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
    FOREIGN KEY (program_id)     REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_attendance_participant_program
    ON attendance_events(participant_id, program_id);

-- Aggregated attendance per participant-program (mirrors ETL aggregation).
CREATE VIEW IF NOT EXISTS attendance_summary AS
SELECT
    participant_id,
    program_id,
    COUNT(*)                    AS sessions_total,
    SUM(attended)               AS sessions_attended,
    MIN(event_date)             AS first_session,
    MAX(event_date)             AS last_session,
    CAST(SUM(attended) AS REAL) / NULLIF(COUNT(*), 0) AS attendance_rate
FROM attendance_events
GROUP BY participant_id, program_id;

-- ---------------------------------------------------------------------------
-- Survey responses: one row per response (grain of surveys_clean.csv).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS survey_responses (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT NOT NULL,
    program_id     TEXT NOT NULL,
    event_date     DATE NOT NULL,
    survey_score   REAL,
    nps            REAL,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
    FOREIGN KEY (program_id)     REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_survey_participant_program
    ON survey_responses(participant_id, program_id);

-- Aggregated surveys per participant-program.
CREATE VIEW IF NOT EXISTS survey_summary AS
SELECT
    participant_id,
    program_id,
    AVG(survey_score)   AS avg_satisfaction,
    AVG(nps)            AS avg_nps,
    COUNT(*)            AS survey_responses,
    MAX(event_date)     AS last_survey
FROM survey_responses
GROUP BY participant_id, program_id;

-- ---------------------------------------------------------------------------
-- Outcomes: one row per participant-program (grain of outcomes_clean.csv).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS outcomes (
    participant_id TEXT NOT NULL,
    program_id     TEXT NOT NULL,
    pre_score      REAL,
    post_score     REAL,
    city           TEXT,
    recorded_at    TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (participant_id, program_id),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
    FOREIGN KEY (program_id)     REFERENCES programs(program_id)
);

-- ---------------------------------------------------------------------------
-- Master / scorecard table: participant-program grain with all metrics.
-- Mirrors data_clean/master_dataset.csv produced by the ETL.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS master_dataset (
    participant_id    TEXT,
    program_id        TEXT,
    city              TEXT,
    email             TEXT,
    sessions_total    REAL,
    sessions_attended REAL,
    attendance_rate   REAL,
    first_session     TEXT,
    last_session      TEXT,
    avg_satisfaction  REAL,
    avg_nps           REAL,
    survey_responses  REAL,
    last_survey       TEXT,
    pre_score         REAL,
    post_score        REAL,
    outcome_delta     REAL
);

CREATE INDEX IF NOT EXISTS idx_master_participant_program
    ON master_dataset(participant_id, program_id);
