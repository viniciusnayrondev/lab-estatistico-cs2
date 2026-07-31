import pandas as pd

df = pd.read_csv("data/raw/cs2_newestcombinedmatches.csv")

print("Número de linhas:", len(df))
print("Número de colunas:", len(df.columns))