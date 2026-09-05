import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson
import random
import sys
sys.path.append("src")
import minhastats as ms

st.title("Laboratório Estatístico Interativo — CS2 (Counter-Strike 2)")

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

colunas_categoricas = ["event_type", "decider_map", "winner"]

tipo_variavel = st.radio("Escolha o tipo de variável:", ["Numérica", "Categórica"])

if tipo_variavel == "Numérica":
    variavel_escolhida = st.selectbox("Escolha uma variável para analisar:", colunas_numericas)
else:
    variavel_escolhida = st.selectbox("Escolha uma variável para analisar:", colunas_categoricas)

st.write(f"Você escolheu: {variavel_escolhida}")

dados_variavel = df[variavel_escolhida].tolist()

if tipo_variavel == "Numérica":
    st.subheader("Tabela de Frequências")
    numero_classes = 8
    valor_minimo = min(dados_variavel)
    valor_maximo = max(dados_variavel)
    largura_classe = (valor_maximo - valor_minimo) / numero_classes

    classes = []
    frequencias = []

    for i in range(numero_classes):
        limite_inferior = valor_minimo + i * largura_classe
        limite_superior = valor_minimo + (i + 1) * largura_classe

        contagem = 0
        for valor in dados_variavel:
            if i == numero_classes - 1:
                if limite_inferior <= valor <= limite_superior:
                    contagem = contagem + 1
            else:
                if limite_inferior <= valor < limite_superior:
                    contagem = contagem + 1

        if i == numero_classes - 1:
            classes.append(f"[{limite_inferior:.4f} até {limite_superior:.4f}]")
        else:
            classes.append(f"[{limite_inferior:.4f} até {limite_superior:.4f})")

        frequencias.append(contagem)

    tabela_frequencias = pd.DataFrame({
        "Classe": classes,
        "Frequência": frequencias
    })

    st.dataframe(tabela_frequencias)

    st.subheader("Medidas de Tendência Central")
    st.write(f"Média: {ms.media(dados_variavel):.4f}")
    st.write(f"Mediana: {ms.mediana(dados_variavel):.4f}")
    st.write(f"Moda: {ms.moda(dados_variavel)}") # Moda retorna lista (exemplo: [1.65]) por isso não é necessário formatar

    st.subheader("Medidas de Dispersão")
    st.write(f"Amplitude: {ms.amplitude(dados_variavel):.4f}")
    st.write(f"Variância: {ms.variancia(dados_variavel):.4f}")
    st.write(f"Desvio Padrão: {ms.desvio_padrao(dados_variavel):.4f}")
    st.write(f"Coeficiente de Variação: {ms.coeficiente_variacao(dados_variavel):.2f}%") # Expresso em percentual

    st.subheader("Histograma")
    fig, ax = plt.subplots()
    ax.hist(dados_variavel, bins=numero_classes, edgecolor="black")
    ax.set_xlabel(variavel_escolhida)
    ax.set_ylabel("Frequência")

    st.pyplot(fig)

    st.subheader("Boxplot")
    fig2, ax2 = plt.subplots()
    ax2.boxplot(dados_variavel, vert=False)
    ax2.set_xlabel(variavel_escolhida)

    st.pyplot(fig2)

    st.subheader("Detecção de Outliers (Regra do IQR)")
    quartis_dados = ms.quartis(dados_variavel)
    q1 = quartis_dados["Q1"]
    q3 = quartis_dados["Q3"]
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    outliers = []

    for valor in dados_variavel:
        if valor < limite_inferior or valor > limite_superior:
            outliers.append(valor)

    st.write(f"Q1: {q1:.4f}")
    st.write(f"Q3: {q3:.4f}")
    st.write(f"IQR: {iqr:.4f}")
    st.write(f"Limite inferior: {limite_inferior:.4f}")
    st.write(f"Limite superior: {limite_superior:.4f}")
    st.write(f"Número de outliers encontrados: {len(outliers)}")

    st.subheader("Interpretação Automática")

    media_dados = ms.media(dados_variavel)
    mediana_dados = ms.mediana(dados_variavel)

    if media_dados > mediana_dados:
        interpretacao = "A distribuição apresenta assimetria positiva (à direita) com valores concentrados em faixas mais baixas e uma cauda se estendendo para valores altos."
    elif media_dados < mediana_dados:
        interpretacao = "A distribuição apresenta assimetria negativa (à esquerda) com valores concentrados em faixas mais altas e uma cauda se estendendo para valores baixos."
    else:
        interpretacao = "A distribuição é aproximadamente simétrica com média e mediana praticamente iguais."

    st.write(interpretacao)

    if len(outliers) > 0:
        st.write(f"Foram identificados {len(outliers)} outlier(s) nessa variável, o que pode indicar partidas com desempenho atípico.")
    else:
        st.write("Não foram identificados outliers nessa variável.")

else:
    st.subheader("Tabela de Frequências")

    contagem_categoricas = df[variavel_escolhida].value_counts()

    tabela_frequencias_cat = pd.DataFrame({
        "Categoria": contagem_categoricas.index,
        "Frequência": contagem_categoricas.values
    })

    st.dataframe(tabela_frequencias_cat)

    st.subheader("Gráfico de Barras")

    fig3, ax3 = plt.subplots()
    ax3.bar(contagem_categoricas.index, contagem_categoricas.values)
    ax3.set_xlabel(variavel_escolhida)
    ax3.set_ylabel("Frequência")

    if variavel_escolhida in ["decider_map"]:
        plt.setp(ax3.get_xticklabels(), rotation=45, ha="right") # rotaciona os rótulos eixo X = 45 e alinha cada um sob a barra correspondente evitando que nomes se sobreponham

    fig3.tight_layout() # redimensiona as margens internas do gráfico evitando que os rótulos rotacionados saiam da área visível

    st.pyplot(fig3)

