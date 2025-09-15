import io, pandas as pd
from typing import List, Dict, Any
from .verification import normalize_email, is_valid_email, normalize_phone, external_email_status

def clean_dataframe(df: pd.DataFrame, email_cols: List[str], phone_cols: List[str], key_cols: List[str]) -> dict:
    original_rows = len(df)

    # Strip whitespace
    df = df.applymap(lambda v: v.strip() if isinstance(v, str) else v)

    # Emails
    for c in email_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).apply(normalize_email)
            df[f"{c}__regex_valid"] = df[c].apply(is_valid_email)
            df[f"{c}__status"] = df[c].apply(external_email_status)

    # Phones
    for c in phone_cols:
        if c in df.columns:
            df[c], df[f"{c}__valid"] = zip(*df[c].astype(str).apply(normalize_phone))

    # Dedupe
    dedupe_cols = [c for c in key_cols if c in df.columns]
    before_dedupe = len(df)
    if dedupe_cols:
        df = df.drop_duplicates(subset=dedupe_cols, keep="first")
    after_dedupe = len(df)

    # Summary
    invalid_emails = {}
    for c in email_cols:
        if c in df.columns and f"{c}__status" in df.columns:
            invalid_emails[c] = int((df[f"{c}__status"] != "valid").sum())

    phone_invalids = {}
    for c in phone_cols:
        if c in df.columns and f"{c}__valid" in df.columns:
            phone_invalids[c] = int((~df[f"{c}__valid"]).sum())

    summary = {
        "original_rows": original_rows,
        "after_dedupe": after_dedupe,
        "duplicates_removed": before_dedupe - after_dedupe,
        "invalid_emails_by_column": invalid_emails,
        "invalid_phones_by_column": phone_invalids,
        "email_columns": email_cols,
        "phone_columns": phone_cols,
        "dedupe_key_columns": dedupe_cols,
    }
    return {"df": df, "summary": summary}
