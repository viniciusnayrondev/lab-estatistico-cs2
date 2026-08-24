import streamlit as st
import pandas as pd
import sys
sys.path.append("src")
import minhastats as ms

st.title("Laboratório Estatístico Interativo — CS2")

df = pd.read_csv("data/processed/cs2_matches_clean.csv")

st.write("Dataset carregado com sucesso!")
st.write(f"Número de partidas: {len(df)}")

colunas_numericas = [
    "team1_avg_RATING", "team2_avg_RATING", "rating_diff",
    "team1_avg_ADR", "team2_avg_ADR",
    "team1_avg_KAST", "team2_avg_KAST",
    "team1_totalwinrate", "team2_totalwinrate",
    "score_team1", "score_team2",
]

variavel_escolhida = st.selectbox("Escolha uma variável para analisar:", colunas_numericas)

st.write(f"Você escolheu: {variavel_escolhida}")

dados_variavel = df[variavel_escolhida].tolist()

st.subheader("Medidas Estatísticas")
st.write(f"Média: {ms.media(dados_variavel):.4f}")
st.write(f"Mediana: {ms.mediana(dados_variavel):.4f}")
st.write(f"Desvio Padrão: {ms.desvio_padrao(dados_variavel):.4f}")
st.write(f"Variância: {ms.variancia(dados_variavel):.4f}")