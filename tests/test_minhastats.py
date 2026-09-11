import sys
sys.path.append("src")
import minhastats as ms

import pytest
import numpy as np
from scipy import stats

TOLERANCIA = 0.0001

def test_media():
    dados = [2, 4, 6, 8, 10]
    resultado_proprio = ms.media(dados)
    resultado_numpy = np.mean(dados)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_mediana_impar():
    dados = [7, 2, 9, 4, 5]
    resultado_proprio = ms.mediana(dados)
    resultado_numpy = np.median(dados)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_mediana_par():
    dados = [1, 3, 5, 7]
    resultado_proprio = ms.mediana(dados)
    resultado_numpy = np.median(dados)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_moda():
    dados = [4, 8, 15, 4, 4, 8]
    resultado_proprio = ms.moda(dados)
    resultado_scipy = stats.mode(dados, keepdims=True).mode[0]
    assert resultado_scipy in resultado_proprio

def test_amplitude():
    dados = [4, 8, 15, 16, 23, 42]
    resultado_proprio = ms.amplitude(dados)
    resultado_numpy = np.ptp(dados)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_variancia_amostral():
    dados = [2, 4, 6, 8, 10]
    resultado_proprio = ms.variancia(dados, amostral=True)
    resultado_numpy = np.var(dados, ddof=1)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_variancia_populacional():
    dados = [2, 4, 6, 8, 10]
    resultado_proprio = ms.variancia(dados, amostral=False)
    resultado_numpy = np.var(dados, ddof=0)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_desvio_padrao_amostral():
    dados = [2, 4, 6, 8, 10]
    resultado_proprio = ms.desvio_padrao(dados, amostral=True)
    resultado_numpy = np.std(dados, ddof=1)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_desvio_padrao_populacional():
    dados = [2, 4, 6, 8, 10]
    resultado_proprio = ms.desvio_padrao(dados, amostral=False)
    resultado_numpy = np.std(dados, ddof=0)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_coeficiente_variacao():
    dados = [2, 4, 6, 8, 10]
    resultado_proprio = ms.coeficiente_variacao(dados)
    resultado_numpy = (np.std(dados, ddof=1) / np.mean(dados)) * 100
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_percentil():
    dados = [10, 20, 30, 40, 50]
    resultado_proprio = ms.percentil(dados, 25)
    resultado_numpy = np.percentile(dados, 25)
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_quartis():
    dados = [10, 20, 30, 40, 50]
    resultado_proprio = ms.quartis(dados)
    assert resultado_proprio["Q1"] == pytest.approx(np.percentile(dados, 25), abs=TOLERANCIA)
    assert resultado_proprio["Q2"] == pytest.approx(np.percentile(dados, 50), abs=TOLERANCIA)
    assert resultado_proprio["Q3"] == pytest.approx(np.percentile(dados, 75), abs=TOLERANCIA)

def test_covariancia():
    dados_x = [1, 2, 3, 4, 5]
    dados_y = [2, 4, 6, 8, 10]
    resultado_proprio = ms.covariancia(dados_x, dados_y)
    resultado_numpy = np.cov(dados_x, dados_y, ddof=1)[0][1]
    assert resultado_proprio == pytest.approx(resultado_numpy, abs=TOLERANCIA)

def test_correlacao_pearson():
    dados_x = [1, 2, 3, 4, 5]
    dados_y = [2, 4, 6, 8, 10]
    resultado_proprio = ms.correlacao_pearson(dados_x, dados_y)
    resultado_scipy, _ = stats.pearsonr(dados_x, dados_y)
    assert resultado_proprio == pytest.approx(resultado_scipy, abs=TOLERANCIA)

def test_regressao_linear():
    dados_x = [1, 2, 3, 4, 5]
    dados_y = [2, 4, 6, 8, 10]
    beta0_proprio, beta1_proprio = ms.regressao_linear(dados_x, dados_y)

    resultado_scipy = stats.linregress(dados_x, dados_y)

    assert beta1_proprio == pytest.approx(resultado_scipy.slope, abs=TOLERANCIA)
    assert beta0_proprio == pytest.approx(resultado_scipy.intercept, abs=TOLERANCIA)

def test_r_quadrado():
    dados_x = [1, 2, 3, 4, 5]
    dados_y = [2, 4, 6, 8, 10]
    resultado_proprio = ms.r_quadrado(dados_x, dados_y)

    resultado_scipy = stats.linregress(dados_x, dados_y)
    r2_scipy = resultado_scipy.rvalue ** 2

    assert resultado_proprio == pytest.approx(r2_scipy, abs=TOLERANCIA)