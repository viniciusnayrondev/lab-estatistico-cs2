import streamlit as st
import pandas as pd

COLUNAS_NUMERICAS = [
    "team1_avg_RATING", "team2_avg_RATING", "rating_diff",
    "team1_avg_ADR", "team2_avg_ADR", "team1_avg_KAST", "team2_avg_KAST",
    "team1_totalwinrate", "team2_totalwinrate", "score_team1", "score_team2",
]
COLUNAS_CATEGORICAS = ["event_type", "decider_map", "winner"]

@st.cache_data
def carregar_dados():
    return pd.read_csv("data/processed/cs2_matches_clean.csv")