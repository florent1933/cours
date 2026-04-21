import polars as pl

df = pl.DataFrame(
    {
        "client": [" alice", "aba", "Charlie", "David", "Eve"],
        "montant": [1200.50, 850.75, 950.00, 1100.00, 1050.25],
        "statut": ["ok", "pending", None, "ok", "pending"],
    }
)


print(df.head(1))

print("---  ---")

print(df.tail(1))


print(df.schema)


print(df.describe())
