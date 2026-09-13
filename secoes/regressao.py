import streamlit as st
import matplotlib.pyplot as plt
from secoes.utils import carregar_dados, COLUNAS_NUMERICAS
from src import minhastats as ms

df = carregar_dados()

st.title("Correlação e Regressão Linear")

variavel_x = st.selectbox("Escolha a variável X:", COLUNAS_NUMERICAS, key="regressao_x")
dados_x = df[variavel_x].tolist()

variavel_y = st.selectbox("Escolha a variável Y:", COLUNAS_NUMERICAS, key="regressao_y")
dados_y = df[variavel_y].tolist()

if variavel_x == variavel_y:
    st.warning("Escolha variáveis diferentes para X e Y.")
else:
    correlacao = ms.correlacao_pearson(dados_x, dados_y)
    st.write(f"Correlação de Pearson: {correlacao:.4f}")

    beta0, beta1 = ms.regressao_linear(dados_x, dados_y)

    st.write(f"Coeficiente β₀ (intercepto): {beta0:.4f}")
    st.write(f"Coeficiente β₁ (inclinação): {beta1:.4f}")

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

    fig8, ax8 = plt.subplots(figsize=(6, 4))
    ax8.scatter(dados_x, dados_y, alpha=0.4, label="Dados reais")

    x_reta = [min(dados_x), max(dados_x)]
    y_reta = [beta0 + beta1 * x_reta[0], beta0 + beta1 * x_reta[1]]
    ax8.plot(x_reta, y_reta, color="red", linewidth=2, label="Reta de regressão")

    ax8.set_xlabel(variavel_x)
    ax8.set_ylabel(variavel_y)
    ax8.legend()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig8, use_container_width=False)

    st.subheader("Predição Interativa")

    valor_x_predicao = st.number_input(f"Digite um valor de {variavel_x} para prever {variavel_y}:", value=ms.media(dados_x))
    valor_y_previsto = beta0 + beta1 * valor_x_predicao

    st.write(f"Para {variavel_x} = {valor_x_predicao:.4f}, o valor previsto de {variavel_y} é: {valor_y_previsto:.4f}")