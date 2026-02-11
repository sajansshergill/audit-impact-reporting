"""
Nonprofit Impact Reporting Platform — ETL Pipeline (audit-impact-reporting)

Reads program datasets from data_raw/ and outputs standardized tables into data_clean/.
Includes a bootstrap option to generate sample messy data if raw files are missing.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd


# -----------------------------
# Config
# -----------------------------

@dataclass(frozen=True)
class Paths:
    base: Path = Path(__file__).resolve().parent
    data_raw: Path = base / "data_raw"
    data_clean: Path = base / "data_clean"

    attendance_raw: Path = data_raw / "attendance.xlsx"
    outcomes_raw: Path = data_raw / "program_outcomes.xlsx"
    surveys_raw: Path = data_raw / "survey_responses.csv"
    crm_raw: Path = data_raw / "crm_export.csv"


STANDARD_COLUMNS = {
    # Common fields across datasets
    "participant_id": "participant_id",
    "participantid": "participant_id",
    "student_id": "participant_id",
    "studentid": "participant_id",
    "id": "participant_id",

    "program_id": "program_id",
    "programid": "program_id",
    "program": "program_id",

    "city": "city",
    "site": "city",
    "location": "city",

    "date": "event_date",
    "event_date": "event_date",
    "session_date": "event_date",
    "attendance_date": "event_date",

    "attended": "attended",
    "present": "attended",

    "pre_score": "pre_score",
    "post_score": "post_score",
    "outcome_score_pre": "pre_score",
    "outcome_score_post": "post_score",

    "survey_score": "survey_score",
    "satisfaction": "survey_score",
    "nps": "nps",

    "email": "email",
    "phone": "phone",
    "dob": "dob",
    "birthdate": "dob",
}


# -----------------------------
# Helpers
# -----------------------------

def ensure_dirs(p: Paths) -> None:
    p.data_raw.mkdir(parents=True, exist_ok=True)
    p.data_clean.mkdir(parents=True, exist_ok=True)


def snake_case(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [snake_case(c) for c in df.columns]
    rename_map = {c: STANDARD_COLUMNS.get(c, c) for c in df.columns}
    return df.rename(columns=rename_map)


def normalize_city(city: str) -> str:
    if pd.isna(city):
        return np.nan
    c = str(city).strip().title()
    # Example normalization
    aliases = {
        "Nyc": "New York",
        "New York City": "New York",
        "Bk": "Brooklyn",
    }
    return aliases.get(c, c)


def parse_mixed_date(x) -> pd.Timestamp:
    """
    Parses mixed date formats (MM/DD/YYYY, YYYY-MM-DD, 'Jan 5 2026', etc.)
    Returns pandas Timestamp or NaT.
    """
    if pd.isna(x):
        return pd.NaT
    try:
        return pd.to_datetime(x, errors="coerce")
    except Exception:
        return pd.NaT


def standardize_participant_id(x) -> str:
    """
    Standardizes participant IDs to format: P-000123
    """
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    digits = re.sub(r"\D", "", s)
    if not digits:
        return np.nan
    return f"P-{int(digits):06d}"


def standardize_program_id(x) -> str:
    """
    Standardizes program IDs to format: PRG-001
    """
    if pd.isna(x):
        return np.nan
    s = str(x).strip().upper()
    digits = re.sub(r"\D", "", s)
    if digits:
        return f"PRG-{int(digits):03d}"
    # if string like "STEM_NYC" keep but normalize
    return re.sub(r"\s+", "_", s)


def basic_quality_report(df: pd.DataFrame, name: str) -> Dict[str, object]:
    report = {
        "table": name,
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }
    return report


# -----------------------------
# Bootstrap: Generate messy sample datasets
# -----------------------------

def bootstrap_messy_data(p: Paths, seed: int = 42) -> None:
    """
    Creates realistic messy datasets in data_raw/ if they don't exist.
    This helps you demo process improvement + cleaning.
    """
    rng = np.random.default_rng(seed)

    # --- CRM export (CSV)
    n = 500
    participant_ids = rng.integers(1, 260, size=n)  # intentional duplicates
    cities = rng.choice(["New York", "NYC", "Chicago", "chicago", "Bk", "Boston", None], size=n, p=[0.25,0.1,0.2,0.1,0.05,0.25,0.05])
    emails = [f"user{pid}@example.org" if rng.random() > 0.08 else None for pid in participant_ids]
    phones = [f"({rng.integers(200,999)})-{rng.integers(200,999)}-{rng.integers(1000,9999)}" if rng.random() > 0.12 else "" for _ in range(n)]
    dobs = rng.choice(["2005-01-10", "01/10/2005", "Jan 10 2005", None], size=n, p=[0.4, 0.3, 0.2, 0.1])

    crm = pd.DataFrame({
        "ParticipantID": participant_ids,
        "City": cities,
        "Email": emails,
        "Phone": phones,
        "Birthdate": dobs,
    })
    crm.to_csv(p.crm_raw, index=False)

    # --- Surveys (CSV)
    m = 800
    surveys = pd.DataFrame({
        "student_id": rng.integers(1, 320, size=m),
        "Program": rng.choice(["Program 1", "PRG1", "1", "2", "Program 2", "PRG-003"], size=m),
        "Date": rng.choice(["2026-02-01", "02/03/2026", "Feb 5 2026", "2026/02/07", None], size=m, p=[0.25,0.25,0.25,0.15,0.10]),
        "Satisfaction": rng.integers(1, 6, size=m),  # 1-5
        "NPS": rng.integers(0, 11, size=m),          # 0-10
    })
    # Introduce some gaps
    surveys.loc[rng.choice(m, size=35, replace=False), "Satisfaction"] = np.nan
    surveys.to_csv(p.surveys_raw, index=False)

    # --- Attendance (Excel)
    k = 1200
    attendance = pd.DataFrame({
        "ID": rng.integers(1, 320, size=k),
        "ProgramID": rng.choice(["1", "2", "3", "PRG-001", "PRG-002", "Program 3"], size=k),
        "Session Date": rng.choice(["2026-01-15", "01/20/2026", "Jan 25 2026", "2026/01/30"], size=k),
        "Present": rng.choice([1, 0, "Yes", "No", "Y", "N", None], size=k, p=[0.35,0.25,0.15,0.12,0.05,0.05,0.03]),
        "Site": rng.choice(["New York", "NYC", "Boston", "Chicago", "Bk"], size=k),
    })
    with pd.ExcelWriter(p.attendance_raw, engine="openpyxl") as writer:
        attendance.to_excel(writer, index=False, sheet_name="attendance")

    # --- Outcomes (Excel)
    t = 400
    outcomes = pd.DataFrame({
        "Participant Id": rng.integers(1, 320, size=t),
        "program_id": rng.choice(["1", "2", "3"], size=t),
        "outcome_score_pre": rng.normal(50, 10, size=t).round(1),
        "outcome_score_post": (rng.normal(55, 10, size=t)).round(1),
        "location": rng.choice(["New York City", "Boston", "Chicago", "NYC", None], size=t, p=[0.2,0.3,0.3,0.15,0.05]),
    })
    # Add some missingness
    outcomes.loc[rng.choice(t, size=20, replace=False), "outcome_score_post"] = np.nan

    with pd.ExcelWriter(p.outcomes_raw, engine="openpyxl") as writer:
        outcomes.to_excel(writer, index=False, sheet_name="outcomes")


# -----------------------------
# Loaders
# -----------------------------

def load_raw(p: Paths) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    crm = pd.read_csv(p.crm_raw)
    surveys = pd.read_csv(p.surveys_raw)
    attendance = pd.read_excel(p.attendance_raw, sheet_name=0)
    outcomes = pd.read_excel(p.outcomes_raw, sheet_name=0)
    return crm, surveys, attendance, outcomes


# -----------------------------
# Transformers
# -----------------------------

def clean_crm(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df["participant_id"] = df["participant_id"].apply(standardize_participant_id)
    df["city"] = df["city"].apply(normalize_city)
    df["dob"] = df.get("dob", pd.Series([pd.NaT] * len(df))).apply(parse_mixed_date)

    # Normalize blanks
    for c in ["email", "phone"]:
        if c in df.columns:
            df[c] = df[c].replace({"": np.nan, " ": np.nan})

    df = df.dropna(subset=["participant_id"]).drop_duplicates(subset=["participant_id"], keep="last")
    return df


def clean_surveys(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df["participant_id"] = df["participant_id"].apply(standardize_participant_id)
    df["program_id"] = df["program_id"].apply(standardize_program_id)
    df["event_date"] = df["event_date"].apply(parse_mixed_date)

    # Basic bounds checks
    if "survey_score" in df.columns:
        df.loc[(df["survey_score"] < 1) | (df["survey_score"] > 5), "survey_score"] = np.nan
    if "nps" in df.columns:
        df.loc[(df["nps"] < 0) | (df["nps"] > 10), "nps"] = np.nan

    df = df.dropna(subset=["participant_id", "program_id"])
    return df


def clean_attendance(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df["participant_id"] = df["participant_id"].apply(standardize_participant_id)
    df["program_id"] = df["program_id"].apply(standardize_program_id)
    df["event_date"] = df["event_date"].apply(parse_mixed_date)
    df["city"] = df["city"].apply(normalize_city)

    # Normalize attended values
    if "attended" in df.columns:
        df["attended"] = df["attended"].map({
            1: True, 0: False,
            "Yes": True, "No": False,
            "Y": True, "N": False,
            "yes": True, "no": False,
        }).astype("boolean")

    df = df.dropna(subset=["participant_id", "program_id", "event_date"])
    return df


def clean_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df["participant_id"] = df["participant_id"].apply(standardize_participant_id)
    df["program_id"] = df["program_id"].apply(standardize_program_id)

    if "city" in df.columns:
        df["city"] = df["city"].apply(normalize_city)

    # Ensure numeric
    for c in ["pre_score", "post_score"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["participant_id", "program_id"])
    return df


def build_master_dataset(crm: pd.DataFrame, attendance: pd.DataFrame, surveys: pd.DataFrame, outcomes: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a participant-program level master table with aggregated metrics.
    """
    # Attendance aggregates (per participant+program)
    att_agg = attendance.groupby(["participant_id", "program_id"], as_index=False).agg(
        sessions_total=("event_date", "count"),
        sessions_attended=("attended", lambda s: int(pd.Series(s).fillna(False).sum())),
        first_session=("event_date", "min"),
        last_session=("event_date", "max"),
    )

    # Survey aggregates
    surv_agg = surveys.groupby(["participant_id", "program_id"], as_index=False).agg(
        avg_satisfaction=("survey_score", "mean"),
        avg_nps=("nps", "mean"),
        survey_responses=("event_date", "count"),
        last_survey=("event_date", "max"),
    )

    # Outcomes (keep latest per participant+program)
    out_latest = outcomes.copy()
    if "post_score" in out_latest.columns:
        # if there is a notion of time later, we’d sort; for now just keep max post_score row as proxy
        out_latest = out_latest.sort_values(["participant_id", "program_id", "post_score"], ascending=[True, True, False])
    out_latest = out_latest.drop_duplicates(subset=["participant_id", "program_id"], keep="first")

    master = (
        att_agg.merge(surv_agg, on=["participant_id", "program_id"], how="outer")
              .merge(out_latest[["participant_id", "program_id", "pre_score", "post_score", "city"]]
                             if set(["pre_score", "post_score", "city"]).issubset(out_latest.columns.union(["city"]))
                             else out_latest,  # fallback
                    on=["participant_id", "program_id"], how="left")
              .merge(crm[["participant_id", "city", "email"]] if "email" in crm.columns else crm[["participant_id", "city"]],
                    on="participant_id", how="left", suffixes=("", "_crm"))
    )

    # Prefer city from outcomes, else CRM, else attendance (if you later add it)
    if "city_crm" in master.columns:
        master["city"] = master["city"].fillna(master["city_crm"])
        master = master.drop(columns=["city_crm"])

    # Derived metrics
    master["attendance_rate"] = np.where(
        master["sessions_total"].fillna(0) > 0,
        master["sessions_attended"].fillna(0) / master["sessions_total"].fillna(0),
        np.nan
    )

    if "pre_score" in master.columns and "post_score" in master.columns:
        master["outcome_delta"] = master["post_score"] - master["pre_score"]

    return master


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    p = Paths()
    ensure_dirs(p)

    # Bootstrap raw data if missing (so you can run immediately)
    if not (p.crm_raw.exists() and p.surveys_raw.exists() and p.attendance_raw.exists() and p.outcomes_raw.exists()):
        print("[bootstrap] Raw files missing. Generating messy sample datasets in data_raw/ ...")
        bootstrap_messy_data(p)

    print("[load] Reading raw datasets ...")
    crm_raw, surveys_raw, attendance_raw, outcomes_raw = load_raw(p)

    print("[clean] Cleaning datasets ...")
    crm = clean_crm(crm_raw)
    surveys = clean_surveys(surveys_raw)
    attendance = clean_attendance(attendance_raw)
    outcomes = clean_outcomes(outcomes_raw)

    print("[build] Building master dataset ...")
    master = build_master_dataset(crm=crm, attendance=attendance, surveys=surveys, outcomes=outcomes)

    # Quality reports
    reports = [
        basic_quality_report(crm, "crm_clean"),
        basic_quality_report(surveys, "surveys_clean"),
        basic_quality_report(attendance, "attendance_clean"),
        basic_quality_report(outcomes, "outcomes_clean"),
        basic_quality_report(master, "master_dataset"),
    ]
    report_df = pd.DataFrame(reports)

    # Write outputs
    print("[write] Writing clean outputs to data_clean/ ...")
    crm.to_csv(p.data_clean / "crm_clean.csv", index=False)
    surveys.to_csv(p.data_clean / "surveys_clean.csv", index=False)
    attendance.to_csv(p.data_clean / "attendance_clean.csv", index=False)
    outcomes.to_csv(p.data_clean / "outcomes_clean.csv", index=False)
    master.to_csv(p.data_clean / "master_dataset.csv", index=False)
    report_df.to_csv(p.data_clean / "data_quality_report.csv", index=False)

    print("\n✅ Done.")
    print("Outputs:")
    for f in [
        "crm_clean.csv",
        "surveys_clean.csv",
        "attendance_clean.csv",
        "outcomes_clean.csv",
        "master_dataset.csv",
        "data_quality_report.csv",
    ]:
        print(f" - data_clean/{f}")


if __name__ == "__main__":
    main()
