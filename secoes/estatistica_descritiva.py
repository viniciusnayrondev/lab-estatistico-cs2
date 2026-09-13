import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from secoes.utils import carregar_dados, COLUNAS_NUMERICAS, COLUNAS_CATEGORICAS
from src import minhastats as ms

df = carregar_dados()

tipo_variavel = st.radio("Escolha o tipo de variável:", ["Numérica", "Categórica"])

if tipo_variavel == "Numérica":
    variavel_escolhida = st.selectbox("Escolha uma variável para analisar:", COLUNAS_NUMERICAS)
else:
    variavel_escolhida = st.selectbox("Escolha uma variável para analisar:", COLUNAS_CATEGORICAS)

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
    st.write(f"Moda: {ms.moda(dados_variavel)}")

    st.subheader("Medidas de Dispersão")
    st.write(f"Amplitude: {ms.amplitude(dados_variavel):.4f}")
    st.write(f"Variância: {ms.variancia(dados_variavel):.4f}")
    st.write(f"Desvio Padrão: {ms.desvio_padrao(dados_variavel):.4f}")
    st.write(f"Coeficiente de Variação: {ms.coeficiente_variacao(dados_variavel):.2f}%")

    st.subheader("Histograma")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(dados_variavel, bins=numero_classes, edgecolor="black")
    ax.set_xlabel(variavel_escolhida)
    ax.set_ylabel("Frequência")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig, use_container_width=False)

    st.subheader("Boxplot")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.boxplot(dados_variavel, vert=False)
    ax2.set_xlabel(variavel_escolhida)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig2, use_container_width=False)

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

    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.bar(contagem_categoricas.index, contagem_categoricas.values)
    ax3.set_xlabel(variavel_escolhida)
    ax3.set_ylabel("Frequência")

    if variavel_escolhida in ["decider_map"]:
        plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")

    fig3.tight_layout()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig3, use_container_width=False)