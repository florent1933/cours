import polars as pl

from cleaners import normalize_amount

df = pl.read_csv(
    "/Users/florentclapie/Documents/cours/cours/jeux_de_donnees/ecommerce_pedagogique/input/commandes_volume_j3.csv",
    # null_values=["N/A"],
    # ignore_errors=True,
    schema_overrides={"montant": pl.Utf8},
    # try_parse_dates=True,
)

print(df.schema)


df = df.with_columns(
    pl.coalesce(
        pl.col("date_commande").str.strptime(pl.Date, format="%Y-%m-%d", strict=False),
        pl.col("date_commande").str.strptime(pl.Date, format="%d/%m/%Y", strict=False),
        pl.col("date_commande").str.strptime(pl.Date, format="%Y/%m/%d", strict=False),
    ).alias("date_commande_normalized")
)

df.write_csv("test.csv")

# date normalized in fr format
df = df.with_columns(
    pl.col("date_commande_normalized").dt.strftime("%d/%m/%Y").alias("date_commande_fr")
)


# get day

df = df.with_columns(
    pl.col("date_commande_normalized").dt.strftime("%A").alias("real_day")
)
print(df)

# get week day
df = df.with_columns(
    pl.col("date_commande_normalized").dt.weekday().alias("real_weekday")
)
print(df)


# normalize amount
df = df.with_columns(
    pl.col("montant")
    .map_elements(normalize_amount, return_dtype=pl.Float64)
    .alias("montant_normalized")
)

print(df.select(pl.col("montant"), pl.col("montant_normalized")).head(10))

# get sum by real day
print(
    df.group_by("real_day", "real_weekday")
    .agg(
        pl.col("real_day").first().alias("real_day_name"),
        pl.len().alias("count"),
        pl.col("montant_normalized").sum().alias("total_montant"),
    )
    .sort("real_weekday")
)


print(df.schema)


best_category_by_country = (
    df.group_by("country", "categorie", "sous_categorie")
    .agg(
        pl.col("montant_normalized").sum().round(2).alias("total_montant"),
        # pl.col("client").n_unique().alias("unique_clients"),
    )
    .sort("total_montant", descending=True)
    .group_by("country", maintain_order=True)
    .first()
)

print(best_category_by_country)

# best_category_by_country.write_csv("test.csv")


best_category_by_country.schema


rates_df = pl.read_csv(
    "/Users/florentclapie/Documents/cours/cours/jeux_de_donnees/ecommerce_pedagogique/input/daily_j3.csv"
)


print("DF schema", df.schema)


rates_df = rates_df.with_columns(
    pl.col("Country").alias("country"),
    pl.col("Date")
    .str.strptime(pl.Date, format="%Y-%m-%d", strict=False)
    .alias("date_commande_normalized"),
)

print("Rates schema", rates_df.schema)

df_with_rates = df.join(
    rates_df, on=["country", "date_commande_normalized"], how="left"
)


print(df_with_rates)

# filter order with null exchange rate value
ddd = df_with_rates.filter(pl.col("Exchange rate").is_null())

print(
    ddd.select(
        pl.col(
            "customer_id",
            "commande_id",
            "country",
            "date_commande_normalized",
            "date_commande",
        ),
    )
)


print(df.select(pl.col("country").unique()))


# print(df.select(pl.col("country", "date_normalized")).head())

# print(rates_df.head())


country_currencies = pl.DataFrame(
    {
        "country": ["United Kingdom", "Euro", "Canada", "Japan", "Australia"],
        "currencies": ["£", "€", "$", "¥", "$AUD"],
    }
)


df_with_rates = df_with_rates.join(country_currencies, on="country", how="left")

dff = df_with_rates.with_columns(
    (pl.col("montant_normalized") * pl.col("Exchange rate")).alias("montant_converted")
).with_columns(
    (
        pl.col("montant_converted").round().cast(pl.Float64).cast(pl.Utf8)
        + " "
        + pl.col("currencies")
    ).alias("montant_converted_with_currency")
)


import requests

try:
    endpoint = "https://restcountries.com/v3.1/all?fields=name,region,subregion"
    response = requests.get(endpoint, timeout=20)
    response.raise_for_status()
    countries = response.json()
except:
    countries = [
        {
            "name": {
                "common": "Ivory Coast",
                "official": "Republic of Côte d'Ivoire",
                "nativeName": {
                    "fra": {
                        "official": "République de Côte d'Ivoire",
                        "common": "Côte d'Ivoire",
                    }
                },
            },
            "region": "Africa",
            "subregion": "Western Africa",
        }
    ]


country_beautiful = []

for c in countries:

    # country["country"] = country["name"]["common"]

    country_beautiful.append(
        {
            **c,
            "country": c["name"]["common"],
        }
    )


data_with_country = list(
    map(
        lambda x: {
            **x,
            "country": x["name"]["common"],
        },
        countries,
    )
)


x = pl.DataFrame(
    country_beautiful,
)

print(x)


dff = dff.with_columns(pl.col("country").replace("Euro", "France").alias("country"))

print(dff.join(x, on="country", how="left"))
