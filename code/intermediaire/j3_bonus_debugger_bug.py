from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORDERS_PATH = ROOT / 'cours' / 'jeux_de_donnees' / 'ecommerce_pedagogique' / 'input' / 'commandes_volume_j3.csv'
RATES_PATH = ROOT / 'cours' / 'jeux_de_donnees' / 'ecommerce_pedagogique' / 'input' / 'daily_j3.csv'


def parse_amount(raw: str | None) -> float | None:
    value = (raw or '').strip()
    if not value or value.upper() == 'N/A':
        return None

    value = value.replace('€', '').replace('$', '').replace(' ', '')

    if ',' in value and '.' in value:
        if value.rfind(',') > value.rfind('.'):
            value = value.replace('.', '').replace(',', '.')
        else:
            value = value.replace(',', '')
    elif ',' in value:
        value = value.replace(',', '.')

    try:
        return float(value)
    except ValueError:
        return None


def parse_order_date_bad(raw: str | None) -> str | None:
    """Bug volontaire: ne gère qu'un seul format de date."""
    value = (raw or '').strip()
    if not value:
        return None

    try:
        return datetime.strptime(value, '%d/%m/%Y').date().isoformat()
    except ValueError:
        return None


def load_orders(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    'commande_id': row['commande_id'],
                    'country': row['country'],
                    'date_commande': row['date_commande'],
                    'order_date': parse_order_date_bad(row['date_commande']),
                    'montant_net': parse_amount(row['montant']),
                }
            )
    return rows


def load_rates(path: Path) -> dict[tuple[str, str], float]:
    lookup: dict[tuple[str, str], float] = {}
    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rate = (row['Exchange rate'] or '').strip()
            if not rate:
                continue
            lookup[(row['Date'], row['Country'])] = float(rate)
    return lookup


def build_summary(orders: list[dict], rates_lookup: dict[tuple[str, str], float]) -> dict[str, dict]:
    summary: dict[str, dict] = defaultdict(
        lambda: {
            'nb_commandes': 0,
            'lignes_non_converties': 0,
            'montant_converti_total': 0.0,
        }
    )

    for order in orders:
        country = order['country']
        summary[country]['nb_commandes'] += 1

        lookup_key = (order['order_date'], country)
        rate = rates_lookup.get(lookup_key)
        amount = order['montant_net']

        if rate is None or amount is None:
            summary[country]['lignes_non_converties'] += 1
            continue

        summary[country]['montant_converti_total'] += amount * rate

    return summary


def print_summary(summary: dict[str, dict]) -> None:
    print('country,nb_commandes,lignes_non_converties,montant_converti_total')
    for country in sorted(summary):
        row = summary[country]
        print(
            f"{country},{row['nb_commandes']},{row['lignes_non_converties']},{row['montant_converti_total']:.2f}"
        )


def main() -> None:
    orders = load_orders(ORDERS_PATH)
    rates_lookup = load_rates(RATES_PATH)
    summary = build_summary(orders, rates_lookup)
    print_summary(summary)


if __name__ == '__main__':
    main()
