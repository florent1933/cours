import polars as pl

df = pl.read_csv(
    "cours/jeux_de_donnees/ecommerce_pedagogique/input/commandes_brutes.csv"
)


print(df.head(1))

print("---  ---")

print(df.tail(1))


print(df.schema)


print(df.describe())


dff = df.select(pl.all().exclude("region", "statut", "date_commande"))
print(dff)


print(df.select(pl.col("date_commande")))


dff = df.select(pl.col("client", "email", "statut"))
