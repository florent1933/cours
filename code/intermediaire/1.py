import polars as pl

df = pl.DataFrame(
    {
        "A": [1, 2, 3],
        "B": ["a", "b", "c"],
        "C": [True, False, True],
    }
)

print(df)
print(df.head())

print(df.describe())


df = df.with_columns((pl.col("A") * 2).alias("A_doubled"))
print(df)

print(df.select(pl.all(), pl.col("B").str.to_uppercase().alias("B_upper")))


print(df.filter(pl.col("A") > 2))

print(df.group_by("C").agg(pl.sum("A").alias("sum_A")))

print(df.sort("A", descending=True))

print(df.with_columns(pl.col("A").cast(pl.Float64).alias("A_float")))

print(df.with_columns(pl.col("B").str.contains("a").alias("B_contains_a")))

print(df.with_columns(pl.col("C").cast(pl.Int8).alias("C_int")))

print(df.with_columns(pl.col("A").is_null().alias("A_is_null")))

print(df.null_count())


print(df.with_columns(pl.col("A").fill_null(0).alias("A_filled")))

print(df.with_columns(pl.col("A").drop_nulls().alias("A_no_nulls")))

print(df.with_columns(pl.col("A").is_not_null().alias("A_is_not_null")))

# filter all nulls
print(df.filter(pl.col("A").is_null() | pl.col("B").is_null() | pl.col("C").is_null()))


print