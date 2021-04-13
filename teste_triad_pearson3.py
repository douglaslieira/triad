# coding-UTF-8
# Douglas D. Lieira <douglas.lieira@unesp.br>

from AnalyticHierarchyProcess import AHP
import random
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import pearson3
import exemploGuloso as Guloso
import exemploPolitica as Politica
import exemploWOA as WOA

TEMPO_TESTE = 1200 #Tempo de simulação em segundos
loc_IN = 6
loc_OUT = 12
QTD = 250 #Quantidade gerada de momentos de saída/entrada
REPT = 33 #Quantidade de repetições para cada algoritmo

res_Guloso = {}
res_Politica = {}
res_WOA = {}

r_IN = pearson3.rvs(0, loc=loc_IN, scale=2, size=QTD)
poi_in = np.asarray([n for n in r_IN if n >= 1], dtype=np.int)

r_OUT = pearson3.rvs(0, loc=loc_OUT, scale=2, size=QTD)
poi_out = np.asarray([n for n in r_OUT if n >= 1], dtype=np.int)

QTD_in = poi_in.size
QTD_out = poi_out.size

def exe_metodo(metodo):
    e = 1
    e_p = 1
    s = 1
    s_p = 1

    print ("\nEntrada: ", poi_in)
    print ("\nEntradaSoma: ", poi_in.sum())
 
    print ("\nSaida: ", poi_out)
    print ("\nSaidaSoma: ", poi_out.sum())

    metodo.executar()

    metodo.devices.clear()
    metodo.ID_DEV = 0
    metodo.NEGADOS = 0
    metodo.BLOQUEADOS = 0

    for i in range(0,TEMPO_TESTE):
         data_hora = datetime.now()
         data_hora = data_hora.strftime('%d/%m/%Y %H:%M:%S')
         print ('segundo',i, '-' ,data_hora)
         if e_p < QTD_in:
             if e == poi_in[e_p] and poi_in[e_p] != 0:
                  metodo.entradaEdges()
                  e = 0
                  e_p += 1
             
         if s_p < QTD_out:
             if s == poi_out[s_p] and poi_out[s_p] != 0:
                  metodo.saidaEdges(metodo.selecionaSaida())
                  s = 0
                  s_p += 1
                  
         e += 1  
         s += 1
         #time.sleep(0.05)

    metodo.Edges.clear()

    return metodo.stats()

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def excluir_conf_int(dados):
    cont_int = mean_confidence_interval(dados)
    lim1 = cont_int[1]
    lim2 = cont_int[2]
    dados_validos = [dado for dado in dados if dado > lim1 and dado < lim2]
    return dados

def gera_grafico(dados, lbl_y):
    x = 10*np.array(range(len(dados[0])))
    maior = max([valor for linha in dados for valor in linha])
    NomesMetodos = ['Greedy', 'Reliable', 'TRIAD']
    plt.plot(x, dados[0], label=NomesMetodos[0], color='blue', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='blue', markersize=6 )
    plt.plot(x, dados[1], label=NomesMetodos[1], color='steelblue', linestyle='solid', linewidth = 2, marker='s', markerfacecolor='red', markersize=6 )
    plt.plot(x, dados[2], label=NomesMetodos[2], color='darkblue', linestyle='dotted', linewidth = 2, marker='^', markerfacecolor='green', markersize=6 )
    
    plt.legend(loc='best')
    plt.ylabel(lbl_y)
    plt.show()

qtd_bloc_Guloso = []
qtd_bloc_Politica = []
qtd_bloc_WOA = []
qtd_bloc_total = []

qtd_serv_Guloso = []
qtd_serv_Politica = []
qtd_serv_WOA = []
qtd_serv_total = []

qtd_nega_Guloso = []
qtd_nega_Politica = []
qtd_nega_WOA = []
qtd_nega_total = []

conv_WOA = []

for i in range(0, REPT):
    res_Guloso[i] = exe_metodo(Guloso)
    qtd_bloc_Guloso.append(res_Guloso[i][1])
    qtd_serv_Guloso.append(res_Guloso[i][2])
    qtd_nega_Guloso.append(res_Guloso[i][3])

    res_Politica[i] = exe_metodo(Politica)
    qtd_bloc_Politica.append(res_Politica[i][1])
    qtd_serv_Politica.append(res_Politica[i][2])
    qtd_nega_Politica.append(res_Politica[i][3])

    res_WOA[i] = exe_metodo(WOA)
    qtd_bloc_WOA.append(res_WOA[i][1])
    qtd_serv_WOA.append(res_WOA[i][2])
    qtd_nega_WOA.append(res_WOA[i][3])

qtd_bloc_total.append(excluir_conf_int(qtd_bloc_Guloso))
qtd_bloc_total.append(excluir_conf_int(qtd_bloc_Politica))
qtd_bloc_total.append(excluir_conf_int(qtd_bloc_WOA))

qtd_serv_total.append(excluir_conf_int(qtd_serv_Guloso))
qtd_serv_total.append(excluir_conf_int(qtd_serv_Politica))
qtd_serv_total.append(excluir_conf_int(qtd_serv_WOA))

qtd_nega_total.append(excluir_conf_int(qtd_nega_Guloso))
qtd_nega_total.append(excluir_conf_int(qtd_nega_Politica))
qtd_nega_total.append(excluir_conf_int(qtd_nega_WOA))

arquivo = open('resSim1.py', 'w')

arquivo.write("\n#TEMPO_TESTE: {}".format(TEMPO_TESTE))
arquivo.write("\n#loc_IN: {}".format(loc_IN))
arquivo.write("\n#loc_OUT: {}".format(loc_OUT))
arquivo.write("\n#QTD: {}".format(QTD))
arquivo.write("\n#REPT: {}".format(REPT))
arquivo.write("\nnDevices: {}".format(QTD))
arquivo.write("\n")
arquivo.write("\n#Resultados Guloso: {}".format(res_Guloso))
arquivo.write("\n#Resultados Politica: {}".format(res_Politica))
arquivo.write("\n#Resultados TRIAD: {}".format(res_WOA))
arquivo.write("\n")
arquivo.write("\nBloqueios= {}".format(qtd_bloc_total))
arquivo.write("\nNegados= {}".format(qtd_nega_total))
arquivo.write("\nServicos= {}".format(qtd_serv_total))

arquivo.close()