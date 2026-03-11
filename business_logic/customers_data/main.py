import csv
from pathlib import Path
import collections
from datetime import datetime


def load_exchange_rates(rates_file):
    """
    Loads USD to EUR exchange rates from the provided CSV file.

    Args:
        rates_file (str or Path): Path to the daily exchange rates CSV.

    Returns:
        tuple: A tuple containing:
            - dict: A dictionary mapping dates to EUR exchange rates.
            - float: The most recent exchange rate as a fallback.
    """
    exchange_rates = {}
    last_known_rate = None
    most_recent_date = None

    try:
        with open(rates_file, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Country"] == "Euro":
                    try:
                        date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
                        rate = float(row["Exchange rate"])

                        exchange_rates[date] = rate

                        if most_recent_date is None or date > most_recent_date:
                            most_recent_date = date
                            last_known_rate = rate
                    except (ValueError, TypeError):
                        # This handles empty rate values or incorrect formats
                        if date and last_known_rate:
                            exchange_rates[date] = last_known_rate  # Forward-fill
    except FileNotFoundError:
        print(f"Error: Exchange rate file not found at {rates_file}")
        return {}, None
    except Exception as e:
        print(f"An error occurred while loading exchange rates: {e}")
        return {}, None

    print(
        f"Loaded {len(exchange_rates)} EUR exchange rates. Most recent rate ({most_recent_date}) is {last_known_rate}."
    )
    return exchange_rates, last_known_rate


def create_final_report(orders_file, output_file, exchange_rates, fallback_rate):
    """
    Creates an enriched CSV report with prices converted to EUR.
    """
    if not exchange_rates or fallback_rate is None:
        print("Cannot create report without exchange rates.")
        return

    # Pass 1: Calculate daily revenues in EUR
    daily_revenues_eur = collections.defaultdict(float)
    try:
        with open(orders_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    order_date = datetime.strptime(
                        row["Order Time"], "%Y-%m-%d %H:%M:%S"
                    ).date()
                    price_usd = float(row["Price"])

                    rate = exchange_rates.get(order_date, fallback_rate)
                    price_eur = price_usd * rate
                    daily_revenues_eur[order_date] += price_eur
                except (ValueError, KeyError) as e:
                    print(
                        f"Skipping row during revenue calculation due to data error: {e} - {row}"
                    )

    except FileNotFoundError:
        print(f"Error: Orders file not found at {orders_file}")
        return

    # Pass 2: Generate the enriched CSV
    try:
        with open(orders_file, mode="r", encoding="utf-8") as infile, open(
            output_file, mode="w", newline="", encoding="utf-8"
        ) as outfile:

            reader = csv.DictReader(infile)
            original_header = reader.fieldnames
            new_header = original_header + [
                "order_date_fr",
                "price_eur",
                "daily_revenue_eur",
            ]

            writer = csv.DictWriter(outfile, fieldnames=new_header)
            writer.writeheader()

            for row in reader:
                try:
                    order_date = datetime.strptime(
                        row["Order Time"], "%Y-%m-%d %H:%M:%S"
                    ).date()
                    price_usd = float(row["Price"])

                    rate = exchange_rates.get(order_date, fallback_rate)
                    price_eur = price_usd * rate
                    daily_revenue_eur = daily_revenues_eur.get(order_date, 0.0)

                    # Add new fields to the row
                    row["order_date_fr"] = order_date.strftime("%d/%m/%Y")
                    row["price_eur"] = f"{price_eur:.2f}"
                    row["daily_revenue_eur"] = f"{daily_revenue_eur:.2f}"

                    writer.writerow(row)
                except (ValueError, KeyError) as e:
                    print(
                        f"Skipping row during file writing due to data error: {e} - {row}"
                    )

        print(f"\nSuccessfully generated final enriched report: {output_file}")

    except Exception as e:
        print(f"An error occurred while writing the final report: {e}")


def main():
    """
    Main function to load data, perform conversions, and generate reports.
    """
    input_dir = Path(__file__).parent
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    orders_file = input_dir / "secret/restaurant_orders.csv"
    rates_file = input_dir / "input/daily.csv"
    output_file = output_dir / "enriched_orders_with_eur.csv"

    print("--- Starting Process ---")

    # 1. Load exchange rates
    print("\nStep 1: Loading exchange rates...")
    exchange_rates, fallback_rate = load_exchange_rates(rates_file)

    # 2. Create the final enriched report
    if exchange_rates:
        print("\nStep 2: Generating enriched report with EUR conversion...")
        create_final_report(orders_file, output_file, exchange_rates, fallback_rate)

    print("\n--- Process Finished ---")


if __name__ == "__main__":
    main()
