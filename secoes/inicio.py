import streamlit as st
from secoes.utils import carregar_dados

df = carregar_dados()

st.title("Laboratório Estatístico Interativo — CS2 (Counter-Strike 2)")
st.write("Dataset carregado com sucesso!")
st.write(f"Número de partidas: {len(df)}")