import streamlit as st
import matplotlib.pyplot as plt
import random
from secoes.utils import carregar_dados, COLUNAS_NUMERICAS
from src import minhastats as ms

df = carregar_dados()

st.title("Probabilidade e Simulação")

st.subheader("Lei dos Grandes Números")

vencedores = df["winner"].tolist()
probabilidade_teorica = vencedores.count("team1") / len(vencedores)

numero_sorteios = st.slider("Número de sorteios de partidas:", min_value=10, max_value=5000, value=1000)

contagem_team1 = 0
frequencias_relativas = []

for i in range(numero_sorteios):
    partida_sorteada = random.choice(vencedores)

    if partida_sorteada == "team1":
        contagem_team1 = contagem_team1 + 1

    frequencia_atual = contagem_team1 / (i + 1)
    frequencias_relativas.append(frequencia_atual)

fig4, ax4 = plt.subplots(figsize=(6, 4))
ax4.plot(range(1, numero_sorteios + 1), frequencias_relativas)
ax4.axhline(y=probabilidade_teorica, color="red", linestyle="--", label=f"Proporção real no dataset ({probabilidade_teorica:.4f})")
ax4.set_xlabel("Número de sorteios")
ax4.set_ylabel("Frequência relativa de 'team1' vencer")
ax4.legend()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig4, use_container_width=False)

st.write(f"Frequência relativa final: {frequencias_relativas[-1]:.4f}")
st.write(f"Proporção real no dataset: {probabilidade_teorica:.4f}")

st.subheader("Teorema Central do Limite")

variavel_tcl = st.selectbox("Escolha uma variável para o experimento:", COLUNAS_NUMERICAS, key="tcl")
dados_tcl = df[variavel_tcl].tolist()

tamanho_amostra = st.slider("Tamanho de cada amostra:", min_value=5, max_value=200, value=30)
numero_repeticoes = st.slider("Número de repetições (amostras sorteadas):", min_value=100, max_value=5000, value=1000)

medias_amostrais = []

for i in range(numero_repeticoes):
    amostra = []
    for j in range(tamanho_amostra):
        valor_sorteado = random.choice(dados_tcl)
        amostra.append(valor_sorteado)

    media_amostra = ms.media(amostra)
    medias_amostrais.append(media_amostra)

fig5, ax5 = plt.subplots(figsize=(6, 4))
ax5.hist(medias_amostrais, bins=30, edgecolor="black")
ax5.set_xlabel(f"Média amostral de {variavel_tcl}")
ax5.set_ylabel("Frequência")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig5, use_container_width=False)

st.write(f"Média das médias amostrais: {ms.media(medias_amostrais):.4f}")
st.write(f"Desvio Padrão das médias amostrais: {ms.desvio_padrao(medias_amostrais):.4f}")