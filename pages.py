import streamlit as st

st.set_page_config(page_title="Estatística Interativa", layout="wide")

pagina_1 = st.Page("secoes/inicio.py", title="Início", default=True)
pagina_2 = st.Page("secoes/estatistica_descritiva.py", title="Estatística Descritiva")
pagina_3 = st.Page("secoes/probabilidade.py", title="Probabilidade e Simulação")
pagina_4 = st.Page("secoes/distribuicoes.py", title="Distribuições Teóricas")
pagina_5 = st.Page("secoes/regressao.py", title="Correlação e Regressão")

navegacao = st.navigation({
    "Visão Geral": [pagina_1],
    "Análises": [pagina_2, pagina_3, pagina_4, pagina_5],
})

navegacao.run()