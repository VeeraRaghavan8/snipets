# SPARK COMMON SYNTAX

## WRITE

```python
df1.repartition(1)\
        .write.format("com.databricks.spark.csv")\
        .option("header", "true").option("delimiter", "|")\
        .mode("overwrite")\
        .save("s3://bucket/key/*.txt")

df2.write.format("orc")\
         .mode("overwrite")\
         .save("s3://bucket/key/*.orc")
```

## READ

```python
df = spark.read.format("orc")\
                .load("<<s3://bucket/key_name>>")

df = spark.read.format("com.databricks.spark.csv")\
               .option("inferSchema",True)\
               .option("header",True)\
               .option("delimiter", "|")\
               .load("s3://bucket/key/file.csv")
```

## JOIN
```python
cond = [df_A["col_x"] == df_B["col_x"]
        ,df_A["col_y"] == df_B["col_y"]]
joined_tbl = df_A.join(df_B, cond, "INNER")
```

## GROUP BY AGG

## CASE STATEMENT

## GROUP BY THEN SORT

## JOIN SQL BUILDER

## CREATE TEMP VIEW