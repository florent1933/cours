from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Iterable

import polars as pl
import requests


def parse_amount(raw: str | None) -> float | None:
    value = (raw or "").strip()
    if not value or value.upper() == "N/A":
        return None

    value = value.replace("€", "").replace("$", "").replace(" ", "")

    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")

    try:
        return float(value)
    except ValueError:
        return None


def parse_date_expr(column_name: str) -> pl.Expr:
    return pl.coalesce(
        [
            pl.col(column_name).str.strptime(pl.Date, format="%Y-%m-%d", strict=False),
            pl.col(column_name).str.strptime(pl.Date, format="%d/%m/%Y", strict=False),
            pl.col(column_name).str.strptime(pl.Date, format="%Y/%m/%d", strict=False),
        ]
    )


def load_orders(orders_path: str | Path) -> pl.DataFrame:
    status_upper = pl.col("statut").cast(pl.String).str.strip_chars().str.to_uppercase()

    return (
        pl.read_csv(
            orders_path,
            schema_overrides={
                "date_commande": pl.String,
                "montant": pl.String,
                "statut": pl.String,
                "country": pl.String,
            },
            null_values=[""],
        )
        .with_columns(
            [
                pl.col("quantite").cast(pl.Int64, strict=False),
                parse_date_expr("date_commande").alias("order_date"),
                pl.col("montant")
                .map_elements(parse_amount, return_dtype=pl.Float64)
                .alias("montant_net"),
                pl.when(status_upper == "EN ATTENTE")
                .then(pl.lit("PENDING"))
                .otherwise(status_upper)
                .alias("statut_normalise"),
            ]
        )
        .with_columns(
            [
                pl.col("order_date").dt.strftime("%Y-%m").alias("mois_commande"),
                pl.when(
                    pl.col("order_date").is_not_null() & pl.col("montant_net").is_not_null()
                )
                .then(True)
                .otherwise(False)
                .alias("ligne_exploitable"),
            ]
        )
    )


def load_rates(rates_path: str | Path) -> pl.DataFrame:
    return (
        pl.read_csv(rates_path)
        .with_columns(
            [
                parse_date_expr("Date").alias("order_date"),
                pl.col("Country").alias("country"),
                pl.col("Exchange rate").cast(pl.Float64).alias("exchange_rate"),
            ]
        )
        .select(["order_date", "country", "exchange_rate"])
        .drop_nulls()
    )


def status_counts(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(pl.col("statut_normalise").value_counts(sort=True)).unnest(
        "statut_normalise"
    )


def revenue_by_category(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("ligne_exploitable"))
        .group_by("categorie")
        .agg(
            [
                pl.len().alias("nb_commandes"),
                pl.col("customer_id").n_unique().alias("nb_clients_uniques"),
                pl.col("montant_net").sum().round(2).alias("montant_total"),
                pl.col("montant_net").mean().round(2).alias("montant_moyen"),
            ]
        )
        .sort("montant_total", descending=True)
    )


def revenue_by_country(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("ligne_exploitable"))
        .group_by("country")
        .agg(
            [
                pl.len().alias("nb_commandes"),
                pl.col("customer_id").n_unique().alias("nb_clients_uniques"),
                pl.col("montant_net").sum().round(2).alias("montant_total"),
            ]
        )
        .sort("montant_total", descending=True)
    )


def revenue_by_country_category(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("ligne_exploitable"))
        .group_by(["country", "categorie"])
        .agg(
            [
                pl.len().alias("nb_commandes"),
                pl.col("customer_id").n_unique().alias("nb_clients_uniques"),
                pl.col("montant_net").sum().round(2).alias("montant_total"),
            ]
        )
        .sort(["country", "montant_total"], descending=[False, True])
    )


def join_exchange_rates(orders_df: pl.DataFrame, rates_df: pl.DataFrame) -> pl.DataFrame:
    return (
        orders_df.join(rates_df, on=["order_date", "country"], how="left")
        .with_columns(
            [
                (pl.col("montant_net") * pl.col("exchange_rate"))
                .round(2)
                .alias("montant_converti"),
                pl.col("exchange_rate").is_null().alias("fx_manquant"),
            ]
        )
    )


