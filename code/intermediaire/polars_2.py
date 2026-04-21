import polars as pl

from cleaners import normalize_amount

df = pl.read_csv(
    "cours/jeux_de_donnees/ecommerce_pedagogique/input/commandes_brutes.csv"
)

normalize_amount(" 1 200,50 €")

print(df.head(1))

print("---  ---")

print(df.tail(1))


print(df.schema)


print(df.describe())


# dff = df.select(pl.all().exclude("region", "statut", "date_commande"))
# print(dff)


print(df.select(pl.col("date_commande")))


dff = df.select(
    pl.col(
        "client", "email", "statut", "profit", "montant", "categorie", "sous_categorie"
    )
)

print(dff)
# dff = dff.filter(pl.col("statut") == "pending")

# dff = dff.sort("profit", descending=True)

dff = dff.with_columns(
    pl.col("email").str.to_lowercase().str.strip_chars().alias("email_cleaned")
)

print(dff)
# is email valid, contains "@" and "."
dff = dff.with_columns(
    (
        pl.col("email_cleaned").str.contains("@")
        # and
        & pl.col("email_cleaned").str.contains("\\.")
    ).alias("is_valid_email")
)

print(dff)

# filter email != email cleaned
print(dff.filter(~pl.col("is_valid_email")))


dff = dff.with_columns(
    pl.col("montant")
    .map_elements(normalize_amount, return_dtype=pl.Float64)
    .alias("montant_normalized")
)

print(dff)


AVAILABLE_CURRENCIES = ["€", "$", "£", "¥"]
# €$£¥
# get currency from montant
dff = dff.with_columns(
    pl.col("montant")
    .str.replace_all(f"[^{''.join(AVAILABLE_CURRENCIES)}]", "")
    .alias("currency")
)


VAT_PERCENTAGE = 0.20

dff = (
    dff.with_columns(
        (pl.col("montant_normalized") * VAT_PERCENTAGE).alias("vat_amount")
    )
    .with_columns(
        (pl.col("montant_normalized") + pl.col("vat_amount"))
        .round(2)
        .alias("total_with_vat")
    )
    .with_columns(
        (pl.col("total_with_vat").cast(pl.Utf8) + " " + pl.col("currency")).alias(
            "total_with_vat_and_currency"
        )
    )
)

print(dff.select(pl.all().exclude("email", "email_cleaned", "is_valid_email")))


### show unique values of statut
print(dff.select(pl.col("statut").unique()))


dff = dff.with_columns(
    pl.col("statut")
    .str.strip_chars()
    .str.to_lowercase()
    .alias("statut_cleaned")
    .replace(
        {
            "ok": "terminé",
            "en_attente": "en attente",
            "pending": "en attente",
        }
    )
)

print(dff.select(pl.col("statut_cleaned").unique()))


dff.write_csv(
    "cours/jeux_de_donnees/ecommerce_pedagogique/input/commandes_nettoyees.csv"
)


print(dff["statut_cleaned"].value_counts(sort=True).reverse())

print(dff["categorie"].value_counts(sort=True).reverse())


print(
    dff.group_by(["statut_cleaned"]).agg(
        pl.len().alias("count"),
        pl.col("montant_normalized").sum().alias("total_montant"),
        pl.col("profit").sum().alias("total_profit"),
    )
)


print(
    dff.group_by("categorie", "sous_categorie")
    .agg(
        pl.len().alias("count"),
        pl.col("montant_normalized").sum().alias("total_montant"),
        pl.col("profit").sum().alias("total_profit"),
    )
    .sort(["categorie", "sous_categorie"])
)