st.divider()
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

fig4, ax4 = plt.subplots()
ax4.plot(range(1, numero_sorteios + 1), frequencias_relativas)
ax4.axhline(y=probabilidade_teorica, color="red", linestyle="--", label=f"Proporção real no dataset ({probabilidade_teorica:.4f})")
ax4.set_xlabel("Número de sorteios")
ax4.set_ylabel("Frequência relativa de 'team1' vencer")
ax4.legend()

st.pyplot(fig4)

st.write(f"Frequência relativa final: {frequencias_relativas[-1]:.4f}")
st.write(f"Proporção real no dataset: {probabilidade_teorica:.4f}")

st.subheader("Teorema Central do Limite")

variavel_tcl = st.selectbox("Escolha uma variável para o experimento:", colunas_numericas, key="tcl")
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

fig5, ax5 = plt.subplots()
ax5.hist(medias_amostrais, bins=30, edgecolor="black")
ax5.set_xlabel(f"Média amostral de {variavel_tcl}")
ax5.set_ylabel("Frequência")

st.pyplot(fig5)

st.write(f"Média das médias amostrais: {ms.media(medias_amostrais):.4f}")
st.write(f"Desvio Padrão das médias amostrais: {ms.desvio_padrao(medias_amostrais):.4f}")

st.divider()
st.title("Distribuições Teóricas")

st.subheader("Ajuste à Distribuição Normal")

variavel_dist = st.selectbox("Escolha uma variável para analisar:", colunas_numericas, key="dist_normal")
dados_dist = df[variavel_dist].tolist()

media_dist = ms.media(dados_dist)
desvio_dist = ms.desvio_padrao(dados_dist)

fig6, ax6 = plt.subplots()
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

st.pyplot(fig6)

st.write(f"Parâmetros estimados: Média = {media_dist:.4f}; Desvio Padrão = {desvio_dist:.4f}")

st.subheader("Ajuste à Distribuição de Poisson")

variavel_poisson = "score_team1"
dados_poisson = df[variavel_poisson].tolist()

lambda_estimado = ms.media(dados_poisson)

valores_possiveis = list(range(0, int(max(dados_poisson)) + 1))
probabilidades_teoricas = poisson.pmf(valores_possiveis, mu=lambda_estimado)

contagem_real = df[variavel_poisson].value_counts().sort_index()
frequencias_relativas_reais = contagem_real / len(dados_poisson)

fig7, ax7 = plt.subplots()
ax7.bar(contagem_real.index, frequencias_relativas_reais.values, alpha=0.6, label="Dados reais", edgecolor="black")
ax7.plot(valores_possiveis, probabilidades_teoricas, "o-", color="red", linewidth=2, label="Poisson teórica")
ax7.set_xlabel(variavel_poisson)
ax7.set_ylabel("Frequência relativa / Probabilidade")
ax7.legend()

st.pyplot(fig7)

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

st.divider()
st.title("Correlação e Regressão Linear")

variavel_x = st.selectbox("Escolha a variável X:", colunas_numericas, key="regressao_x")
dados_x = df[variavel_x].tolist()

variavel_y = st.selectbox("Escolha a variável Y:", colunas_numericas, key="regressao_y")
dados_y = df[variavel_y].tolist()

if variavel_x == variavel_y:
    st.warning("Escolha variáveis diferentes para X e Y.")
else:
    correlacao = ms.correlacao_pearson(dados_x, dados_y)
    st.write(f"Correlação de Pearson: {correlacao:.4f}")

    beta0, beta1 = ms.regressao_linear(dados_x, dados_y)

    st.write(f"Coeficiente β₀ (intercepto): {beta0:.4f}")
    st.write(f"Coeficiente β₁ (inclinação): {beta1:.4f}")

    # Cálculo do R² (coeficiente de determinação)
    r2 = ms.r_quadrado(dados_x, dados_y)
    if r2 is None:
        st.write("R²: indefinido (a variável Y possui variância zero).")
    else:
        st.write(f"R² (coeficiente de determinação): {r2:.4f}")

    if beta1 >= 0:
        st.write(f"Equação da reta: ŷ = {beta0:.4f} + {beta1:.4f}x")
    else:
        st.write(f"Equação da reta: ŷ = {beta0:.4f} - {abs(beta1):.4f}x")

    st.write("**Interpretação do coeficiente β₀:**")
    st.write(ms.interpretar_beta0(beta0, variavel_x, variavel_y))

    st.write("**Interpretação do coeficiente β₁:**")
    st.write(ms.interpretar_beta1(beta1, variavel_x, variavel_y))

    st.warning(ms.alerta_causalidade())

    st.subheader("Diagrama de Dispersão")

    fig8, ax8 = plt.subplots()
    ax8.scatter(dados_x, dados_y, alpha=0.4, label="Dados reais")

    x_reta = [min(dados_x), max(dados_x)]
    y_reta = [beta0 + beta1 * x_reta[0], beta0 + beta1 * x_reta[1]]
    ax8.plot(x_reta, y_reta, color="red", linewidth=2, label="Reta de regressão")

    ax8.set_xlabel(variavel_x)
    ax8.set_ylabel(variavel_y)
    ax8.legend()

    st.pyplot(fig8)

    st.subheader("Predição Interativa")

    valor_x_predicao = st.number_input(f"Digite um valor de {variavel_x} para prever {variavel_y}:", value=ms.media(dados_x))
    valor_y_previsto = beta0 + beta1 * valor_x_predicao

    st.write(f"Para {variavel_x} = {valor_x_predicao:.4f}, o valor previsto de {variavel_y} é: {valor_y_previsto:.4f}")