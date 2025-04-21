import pandas as pd

pd.read_excel("clean_ai_products.xlsx").groupby('department', group_keys=False).head(10).reset_index(drop=True).to_excel('clean_ai_products_subset.xlsx', index=False)
