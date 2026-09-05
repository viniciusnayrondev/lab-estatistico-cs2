# Laboratório Estatístico Interativo — CS2 (Counter-Strike 2)

Sistematização da disciplina Matemática e Estatística para Computação.

Este projeto implementa um laboratório estatístico interativo, explorando um
dataset real de partidas profissionais de CS2 (Counter-Strike 2) com uma
biblioteca de funções estatísticas implementada do zero.

## Stack Utilizada

- Python
- Streamlit (interface interativa)
- matplotlib (visualização de dados)
- pandas / numpy / scipy (manipulação e validação de dados)
- pytest (testes automatizados) — a ser implementado

## Estrutura do projeto

    lab-estatistico-cs2/
    ├── app/
    │   └── app.py             # Aplicação Streamlit (Módulos 2, 3 e 4)
    ├── data/
    │   ├── processed/         # Dataset limpo (gerado por prepare_data.py)
    │   └── raw/               # Dataset original (não versionado no Git)
    ├── src/
    │   ├── prepare_data.py    # Módulo 0: leitura e limpeza dos dados
    │   └── minhastats.py      # Módulo 1: biblioteca estatística própria
    ├── tests/                 # Testes automatizados (ainda não iniciados)
    └── .gitignore

## Fonte dos dados

**Dataset:** CS2 HLTV Professional Match Statistics Dataset

**Autor:** griffindesroches (Kaggle)

**URL:** https://www.kaggle.com/datasets/griffindesroches/cs2-hltv-professional-match-statistics-dataset

7.033 partidas profissionais de CS2 (maio/2024 a outubro/2025), 140 colunas
originais no arquivo bruto (reduzido a 6.969 partidas e 19 colunas após a
limpeza descrita no Módulo 0).

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

**Colunas `team2_avg_RATING`, `team2_avg_ADR`, `team2_avg_KAST`:** identificada
1 linha (partida `hltv_match_2377790`) com valores ausentes simultaneamente
nas três colunas, causando ausência em `rating_diff` (calculado a
partir de `team2_avg_RATING`). A linha foi removida por `dropna()`,
resultando em 6.969 partidas no dataset final (de 6.970 após etapa
anterior).

## Módulo 1 — Núcleo Estatístico Próprio (completo)

Biblioteca `src/minhastats.py`, implementada do zero (sem uso de funções
prontas de estatística do pandas/numpy/scipy), contendo:

- Medidas de tendência central: `media()`, `mediana()`, `moda()`
- Medidas de dispersão: `amplitude()`, `variancia()` e `desvio_padrao()`
  (amostral e populacional), `coeficiente_variacao()`
- Posição: `percentil()` e `quartis()` (Q1, Q2, Q3)
- Relação entre variáveis: `covariancia()` e `correlacao_pearson()`

Cada função foi validada com conjuntos de dados de exemplo.

Os testes de validação ficam protegidos por
`if __name__ == "__main__":` garantindo que só executem quando o arquivo é
executado diretamente (`python src/minhastats.py`) e não quando é importado
por outro módulo (como `app/app.py`) — evitando poluir o log de execução da
aplicação Streamlit com prints de teste irrelevantes.

## Módulo 2 — Estatística Descritiva Interativa (completo)

Aplicação Streamlit (`app/app.py`) que permite ao usuário escolher o tipo
de variável (numérica ou categórica) e, em seguida, a variável específica
a ser analisada dentro do dataset.

### Para variáveis numéricas

- **Tabela de frequências**: dados agrupados em 8 classes (faixas de
  valores), calculadas a partir da amplitude dos dados
- **Medidas de tendência central**: média, mediana e moda
- **Medidas de dispersão**: amplitude, variância, desvio padrão e
  coeficiente de variação
- **Histograma**: distribuição visual dos dados por classe
- **Boxplot**: visualização dos quartis e possíveis valores extremos
- **Detecção de outliers**: aplicação da regra do IQR
  (limites em Q1 − 1.5 × IQR e Q3 + 1.5 × IQR)
- **Interpretação automática**: identifica a assimetria da distribuição
  (comparando média e mediana) e comenta a presença de outliers

### Para variáveis categóricas

- **Tabela de frequências**: contagem de ocorrências de cada categoria
  (via `.value_counts()`)
- **Gráfico de barras**: frequência de cada categoria, com rotação dos
  rótulos do eixo X quando necessário (ex.: nomes de mapas em `decider_map`)

### Observação

Todas as medidas estatísticas exibidas são calculadas pela biblioteca
própria `minhastats.py` (Módulo 1).

## Módulo 3 — Probabilidade e Simulação (completo)

