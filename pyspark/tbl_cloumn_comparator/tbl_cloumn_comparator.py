from pyspark.sql.functions import col, lit

def chk_diff_col(df, key, col_a, col_b, rows):
    """returns rows where col_a != col_b in a dataframe

    Args:
        df (dataframe): data
        key (list): list of primary keys
        col_a (string): cloumn a
        col_b (string): cloumn b
        rows (): number of rows to return

    Returns:
        dataframe: example schema. The first n cloumns same as the primary key

            StructType(
                List(
                    StructField(<key1>, <key type>, true),
                    StructField(<key2>, <key type>, true),
                    ...
                    StructField(column_name, StringType, false),
                    StructField(col_a, StringType, true),
                    StructField(col_b, StringType, true),
                )
            )
    """
    df_ret = (
        df.select(*key, col_a, col_b)
        .where(f"{col_a} != {col_b} or ({col_a} is NULL and {col_b} is not NULL) or ({col_a} is not NULL and {col_b} is NULL)")
        .limit(rows)
        .withColumnRenamed(col_a, "col_a")
        .withColumnRenamed(col_b, "col_b")
        .withColumn("column_name", lit(col_a))
        .selectExpr(*key, "column_name", "cast(col_a as string)", "cast(col_b as string)")
    )
    # print(df_ret.show())
    return df_ret


def tbl_cloumn_comparator(df_A_full, df_B_full, keys: list, examples: int = 3, cloumns_lst: list = None):
    """Compare cloumns of 2 dataframes. And generate report of all cloumns that do not match, with examples.

    Args:
        df_A (dataframe): dataframe A
        df_B (dataframe): dataframe B
        keys (list): list of the tables primary keys
        examples (int): list of StructField's of the table primary keys. Defaults to 3.
        cloumns_lst (list): list of cloumns to compare. Defaults to None.

    Returns:
        dataframe: example schema. The first n cloumns same as the primary key
            StructType(
                List(
                    StructField(<key1>, <key type>, true),
                    StructField(<key2>, <key type>, true),
                    ...
                    StructField(column_name, StringType, false),
                    StructField(col_a, StringType, true),
                    StructField(col_b, StringType, true),
                )
            )
    """

    # assert existence of keyname in tables
    assert False not in [False for n in keys if n not in df_A_full.columns]
    
    # Cloumns list, Default FULL #
    if cloumns_lst is None:
        cloumns_lst_final = [x for x in df_A_full.columns if x not in keys]
    else :
        cloumns_lst_final = [x for x in cloumns_lst if x not in keys]
    print(cloumns_lst_final)
    
    df_A = df_A_full.select(keys + cloumns_lst_final)
    df_B = df_B_full.select(keys + cloumns_lst_final)
    
    # assert cloum name match #
    assert df_A.columns.sort() == df_B.columns.sort()

    # init report df #
    report_schema = df_A.select(keys).withColumn("column_name", lit("")).withColumn("col_a", lit("")).withColumn("col_b", lit("")).schema
    report_df = spark.createDataFrame([], report_schema)

    # Alias B cloumns and Join #
    df_B_alias = df_B.select([col(c).alias(c + "_B") for c in df_B.columns])
    join_cond = []
    for n in keys:
        join_cond.append(df_A[n] == df_B_alias[n + "_B"])
    
    joined_tbl = df_A.join(df_B_alias, join_cond, "INNER")

    for col_a in cloumns_lst_final:
        diff_df = chk_diff_col(joined_tbl, keys, col_a, col_a + "_B", examples)
        report_df = report_df.union(diff_df)

    return report_df
