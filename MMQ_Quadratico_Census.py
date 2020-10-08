# -*- coding: utf-8 -*-
"""
@author: Andrey Ferreira de Almeida
"""

#bibliotecas
import pandas as pd

#importo a base de dados
db = pd.read_csv('datasets/US-Census.txt', header = None, delim_whitespace = True, names=['Ano','Valor'])

#crio uma coluna com os valores da variavel dependente elevado ao quadrado
db['x2'] = db['Ano'] ** 2

#crio uma coluna com os valores da variavel dependente quadratica (x * x)
db['xx'] = db['Ano'] * db['Ano'] 

#crio uma coluna com a multiplicacao dos valores da variavel dependente e independente
db['xy'] = db['Ano'] * db['Valor']

#crio uma coluna que multiplica x por x*x
db['x1x2'] = db['Ano'] * db['xx']

#crio uma coluna com os valores da variavel dependente elevado ao quadrado
db['xx2'] = db['xx'] ** 2

#crio uma coluna com a multiplicacao dos valores da variavel dependente e independente
db['xxy'] = db['xx'] * db['Valor']

#quantidade de registros na base
n = float(db.shape[0])

#somatoria dos valores de x (variavel dependente)
sx = float(db['Ano'].sum())

#somatoria dos valores de x^2
sx2 = float(db['x2'].sum())

#somatoria dos valores quadraticos x * x
sxx = float(db['xx'].sum())

#somatoria dos valores de x1 e x2
sx1x2 = float(db['x1x2'].sum())

#somatoria dos valores de x2 ^2
sxx2 = float(db['xx2'].sum())

#somatoria dos valores de y (variavel independente)
sy = float(db['Ano'].sum())

#somatoria da multiplicacao das variaveis x e y
sxy = float(db['xy'].sum())

#somatoria da multiplicacao das variaveis xx e y
sxxy = float(db['xxy'].sum())

#crio a minha matriz (3x3) com as minhas variaveis de trabalho (informadas) 
M = pd.DataFrame([[n, sx, sxx],[sx, sx2, sx1x2],[sxx, sx1x2, sxx2]])[:].values

#crio uma matriz (2x1) com as minhas variaveis de trabalho (esperadas)
N = pd.DataFrame([[sy],[sxy],[sxxy]])[:].values

#calculo a determinante da matriz
det = (((M[0][0] * M[1][1] * M[2][2]) + \
        (M[0][1] * M[1][2] * M[2][0]) + \
        (M[0][2] * M[1][0] * M[2][1])) - \
        ((M[0][2] * M[1][1] * M[2][0]) + \
         (M[0][0] * M[1][2] * M[2][1]) + \
         (M[0][1] * M[1][0] * M[2][2])))

#cria a matriz adjunta
MA = [[(M[1][1] * M[2][2])-(M[1][2] * M[2][1]),(M[2][1] * M[0][2])-(M[2][2] * M[0][1]),(M[0][1] * M[1][2])-(M[0][2] * M[1][1])], \
       [(M[1][2] * M[2][0])-(M[1][0] * M[2][2]),(M[2][0] * M[0][2])-(M[2][2] * M[0][0]),(M[0][2] * M[1][0])-(M[0][0] * M[1][2])], \
       [(M[1][0] * M[2][1])-(M[1][1] * M[2][0]),(M[2][0] * M[0][1])-(M[2][1] * M[0][0]),(M[0][0] * M[1][1])-(M[0][1] * M[1][0])]]

#cria a matriz inversa
I = pd.DataFrame([[MA[0][0]/det, MA[0][1]/det, MA[0][2]/det], \
     [MA[1][0]/det, MA[1][1]/det, MA[1][2]/det], \
     [MA[2][0]/det, MA[2][1]/det, MA[2][2]/det]])[:].values

#cria a matriz com zeros (será populada com o resultado da multiplicacao da matriz inversa com a matriz 3x1)
F = [[0 for a in range(N.shape[1])] for b in range(N.shape[0])]

#realizo a multiplicacao dessas matrizes e crio uma matriz final (3x1) com os valores de Beta 0, Beta 1 e Beta 2
for i in range(len(I)):
    for j in range(len(N[0])):
        for k in range(len(N)):
            F[i][j] += I[i][k] * N[k][j]

#formato a minha saida para float (3x1)
F = pd.DataFrame(F)[:].values

#crio um método de predicao
def predicao(ano):
    #crio uma matriz (1x3) com o valor do viés e o valor informado
    A = pd.DataFrame([[1, ano, ano * ano]])[:].values
    
    #a saída será a multiplicacao da matriz com o vies e o valor informado com o valor final de Beta 0, Beta 1 e Beta 2
    return ((A[0][0] * F[0][0]) + (A[0][1] * F[1][0]) + (A[0][2] * F[2][0]))

#TESTE
#Qual o valor de censo para a temperatura de 200 F?
print('O valor de censo predito é : %.2f' %(predicao(2010)))
