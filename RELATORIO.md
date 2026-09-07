# Relatório de Descobertas — Laboratório Estatístico CS2

## Introdução

Este relatório apresenta as três descobertas estatísticas mais relevantes
identificadas ao longo do desenvolvimento do Laboratório Estatístico
Interativo, com base na análise de 6.969 partidas profissionais de CS2
(Counter-Strike 2). Todas as medidas foram calculadas pela biblioteca
estatística própria (`src/minhastats.py`), sem uso de funções do
pandas/numpy/scipy para os cálculos exibidos.

## Descoberta 1 — O Rating profissional tem dispersão extremamente baixa

Ao analisar a variável `team1_avg_RATING` no Módulo 2 (Estatística
Descritiva), observou-se:

- Q1 = 1.0400, Q3 = 1.0900, IQR = 0.0500
- Faixa completa dos dados: 0.81 a 1.17

O IQR de apenas 0.05 é extremamente pequeno diante da escala natural do
Rating. Isso faz com que a regra padrão de detecção de outliers
(1.5 × IQR) resulte em limites muito apertados (0.965 a 1.165),
classificando 219 partidas (cerca de 3% do dataset) como estatisticamente
atípicas — mesmo quando os valores individuais (como 0.92 ou 0.96)
pareceriam normais a uma inspeção visual rápida.

**Interpretação:** o Rating profissional de CS2 é uma métrica bastante
homogênea entre os times de elite, o que é esperado — jogadores
profissionais tendem a ter desempenho consistentemente próximo da média
do cenário competitivo. A baixa dispersão é, portanto, um reflexo real do
alto nível competitivo da cena profissional, não um problema nos dados.

## Descoberta 2 — O placar de partidas revela a mecânica de regras do CS2

Ao tentar ajustar a distribuição de Poisson à variável `score_team1`
(Módulo 4), observou-se um ajuste visualmente fraco: um pico isolado em
13 rounds, seguido de saltos discretos em 16, 19 e 22 rounds — um padrão
que a curva teórica de Poisson não prevê.

Investigando a causa, confirmou-se que essa distribuição reflete
diretamente as regras do jogo:

- 13 rounds = vitória direta de mapa, no formato MR12 (sem prorrogação)
- 16, 19, 22 rounds = vitórias decididas em overtime, que soma blocos de
  3 rounds extras por prorrogação

**Interpretação:** a distribuição de Poisson pressupõe eventos de
contagem livre e ilimitada, mas o placar de CS2 tem um "teto" estrutural
(o mapa termina ao atingir 13 rounds) e saltos artificiais causados pelo
sistema de overtime. Esse é um exemplo de como um ajuste estatístico
"ruim" pode revelar, de forma legítima, uma característica estrutural
real do fenômeno estudado — nesse caso, as próprias regras do jogo.

## Descoberta 3 — Rating e ADR possuem forte relação linear positiva

Utilizando o Módulo 5 (Correlação e Regressão Linear), analisou-se a
relação entre `team1_avg_RATING` (X) e `team1_avg_ADR` (Y):

- Correlação de Pearson: r = 0,8767
- Equação da reta: ŷ = 26,6632 + 45,2687x
- R² = 0,7687

**Interpretação:** existe uma relação linear forte e positiva entre o
Rating de um time e seu dano médio por rodada (ADR) — aproximadamente
77% da variação do ADR é explicada pela variação do Rating através dessa
reta. Isso é estatisticamente esperado, já que o ADR é um dos componentes
que compõem o cálculo do próprio Rating no HLTV. **Importante ressaltar
(conforme discutido na própria aplicação): essa correlação não implica
causalidade** — não é correto afirmar que "ter Rating alto causa ADR
alto"; a relação decorre da forma como as duas métricas são calculadas e
de padrões reais de desempenho competitivo.

## Considerações finais

As três descobertas acima demonstram como ferramentas estatísticas
simples — quartis, ajuste de distribuições teóricas e regressão linear —
podem revelar tanto características do desempenho competitivo (achados 1
e 3) quanto da própria mecânica de regras do jogo (achado 2), quando
aplicadas com cuidado interpretativo sobre dados reais.