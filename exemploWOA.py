# coding-UTF-8
# Douglas D. Lieira <douglas.lieira@unesp.br>

import woa as WOA
import random
import time
from datetime import datetime

e = 1
s = 1 #variaveis para controlar o tempo de entrada e saida
BLOQUEADOS = 0 #contador de bloqueios
NEGADOS = 0   #contador de negados por não caber em nenhuma edge quando entrar
ID_DEV = 0 #id para criação dos dispositivos
devices = {} # dicionario de dispositivos
Edges = {} # dicionario de edges
LIMITE_RECURSOS = [100, 100, 100, 100]  #limite dos recursos
INICIO = 20 #define com quantos dispositivos iniciais vamos preencher as edges


#método para gerar as edges iniciais com valores randômicos de 1 a 10
def gerarEdges(nroEdges):  
     for i in range(0,nroEdges):
          if i == 0:
               nomeEdge = "atual"
          else:
               nomeEdge = "Edge" + str(i)
          Edges[nomeEdge] = [0,0,0,0] 
     return Edges

#método para verificar a disponibilidade
def verificarDisponibilidade(i, dados):
     global BLOQUEADOS
     verificaBlock = 0   #armazena os bloqueios do dispositivo verificado
     edgeAuxiliar = Edges  #cria edge auxiliar
     retorno = False   #variavel booleana de retorno
     for n in range(0,4): #atualizar cada valor da edge
          if ((dados[0][n] + edgeAuxiliar[i][n]) > LIMITE_RECURSOS[n]): #verifica se (valor que está entrando + valor da edge)  é maior que o limite daquele recurso
               verificaBlock += 1   #se for atualiza a verificaBlock, informa e retorno = true
               retorno = True
     if verificaBlock > 0:
          BLOQUEADOS += 1   #atualiza a constante BLOCK
     return retorno

#método para mudar para a próxima edge, caso não tenha disponibilidade para recurso
def mudarEdge(edge):
     v = 0
     for i in Edges:
          if (i == edge):
               if (v==0):
                    return WOA.WOA(devices[ID_DEV], Edges)
               elif (v==1):
                    return WOA.WOA(devices[ID_DEV], Edges)
               elif (v==2):
                    return WOA.WOA(devices[ID_DEV], Edges)
               else:
                    return WOA.WOA(devices[ID_DEV], Edges)
          v += 1
     
def atualizarEdgesEntrada(edgeSelecionado):
     global NEGADOS
     for c, dados in devices.items(): #Encontrar o dispositivo que entrou
          if c == ID_DEV:               
               dados[1] = edgeSelecionado #insere a edge como posicao atual do dispositivo
               for i in Edges: #selecionar a edge
                    
                    if (i == dados[1]):
                         x = 0
                         while (verificarDisponibilidade(i,dados)): #verifica disponibilidade
                              i = mudarEdge(i)     #se entrou aqui houve bloqueio, então muda de edge
                              x += 1
                              if (x == 4):      #se entrar aqui significa que não coube em nenhuma edge 
                                   NEGADOS += 1
                                   #return Edges
                                   return Edges, 'negado', dados
                         dados[1] = i  #atualiza o index 'atual' do dispositivo com a edge selecionada
                         for n in range(0,4): #atualizar cada valor da edge
                              Edges[i][n] = Edges[i][n] + dados[0][n]
                         #return Edges
                         return Edges, 'alocado', dados

#método que gera os parâmetros aleatórios do dispositivo quando entrar
def gerarParametrosDispositivos():
     Edges = [random.randrange(1,10),
                         random.randrange(1,10),
                         random.randrange(1,10),
                         random.randrange(1,10)]
     return Edges

#método que insere um novo dispositivo no dicionario devices
def criarDispositivos():
     #devices = {"id": ID_DEV, "recursos": gerarParametrosDispositivos()}
     global ID_DEV
     ID_DEV += 1
     devices[ID_DEV] = [gerarParametrosDispositivos(),""]
     return devices

#faz as entradas na edge
def entradaEdges():
     global devices
     devices = criarDispositivos() #criar os parametros do dispositivo
     print("\n********** Entrada dispositivo: **********\n" , devices[ID_DEV])
     edgeSelecionado= WOA.WOA(devices[ID_DEV], Edges) #seleciona melhor edge
     tes, situacao, retorno = atualizarEdgesEntrada(edgeSelecionado)
     algoritmo = 'WOA'
     return ID_DEV, retorno[0], retorno[1], situacao, algoritmo

          
def saidaEdges(id):
     for c, dados in devices.items():  #encontrar o dispositivo que esta saindo
          if c == id:
               print ("\n********** Saída dispositivo: ********** \n", c , dados)
               for i in Edges: #selecionar a edge
                    if (i == dados[1]):
                         for n in range(0,4): #atualizar cada valor da edge
                              Edges[i][n] =  Edges[i][n] - dados[0][n]
     del devices[id]               

#método que seleciona aleatoriamente um veiculo para sair
def selecionaSaida():
     idDevices = []
     c = len(devices) 
     for i in devices:
          idDevices = idDevices + [i]   #cria um array com todos id de devices
     return (random.choice(idDevices)) #retorna um elemento aleatorio da lista de ids

#inserir valores iniciais nas edges
def preencherEdges():
     global ID_DEV
     ID_DEV += 1
     f = ""
     i = random.randrange(0,4)
     if i == 0:
          f = "atual"
     elif i==1:
          f = "Edge1"
     elif i==2:
          f = "Edge2"
     else:
          f = "Edge3"
     devices[ID_DEV] = [gerarParametrosDispositivos(),f]
     for i in Edges:
          if i == f:
               for n in range(0,4):
                    #atualizar cada valor da edge
                    Edges[i][n] = Edges[i][n] + devices[ID_DEV][0][n]
     return Edges          

#teste1 = AHP (log=True)

def executar():

     f= gerarEdges(4)

     #preenche com tanto de dispositivos informados na constante INICIO
     for x in range(INICIO):
          preencherEdges()

     print ("Edges: ", Edges)     


def stats(): 
     print ("\nDados finais das edges: {}".format(Edges))
     print ("\nDispositivos que terminaram na região: {}".format(devices))
     print ("\nQuantidade de dispositivos: {} ".format(ID_DEV))
     print ("\nQuantidade de bloqueios: {}".format(BLOQUEADOS))
     print ("\nQuantidade de dispositivos que entraram no serviço: {}".format((ID_DEV-NEGADOS)-INICIO))
     print ("\nQuantidade de dispositivos com serviços negados: " , NEGADOS)
     sumary = [ID_DEV, BLOQUEADOS, (ID_DEV-NEGADOS)-INICIO, NEGADOS]

     return sumary