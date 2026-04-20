from __future__ import annotations

import argparse
from pathlib import Path
import sys

import polars as pl

# Allow direct execution: `python main.py` from template/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from libs.cleaners import normalize_amount, normalize_date

OUTPUT_FIELDS = [
    "commande_id",
    "client",
    "email",
    "montant",
    "date_commande",
    "statut",
    "email_clean",
    "email_valide",
    "montant_net",
    "date_commande_clean",
    "statut_normalise",
    "ligne_valide",
    "anomalie",
]


def build_anomaly(row: dict[str, object]) -> str:
    anomaly: list[str] = []
    raw_date = str(row.get("date_commande_source") or "").strip()

    if not bool(row.get("email_valide")):
        anomaly.append("email_invalide")
    if row.get("montant_net") is None:
        anomaly.append("montant_invalide")
    if row.get("date_commande_clean") is None and raw_date:
        anomaly.append("date_invalide")

    return "|".join(anomaly)


def transform_orders_frame(df: pl.DataFrame) -> pl.DataFrame:
    transformed = (
        df.with_columns(
            [
                pl.col("commande_id").cast(pl.Utf8),
                pl.col("client").cast(pl.Utf8).str.strip_chars().alias("client"),
                pl.col("email").cast(pl.Utf8).fill_null("").alias("email"),
                pl.col("montant").cast(pl.Utf8).fill_null("").alias("montant"),
                pl.col("date_commande")
                .cast(pl.Utf8)
                .fill_null("")
                .alias("date_commande_source"),
                pl.col("statut").cast(pl.Utf8).fill_null("").alias("statut"),
            ]
        )
        .with_columns(
            [
                pl.col("email")
                .str.strip_chars()
                .str.to_lowercase()
                .alias("email_clean"),
                pl.col("montant")
                .map_elements(normalize_amount, return_dtype=pl.Float64)
                .alias("montant_net"),
                pl.col("date_commande_source")
                .map_elements(normalize_date, return_dtype=pl.Utf8)
                .alias("date_commande_clean"),
                pl.col("statut")
                .str.strip_chars()
                .str.to_lowercase()
                .alias("statut_normalise"),
            ]
        )
        .with_columns(
            [
                (
                    pl.col("email_clean").str.contains("@", literal=True)
                    & pl.col("email_clean").str.contains(".", literal=True)
                ).alias("email_valide"),
                (
                    pl.col("montant_net").is_not_null()
                    & pl.col("date_commande_clean").is_not_null()
                    & pl.col("email_clean").str.len_chars().gt(0)
                ).alias("ligne_valide"),
            ]
        )
        .with_columns(
            [
                pl.struct(
                    [
                        "email_valide",
                        "montant_net",
                        "date_commande_clean",
                        "date_commande_source",
                    ]
                )
                .map_elements(build_anomaly, return_dtype=pl.Utf8)
                .alias("anomalie")
            ]
        )
        .select(OUTPUT_FIELDS)
    )

    return transformed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input/commandes_input_exemple.csv")
    parser.add_argument("--output", default="output/resultat_exemple.csv")
    args = parser.parse_args()

    df = pl.read_csv(args.input)
    output_df = transform_orders_frame(df)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.write_csv(output_path)
    print(f"OK -> {args.output}")


if __name__ == "__main__":
    main()