def load_fallback_countries(fallback_path: str | Path) -> list[dict]:
    with Path(fallback_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def countries_payload_to_frame(payload: Iterable[dict]) -> pl.DataFrame:
    rows = []
    for item in payload:
        common_name = item.get("name", {}).get("common")
        if not common_name:
            continue
        rows.append(
            {
                "country": common_name,
                "region": item.get("region") or "Unknown",
                "subregion": item.get("subregion") or "Unknown",
            }
        )

    if not rows:
        return pl.DataFrame(
            schema={
                "country": pl.String,
                "region": pl.String,
                "subregion": pl.String,
            }
        )

    return pl.DataFrame(rows).unique(subset=["country"], maintain_order=True)


def fetch_countries_dataframe(
    endpoint: str, fallback_path: str | Path, required_countries: set[str]
) -> pl.DataFrame:
    payload: list[dict]
    try:
        response = requests.get(endpoint, timeout=20)
        response.raise_for_status()
        payload = response.json()
        logging.info("API Rest Countries OK: %s pays recus", len(payload))
    except requests.RequestException:
        logging.exception("Echec appel Rest Countries, utilisation du fallback local")
        payload = load_fallback_countries(fallback_path)

    countries_df = countries_payload_to_frame(payload)
    available = set(countries_df.get_column("country").to_list()) if countries_df.height else set()
    missing = required_countries - available

    if missing:
        fallback_df = countries_payload_to_frame(load_fallback_countries(fallback_path))
        countries_df = pl.concat(
            [countries_df, fallback_df.filter(pl.col("country").is_in(sorted(missing)))],
            how="vertical_relaxed",
        ).unique(subset=["country"], maintain_order=True)

    return countries_df


def join_countries(df: pl.DataFrame, countries_df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.join(countries_df, on="country", how="left")
        .with_columns(
            [
                pl.col("region").fill_null("Unknown"),
                pl.col("subregion").fill_null("Unknown"),
            ]
        )
    )


def revenue_by_region(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("ligne_exploitable"))
        .group_by("region")
        .agg(pl.col("montant_converti").sum().round(2).alias("montant_converti_total"))
        .sort("montant_converti_total", descending=True)
    )


def final_aggregate(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("ligne_exploitable"))
        .group_by(["mois_commande", "region", "country", "categorie"])
        .agg(
            [
                pl.len().alias("nb_commandes"),
                pl.col("customer_id").n_unique().alias("nb_clients_uniques"),
                pl.col("montant_net").sum().round(2).alias("montant_total"),
                pl.col("montant_converti")
                .sum()
                .round(2)
                .alias("montant_converti_total"),
            ]
        )
        .sort(["mois_commande", "region", "country", "categorie"])
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="J3 volume + FX + API + aggregations")
    parser.add_argument(
        "--orders",
        default="cours/jeux_de_donnees/ecommerce_pedagogique/input/commandes_volume_j3.csv",
    )
    parser.add_argument(
        "--rates",
        default="cours/jeux_de_donnees/ecommerce_pedagogique/input/daily_j3.csv",
    )
    parser.add_argument(
        "--output",
        default="cours/jeux_de_donnees/ecommerce_pedagogique/output/j3_aggregate_final.csv",
    )
    parser.add_argument(
        "--countries-api",
        default="https://restcountries.com/v3.1/all?fields=name,region,subregion",
    )
    parser.add_argument(
        "--api-fallback",
        default="cours/jeux_de_donnees/ecommerce_pedagogique/api/rest_countries_fallback_j3.json",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    detail_output = output_path.with_name(f"{output_path.stem}_detail.csv")

    logging.info("Chargement du gros dataset commandes")
    orders_df = load_orders(args.orders)
    logging.info("Lignes lues: %s", orders_df.height)
    logging.info(
        "Lignes exploitables: %s",
        orders_df.filter(pl.col("ligne_exploitable")).height,
    )

    logging.info("Chargement des taux de change")
    rates_df = load_rates(args.rates)

    logging.info("Jointure devise sur date + pays")
    fx_df = join_exchange_rates(orders_df, rates_df)
    logging.info("Lignes avec taux manquant: %s", fx_df.filter(pl.col("fx_manquant")).height)

    required_countries = set(fx_df.get_column("country").unique().to_list())
    logging.info("Appel API Rest Countries")
    countries_df = fetch_countries_dataframe(
        args.countries_api,
        args.api_fallback,
        required_countries,
    )

    enriched_df = join_countries(fx_df, countries_df)

    logging.info("Exemples d'aggregations disponibles")
    logging.info("Statuts:\n%s", status_counts(enriched_df))
    logging.info("CA par categorie:\n%s", revenue_by_category(enriched_df).head(5))
    logging.info("CA par pays:\n%s", revenue_by_country(enriched_df))
    logging.info(
        "Total converti par region:\n%s",
        revenue_by_region(enriched_df),
    )

    final_df = final_aggregate(enriched_df)
    enriched_df.write_csv(detail_output)
    final_df.write_csv(output_path)

    logging.info("Export detail: %s", detail_output)
    logging.info("Export final: %s", output_path)


if __name__ == "__main__":
    main()
