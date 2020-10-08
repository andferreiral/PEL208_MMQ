# -*- coding: utf-8 -*-
"""
@author: Andrey Ferreira de Almeida
"""

#bibliotecas
import pandas as pd
import math

#importo a base de dados
db = pd.read_csv('datasets/US-Census.txt', header = None, delim_whitespace = True, names=['Ano','Valor'])

#crio uma coluna com os valores da variavel dependente elevado ao quadrado
db['x2'] = db['Ano'] ** 2

#crio uma coluna com a multiplicacao dos valores da variavel dependente e independente
db['xy'] = db['Ano'] * db['Valor']

#quantidade de registros na base
n = db.shape[0]

#somatoria dos valores de x (variavel dependente)
sx = db['Ano'].sum()

#somatoria dos valores de x^2
sx2 = db['x2'].sum()

#somatoria dos valores de y (variavel independente)
sy = db['Valor'].sum()

#somatoria da multiplicacao das variaveis x e y
sxy = db['xy'].sum()

#crio a minha matriz (2x2) com as minhas variaveis de trabalho (informadas) 
M = pd.DataFrame([[n, sx],[sx, sx2]])[:].values

#crio uma matriz (2x1) com as minhas variaveis de trabalho (esperadas)
N = pd.DataFrame([[sy],[sxy]])[:].values

#calculo a determinante da minha matriz (2x2)
det = 1 / ((M[0][0] * M[1][1])-(M[0][1] * M[1][0]))

#calculo a matriz inversa da matriz com os valores informados (utilizando a determinante)
I =[[M[1][1] * det, (M[0][1] * -1) * det],[(M[1][0] * -1) * det, M[0][0] * det]]

#formato a minha saida para float (2x2)
I = pd.DataFrame(I)[:].values 

#cria a matriz com zeros (será populada com o resultado da multiplicacao da matriz inversa com a matriz 2x1)
F = [[0 for a in range(N.shape[1])] for b in range(N.shape[0])]

#realizo a multiplicacao dessas matrizes e crio uma matriz final (2x1) com os valores de Beta 0 e Beta 1
for i in range(len(I)):
    for j in range(len(N[0])):
        for k in range(len(N)):
            F[i][j] += I[i][k] * N[k][j]

#formato a minha saida para float (2x1)
F = pd.DataFrame(F)[:].values

#calculo o valor do peso
#media
media = sx / n

#somo todas as linhas, subtraio a media e elevo ao quadrado
somatoria = 0

for i in range(len(db['Valor'])):
    somatoria += (db['Valor'][i] - media) ** 2
    
#a partir do resultado anrerior eu tiro a raiz quadrada
desviopadrao = math.sqrt(somatoria/n)

#divido 1 sobre o valor do desvio padrão calculado
peso = abs(1 / desviopadrao)

#crio um método de predicao
def predicao(ano):
    #crio uma matriz (1x2) com o valor do viés e o valor informado
    A = pd.DataFrame([[peso, ano]])[:].values
    #a saída será a multiplicacao da matriz com o vies e o valor informado com o valor final de Beta 0 e Beta 1
    return ((A[0][0] * F[0][0]) + (A[0][1] * F[1][0]))

#TESTE
#Qual o valor de censo para a temperatura de 200 F?
print('O valor do censo predito é : %.2f' %(predicao(2010)))
