# Laboratório Estatístico Interativo — CS2 (Counter-Strike 2)

Trabalho de Sistematização da disciplina Matemática e Estatística para Computação.

Este projeto implementa um laboratório estatístico interativo, explorando um
dataset real de partidas profissionais de CS2 (Counter-Strike 2) com uma
biblioteca de funções estatísticas implementada do zero.

## Stack Utilizada

- Python
- Streamlit (interface interativa) — a ser implementado
- pandas / numpy / scipy (manipulação e validação de dados)
- pytest (testes automatizados) — a ser implementado

## Estrutura do projeto

    lab-estatistico-cs2/
    ├── app/                  # Aplicação Streamlit (ainda não iniciada)
    ├── data/
    │   ├── processed/         # Dataset limpo (ainda não gerado)
    │   └── raw/               # Dataset original (não versionado no Git)
    ├── src/
    │   └── prepare_data.py    # Módulo 0: leitura e limpeza dos dados
    ├── tests/                 # Testes automatizados (ainda não iniciados)
    └── .gitignore

## Fonte dos dados

**Dataset:** CS2 HLTV Professional Match Statistics Dataset

**Autor:** griffindesroches (Kaggle)

**URL:** https://www.kaggle.com/datasets/griffindesroches/cs2-hltv-professional-match-statistics-dataset

7.033 partidas profissionais de CS2 (maio/2024 a outubro/2025), 140 colunas
originais no arquivo bruto.

## Módulo 0 — Preparação dos Dados (completo)

### Seleção de colunas

Das 140 colunas originais, selecionou-se 19 relevantes para a análise:

- **Metadados:** match_id, date, tournament, team1_name, team2_name
- **Categóricas:** event_type, decider_map, winner
- **Numéricas:** team1_avg_RATING, team2_avg_RATING, rating_diff,
  team1_avg_ADR, team2_avg_ADR, team1_avg_KAST, team2_avg_KAST,
  team1_totalwinrate, team2_totalwinrate, score_team1, score_team2

### Tratamento de inconsistências

**Coluna `event_type`:** identificou-se, via `.value_counts()`, que a coluna
possuía 4 valores únicos em vez dos 2 esperados, devido a inconsistência de
capitalização:

| Valor original | Contagem |
|---|---|
| Online | 5.149 |
| LAN | 1.830 |
| online | 46 |
| lan | 8 |

Aplicou-se uma função de normalização (`normalizar_event_type`), que remove
espaços em branco e padroniza a capitalização, preservando "LAN"
(tratamento especial, visto que a capitalização padrão
do Python modificaria para "Lan"). Resultado esperado: apenas 2 categorias
(Online, LAN).

**Coluna `decider_map`:** identificou-se 63 linhas sem valor
registrado — partidas sem um mapa decisivo definido nos dados originais.
Essas linhas foram removidas via `dropna()` resultando em 6.970 partidas
no dataset final.

## Como executar o projeto

### Pré-requisitos

- Python 3.10 ou superior.

### Passos

1. Clone o repositório:

       git clone https://github.com/viniciusnayrondev/lab-estatistico-cs2.git
       cd lab-estatistico-cs2

2. Crie e ative um ambiente virtual:

       python -m venv .venv
       .venv\Scripts\Activate.ps1

3. Instale as dependências:

       pip install pandas

4. Execute o script de preparação dos dados:

       python src/prepare_data.py

O script gera `data/processed/cs2_matches_clean.csv`, o dataset limpo
usado pelo restante do projeto.

**Nota:** o dataset bruto (`data/raw/cs2_newestcombinedmatches.csv`) não é
versionado no Git (arquivo grande). Baixe do Kaggle (link acima) e coloque
manualmente em `data/raw/` antes de executar o script.

## Status do projeto

- [x] Módulo 0 — Dados Reais (completo: seleção de colunas, limpeza e dataset processado salvo)
- [ ] Módulo 1 — Núcleo Estatístico Próprio
- [ ] Módulo 2 — Estatística Descritiva Interativa
- [ ] Módulo 3 — Probabilidade e Simulação
- [ ] Módulo 4 — Distribuições Teóricas
- [ ] Módulo 5 — Correlação e Regressão Linear
- [ ] Módulo 6 — Relatório de Descobertas