Dois experimentos de simulação de Monte Carlo incluídos na aplicação
Streamlit com parâmetros controláveis pelo usuário (sliders):

### Lei dos Grandes Números

Sorteios repetidos (com reposição) do histórico real de vencedores
(`winner`) do dataset, calculando a frequência relativa acumulada de
vitórias de 'team1' a cada sorteio. Demonstra a convergência dessa
frequência para a proporção real observada no dataset completo, conforme
o número de sorteios aumenta.

### Teorema Central do Limite

Sorteio repetido de amostras (com reposição) de uma variável numérica
selecionada pelo usuário, calculando a média de cada amostra. A distribuição
dessas médias amostrais (visualizada em histograma) se aproxima de uma
distribuição Normal conforme o tamanho de cada amostra aumenta — mesmo
quando a variável original não segue uma distribuição normal.

## Módulo 4 — Distribuições Teóricas (completo)

Aplicação Streamlit sobrepõe, ao histograma de uma variável escolhida, a
curva de uma distribuição teórica candidata, com parâmetros estimados a
partir dos dados reais (usando a biblioteca própria `minhastats.py`).

### Distribuição Normal

Aplicada a qualquer variável numérica selecionável pelo usuário. Parâmetros
estimados: média (`ms.media()`) e desvio padrão (`ms.desvio_padrao()`). A
curva teórica é gerada com `scipy.stats.norm.pdf()`.

### Distribuição de Poisson

Aplicada à variável `score_team1`. Parâmetro estimado: λ (lambda), igual à
média dos dados. A curva teórica é gerada com `scipy.stats.poisson.pmf()`.

**Descoberta relevante:** o ajuste visual à Poisson é fraco para essa
variável. Observa-se um pico isolado em 13 rounds, não previsto pela
distribuição teórica — isso ocorre porque, no CS2, um mapa é vencido
diretamente ao atingir 13 rounds (formato MR12), sem necessidade de
prorrogação. Picos adicionais em 16, 19 e 22 rounds correspondem a vitórias
decididas em overtime (incrementos de 3 rounds por prorrogação). Essa
estrutura de regras cria um teto (13 rounds) e saltos discretos
que a distribuição de Poisson — pensada para contagens de eventos livres e
ilimitados — não consegue capturar. A discrepância entre dados reais e
curva teórica revela, portanto, uma característica estrutural real do 
CS2, não um problema de qualidade dos dados.

## Módulo 5 — Correlação e Regressão Linear (completo)

Aplicação Streamlit permite ao usuário escolher duas variáveis numéricas
(X e Y) e exibe:

- **Coeficiente de correlação de Pearson** (biblioteca própria)
- **Regressão linear simples**: coeficientes β₀ (intercepto) e β₁
  (inclinação), calculados pelo método dos mínimos quadrados,
  implementado do zero em `minhastats.py` (`regressao_linear()`)
- **R² (coeficiente de determinação)**, calculado pela definição formal
  (1 − soma dos resíduos / soma total), com proteção contra divisão por
  zero quando a variável Y tem variância nula
- **Equação da reta**, formatada com o sinal correto do coeficiente
  angular
- **Diagrama de dispersão** com a reta de regressão sobreposta
- **Predição interativa**: o usuário digita um valor de X e a aplicação
  calcula o Ŷ previsto
- **Interpretação textual** dos coeficientes β₀ e β₁, gerada por funções
  próprias (`interpretar_beta0()`, `interpretar_beta1()`)
- **Alerta explícito**: correlação e regressão não comprovam causalidade
  (`alerta_causalidade()`)

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

       pip install pandas streamlit matplotlib scipy

4. Execute o script de preparação dos dados:

       python src/prepare_data.py

O script gera `data/processed/cs2_matches_clean.csv`, o dataset limpo
usado pelo restante do projeto.

5. Execute a aplicação Streamlit:

       streamlit run app/app.py

**Nota:** o dataset bruto (`data/raw/cs2_newestcombinedmatches.csv`) não é
versionado no Git (arquivo grande). Baixe do Kaggle (link acima) e coloque
manualmente em `data/raw/` antes de executar o script.

## Status do projeto

- [x] Módulo 0 — Dados Reais (completo: seleção de colunas, limpeza e dataset processado salvo)
- [x] Módulo 1 — Núcleo Estatístico Próprio
- [x] Módulo 2 — Estatística Descritiva Interativa
- [x] Módulo 3 — Probabilidade e Simulação
- [x] Módulo 4 — Distribuições Teóricas
- [x] Módulo 5 — Correlação e Regressão Linear
- [ ] Módulo 6 — Relatório de Descobertas