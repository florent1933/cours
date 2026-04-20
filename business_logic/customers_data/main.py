from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl


def load_exchange_rates(rates_file: str | Path) -> tuple[pl.DataFrame, float | None]:
    rates_df = (
        pl.read_csv(rates_file)
        .filter(pl.col("Country") == "Euro")
        .with_columns(
            [
                pl.col("Date")
                .str.strptime(pl.Date, format="%Y-%m-%d", strict=False)
                .alias("order_date"),
                pl.col("Exchange rate").cast(pl.Float64).alias("exchange_rate_eur"),
            ]
        )
        .select(["order_date", "exchange_rate_eur"])
        .drop_nulls()
        .sort("order_date")
    )

    if rates_df.is_empty():
        return rates_df, None

    fallback_rate = rates_df.select(pl.col("exchange_rate_eur").last()).item()
    return rates_df, fallback_rate


def load_orders(orders_file: str | Path) -> pl.DataFrame:
    return (
        pl.read_csv(orders_file)
        .with_columns(
            [
                pl.col("Order Time")
                .str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S", strict=False)
                .alias("order_ts"),
                pl.col("Price").cast(pl.Float64).alias("price_usd"),
            ]
        )
        .with_columns(pl.col("order_ts").dt.date().alias("order_date"))
    )


def build_enriched_report(
    orders_df: pl.DataFrame, rates_df: pl.DataFrame, fallback_rate: float
) -> pl.DataFrame:
    return (
        orders_df.join(rates_df, on="order_date", how="left")
        .with_columns(pl.col("exchange_rate_eur").fill_null(fallback_rate))
        .with_columns(
            [
                (pl.col("price_usd") * pl.col("exchange_rate_eur"))
                .round(2)
                .alias("price_eur"),
                pl.col("order_date").dt.strftime("%d/%m/%Y").alias("order_date_fr"),
            ]
        )
        .with_columns(
            pl.col("price_eur")
            .sum()
            .over("order_date")
            .round(2)
            .alias("daily_revenue_eur")
        )
        .select(
            [
                "Order ID",
                "Customer Name",
                "Food Item",
                "Category",
                "Quantity",
                "Price",
                "Payment Method",
                "Order Time",
                "order_date_fr",
                "price_eur",
                "daily_revenue_eur",
            ]
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", default="input/restaurant_orders_anonymous.csv")
    parser.add_argument("--rates", default="input/daily.csv")
    parser.add_argument("--output", default="output/enriched_orders_with_eur.csv")
    args = parser.parse_args()

    output_dir = Path(args.output).parent
    output_dir.mkdir(exist_ok=True)

    print("--- Starting Process ---")
    print("\nStep 1: Loading exchange rates...")
    rates_df, fallback_rate = load_exchange_rates(args.rates)
    if fallback_rate is None:
        raise SystemExit("No EUR exchange rates available in input file.")

    print("\nStep 2: Loading sanitized order data...")
    orders_df = load_orders(args.orders)

    print("\nStep 3: Generating enriched report with EUR conversion...")
    report_df = build_enriched_report(orders_df, rates_df, fallback_rate)
    report_df.write_csv(args.output)

    print(f"\nSuccessfully generated final enriched report: {args.output}")
    print("\n--- Process Finished ---")


if __name__ == "__main__":
    main()
