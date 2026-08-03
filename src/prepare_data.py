import pandas as pd

df = pd.read_csv("data/raw/cs2_newestcombinedmatches.csv")

colunas_relevantes = [
    "match_id", "date", "tournament", "team1_name", "team2_name",
    "event_type", "decider_map", "winner",
    "team1_avg_RATING", "team2_avg_RATING", "rating_diff",
    "team1_avg_ADR", "team2_avg_ADR",
    "team1_avg_KAST", "team2_avg_KAST",
    "team1_totalwinrate", "team2_totalwinrate",
    "score_team1", "score_team2",
]

df = df[colunas_relevantes]

# Corrige inconsistência de capitalização em event_type (ex: "online" para "Online" e "lan" para "LAN")
def normalizar_event_type(valor):
    valor_limpo = valor.strip().title()
    if valor_limpo == "Lan":
        return "LAN"
    return valor_limpo

df["event_type"] = df["event_type"].apply(normalizar_event_type)

print("Número de linhas:", len(df))
print("Número de colunas:", len(df.columns))
print(df.head())

# Verifica os valores únicos de event_type (deve mostrar somente "Online" e "LAN")
print(df["event_type"].value_counts())