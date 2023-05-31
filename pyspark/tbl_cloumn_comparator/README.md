`Pyspark` helper to identify mismatches in column data.  
Compares the two tables, column by column to generate report of mismatches.

* both tables should have the same column names
* table should have a identifiable primary key

# Usage
```python
report_df = tbl_cloumn_comparator(pi_df_prod_wipers, pi_df_test_wipers, ["primary_key1", "primary_key2"], examples=4, cloumns_lst=["col_a"])
report_df.show()
```

# Example Output
Comparing two datadframes. dataframe A is original and dataframe B is modified
we see here that data for these 2 columns are not matching for these primary keys.

| primary_key1 | primary_key2 | column_name | col_a | col_b |
|--------------|--------------|-------------|-------|-------|
| 1000         | 15190141     | col_11      | HIGH  | MID   |
| 1001         | 15190141     | col_11      | MID   | LOW   |
| 1010         | 2212884      | col_42      | 1     | 0.5   |
| 1011         | 2212884      | col_42      | 0.5   | 0.3   |
