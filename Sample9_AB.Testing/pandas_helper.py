

# Swap columns in one or more dataframes
def swap(col, idx, dfs)
    for df in dfs:
        pop_col = df.pop(col)
        df.insert(idx, col, pop_col)


  