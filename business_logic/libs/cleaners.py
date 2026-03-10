from __future__ import annotations

from datetime import datetime


def clean_email(raw: str) -> tuple[str, bool]:
    value = (raw or "").strip().lower()
    return value, ("@" in value and "." in value)


def normalize_amount(raw: str) -> float | None:
    value = (raw or "").strip().replace("€", "").replace(" ", "")
    if value == "":
        return None
    if "," in value and "." in value:
        value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


def normalize_date(raw: str) -> str | None:
    value = (raw or "").strip()
    if not value:
        return None

    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        dt = datetime.strptime(value, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None

