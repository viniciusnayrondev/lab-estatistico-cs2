import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson
from secoes.utils import carregar_dados, COLUNAS_NUMERICAS
from src import minhastats as ms

df = carregar_dados()

st.title("Distribuições Teóricas")

st.subheader("Ajuste à Distribuição Normal")

variavel_dist = st.selectbox("Escolha uma variável para analisar:", COLUNAS_NUMERICAS, key="dist_normal")
dados_dist = df[variavel_dist].tolist()

media_dist = ms.media(dados_dist)
desvio_dist = ms.desvio_padrao(dados_dist)

fig6, ax6 = plt.subplots(figsize=(6, 4))
ax6.hist(dados_dist, bins=30, density=True, edgecolor="black", alpha=0.6, label="Dados reais")

x_valores = []
valor_atual = min(dados_dist)
passo = (max(dados_dist) - min(dados_dist)) / 200
for i in range(200):
    x_valores.append(valor_atual)
    valor_atual = valor_atual + passo

y_valores = norm.pdf(x_valores, loc=media_dist, scale=desvio_dist)

ax6.plot(x_valores, y_valores, color="red", linewidth=2, label="Curva Normal teórica")
ax6.set_xlabel(variavel_dist)
ax6.set_ylabel("Densidade")
ax6.legend()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig6, use_container_width=False)

st.write(f"Parâmetros estimados: Média = {media_dist:.4f}; Desvio Padrão = {desvio_dist:.4f}")

st.subheader("Ajuste à Distribuição de Poisson")

variavel_poisson = "score_team1"
dados_poisson = df[variavel_poisson].tolist()

lambda_estimado = ms.media(dados_poisson)

valores_possiveis = list(range(0, int(max(dados_poisson)) + 1))
probabilidades_teoricas = poisson.pmf(valores_possiveis, mu=lambda_estimado)

contagem_real = df[variavel_poisson].value_counts().sort_index()
frequencias_relativas_reais = contagem_real / len(dados_poisson)

fig7, ax7 = plt.subplots(figsize=(6, 4))
ax7.bar(contagem_real.index, frequencias_relativas_reais.values, alpha=0.6, label="Dados reais", edgecolor="black")
ax7.plot(valores_possiveis, probabilidades_teoricas, "o-", color="red", linewidth=2, label="Poisson teórica")
ax7.set_xlabel(variavel_poisson)
ax7.set_ylabel("Frequência relativa / Probabilidade")
ax7.legend()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig7, use_container_width=False)

st.write(f"Parâmetro estimado: λ (lambda) = {lambda_estimado:.4f}")

st.write(
    "**Discussão do ajuste:** Observa-se um pico isolado em 13 rounds, não "
    "previsto pela curva teórica de Poisson. Isso ocorre porque, no CS2, um "
    "mapa é vencido diretamente ao atingir 13 rounds (formato MR12), sem "
    "necessidade de prorrogação. Picos adicionais em 16, 19 e 22 rounds "
    "correspondem a vitórias decididas em overtime (incrementos de 3 rounds "
    "por prorrogação). Essa estrutura de regras cria um teto e saltos "
    "discretos que a distribuição de Poisson — pensada para contagens de "
    "eventos livres e ilimitados — não consegue capturar. O ajuste "
    "visual, portanto, é fraco para essa variável, mas a discrepância "
    "revela uma característica estrutural real."
)