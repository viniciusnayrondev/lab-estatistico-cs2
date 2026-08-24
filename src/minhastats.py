def media(dados):
    soma = sum(dados)
    quantidade = len(dados)
    return soma / quantidade

def mediana(dados):
    dados_ordenados = sorted(dados)
    quantidade = len(dados_ordenados)
    meio = quantidade // 2

    if quantidade % 2 == 1: # Ímpar?
        return dados_ordenados[meio]
    else:
        valor1 = dados_ordenados[meio - 1]
        valor2 = dados_ordenados[meio]
        return (valor1 + valor2) / 2

def moda(dados):
    contagem = {}
    for valor in dados:
        if valor in contagem:
            contagem[valor] = contagem[valor] + 1
        else:
            contagem[valor] = 1

    frequencia_maxima = max(contagem.values())
    modas = []
    for valor, frequencia in contagem.items():
        if frequencia == frequencia_maxima:
            modas.append(valor)

    return modas

def amplitude(dados):
    return max(dados) - min(dados)

def variancia(dados, amostral=True):
    media_dados = media(dados) # calcula x̄ (média)
    soma_quadrados = 0
    for valor in dados: # percorre cada xᵢ
        soma_quadrados = soma_quadrados + (valor - media_dados) ** 2
        # calcula (xᵢ - x̄)² e somatório (Σ)

    if amostral:
        divisor = len(dados) - 1 # n - 1 (amostral)
    else:
        divisor = len(dados) # n (populacional)

    return soma_quadrados / divisor

def desvio_padrao(dados, amostral=True):
    return variancia(dados, amostral) ** 0.5

def percentil(dados, p):
    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)
    posicao = (p / 100) * (n - 1)

    posicao_inteira = int(posicao)
    parte_decimal = posicao - posicao_inteira

    if posicao_inteira + 1 < n:
        valor_menor = dados_ordenados[posicao_inteira]
        valor_maior = dados_ordenados[posicao_inteira + 1]
        return valor_menor + parte_decimal * (valor_maior - valor_menor)
    else:
        return dados_ordenados[posicao_inteira]

def quartis(dados):
    q1 = percentil(dados, 25)
    q2 = percentil(dados, 50)
    q3 = percentil(dados, 75)
    return {"Q1": q1, "Q2": q2, "Q3": q3}

def coeficiente_variacao(dados):
    return (desvio_padrao(dados) / media(dados)) * 100

def covariancia(dados_x, dados_y):
    media_x = media(dados_x) # x̄
    media_y = media(dados_y) # ȳ

    soma_produtos = 0
    for i in range(len(dados_x)):
        soma_produtos = soma_produtos + (dados_x[i] - media_x) * (dados_y[i] - media_y)
        # calcula (xᵢ - x̄)(yᵢ - ȳ) e somatório (Σ)
    
    divisor = len(dados_x) - 1 # n - 1
    return soma_produtos / divisor

def correlacao_pearson(dados_x, dados_y):
    cov = covariancia(dados_x, dados_y)
    desvio_x = desvio_padrao(dados_x)
    desvio_y = desvio_padrao(dados_y)
    return cov / (desvio_x * desvio_y)

numeros = [2, 4, 6, 8, 10]
resultado = media(numeros)
print("Média:", resultado)

numeros_impar = [7, 2, 9, 4, 5]
print("Mediana (ímpar):", mediana(numeros_impar))

numeros_par = [1, 3, 5, 7]
print("Mediana (par):", mediana(numeros_par))

numeros_moda = [4, 8, 15, 4, 4, 8]
print("Moda:", moda(numeros_moda))

numeros_moda_empate = [1, 1, 2, 2, 3]
print("Moda (empate):", moda(numeros_moda_empate))

numeros_amplitude = [4, 8, 15, 16, 23, 42]
print("Amplitude:", amplitude(numeros_amplitude))

numeros_variancia = [2, 4, 6, 8, 10]
print("Variância (amostral):", variancia(numeros_variancia))
print("Variância (populacional):", variancia(numeros_variancia, amostral=False))

print("Desvio padrão (amostral):", desvio_padrao(numeros_variancia))
print("Desvio padrão (populacional):", desvio_padrao(numeros_variancia, amostral=False))

numeros_percentil = [10, 20, 30, 40, 50]
print("Percentil 25:", percentil(numeros_percentil, 25))
print("Percentil 10:", percentil(numeros_percentil, 10))

resultado_quartis = quartis(numeros_percentil)
print("Quartis:", resultado_quartis)

print("Coeficiente de variação:", coeficiente_variacao(numeros_variancia))

dados_x = [1, 2, 3, 4, 5]
dados_y = [2, 4, 6, 8, 10]
print("Covariância:", covariancia(dados_x, dados_y))

print("Correlação de Pearson:", correlacao_pearson(dados_x, dados_y))