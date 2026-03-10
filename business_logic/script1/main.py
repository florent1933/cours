from __future__ import annotations

import argparse
from pathlib import Path
import sys

# Allow direct execution: `python main.py` from script1/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from libs.csv_io import read_csv_rows, write_csv_rows
from libs.cleaners import clean_email, normalize_amount, normalize_date

OUTPUT_FIELDS = [
    "commande_id",
    "client",
    "email_clean",
    "email_valide",
    "montant_net",
    "date_commande",
    "statut",
    "anomalie",
]


def transform_order_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []

    for row in rows:
        raw_date = row.get("date_commande", "")
        email_clean, email_ok = clean_email(row.get("email", ""))
        amount = normalize_amount(row.get("montant", ""))
        date_clean = normalize_date(raw_date)
        anomaly = []

        if not email_ok:
            anomaly.append("email_invalide")
        if amount is None:
            anomaly.append("montant_invalide")
        if date_clean is None and raw_date.strip():
            anomaly.append("date_invalide")

        output_rows.append(
            {
                "commande_id": str(row.get("commande_id", "")),
                "client": str(row.get("client", "")).strip(),
                "email_clean": email_clean,
                "email_valide": str(email_ok).lower(),
                "montant_net": "" if amount is None else f"{amount:.2f}",
                "date_commande": date_clean or "",
                "statut": str(row.get("statut", "")).strip(),
                "anomalie": "|".join(anomaly),
            }
        )

    return output_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input/commandes_input_exemple.csv")
    parser.add_argument("--output", default="output/resultat_exemple.csv")
    parser.add_argument("--secret-dir", default="secret")
    args = parser.parse_args()

    secret_dir = Path(args.secret_dir)
    if not secret_dir.exists():
        raise SystemExit("Missing secret directory")

    rows = read_csv_rows(Path(args.input))
    output_rows = transform_order_rows(rows)
    write_csv_rows(Path(args.output), OUTPUT_FIELDS, output_rows)
    print(f"OK -> {args.output}")


if __name__ == "__main__":
    main()
