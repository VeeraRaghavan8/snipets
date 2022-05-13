from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col


def chk_diff_col(df, key, col_a, col_b, rows):
    """returns rows where col_a != col_b in a dataframe

    Args:
        df (dataframe): data
        key (list): list of primary keys
        col_a (string): cloumn a
        col_b (string): cloumn b
        rows (): number of rows to return

    Returns:
        dataframe: example schema. The first n cloums same as the primary key

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
        .where(df[col_a] != df[col_b])
        .limit(rows)
        .withColumnRenamed(col_a, "col_a")
        .withColumnRenamed(col_b, "col_b")
        .withColumn("column_name", lit(col_a))
        .selectExpr(*key, "column_name", "cast(col_a as string)", "cast(col_b as string)")
    )
    # print(df_ret.show())
    return df_ret


def tbl_cloumn_comparator(df_A, df_B, keys):
    """Compare cloumns of 2 dataframes. And generate report of all cloumns that do not match, with examples.

    Args:
        df_A (dataframe): dataframe A
        df_B (dataframe): dataframe B
        keys (list): list of StructField's of the table primary keys

    Returns:
        dataframe: example schema. The first n cloums same as the primary key
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

    # assert cloum name match #
    assert df_A.columns.sort() == df_B.columns.sort()

    # assert exitance of keyname in tables
    key_names = [k.name for k in keys]
    assert False not in [False for n in key_names if n not in df_A.columns]

    # init report df #
    report_schema = StructType(
        keys
        + [
            StructField("column_name", StringType(), True),
            StructField("col_a", StringType(), True),
            StructField("col_b", StringType(), True),
        ]
    )
    report_df = spark.createDataFrame([], report_schema)

    # Alias B cloumns and Join #
    df_B_alias = df_B.select([col(c).alias(c + "_B") for c in df_B.columns])
    join_cond = []
    for n in key_names:
        join_cond.append(df_A[n] == df_B_alias[n + "_B"])
    joined_tbl = df_A.join(df_B_alias, join_cond, "INNER")

    # Cloumns list, Default FULL #
    cloumns_lst = [x for x in df_A.columns if x not in key_names]
    for col_a in cloumns_lst:
        diff_df = chk_diff_col(joined_tbl, key_names, col_a, col_a + "_B", 3)
        report_df = report_df.union(diff_df)

    return report_df
