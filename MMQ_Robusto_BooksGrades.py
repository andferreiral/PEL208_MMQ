#bibliotecas
import pandas as pd
import math

#importo a base de dados
db = pd.read_csv('datasets/Books_attend_grade.txt', header = None, delim_whitespace = True, names=['Books','Attend','Grade'])

#crio uma coluna com os valores da variavel dependente elevado ao quadrado
db['x2'] = db['Books'] ** 2

#crio uma coluna com os valores da variavel dependente elevado ao quadrado
db['xx2'] = db['Attend'] ** 2

#crio uma coluna com a multiplicacao dos valores da variavel dependente e independente
db['xy'] = db['Books'] * db['Grade']

#crio uma coluna com a multiplicacao dos valores da variavel dependente e independente
db['xxy'] = db['Attend'] * db['Grade']

#crio uma coluna que multiplica x por x*x
db['x1x2'] = db['Books'] * db['Attend']

#quantidade de registros na base
n = float(db.shape[0])

#somatoria dos valores de x (variavel dependente)
sx = float(db['Books'].sum())

#somatoria dos valores de x^2
sx2 = float(db['x2'].sum())

#somatoria dos valores de Attend
sxx = float(db['Attend'].sum())

#somatoria dos valores de x1 e x2
sx1x2 = float(db['x1x2'].sum())

#somatoria dos valores de x2 ^2
sxx2 = float(db['xx2'].sum())

#somatoria dos valores de y (variavel independente)
sy = float(db['Grade'].sum())

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

#calculo o valor do peso
#media
media = sx / n

#somo todas as linhas, subtraio a media e elevo ao quadrado
somatoria = 0

for i in range(len(db['Grade'])):
    somatoria += (db['Grade'][i] - media) ** 2
    
#a partir do resultado anrerior eu tiro a raiz quadrada
desviopadrao = math.sqrt(somatoria/n)

#divido 1 sobre o valor do desvio padrão calculado
peso = abs(1 / desviopadrao)

#crio um método de predicao
def predicao(books,attend):
    #crio uma matriz (1x3) com o valor do viés e o valor informado
    A = pd.DataFrame([[peso, books, attend]])[:].values
    
    #a saída será a multiplicacao da matriz com o vies e o valor informado com o valor final de Beta 0, Beta 1 e Beta 2
    return ((A[0][0] * F[0][0]) + (A[0][1] * F[1][0]) + (A[0][2] * F[2][0]))

#TESTE
print('O valor de nota predito é : %.2f' %(predicao(3, 17)))