# -*- coding: utf-8 -*-
# Douglas D. Lieira <douglas.lieira@unesp.br>

import random
import numpy
import math
#from solution import solution
import time



def euclidiana(y,z):
    # x, y, z = C, XP, X
    return (numpy.sqrt(sum((y - z) ** 2))) #distancia euclidiana

def update_Coeficientes(a):
    
    r1 = random.randrange(0,11)/10
    r2 = random.randrange(0,11)/10
    C = 2*r2
    A = 2*a*r1-a
    
    return A,C

def F10(x):
    dim=len(x);
    o=-20*numpy.exp(-.2*numpy.sqrt(numpy.sum(x**2)/dim))-numpy.exp(numpy.sum(numpy.cos(2*math.pi*x))/dim)+20+numpy.exp(1);
    return o;

def WOA(sw, Serv_List):
    #Edge_nro = sw
    Max_iter = 30
    dim = 4
    
    Pos = {}
    Nro_serv = len(Serv_List)


    #dim=30
    #SearchAgents_no=50
    #lb=-100
    #ub=100
    #Max_iter=500
    #if not isinstance(lb, list):
    #    lb = [lb] * dim
    #if not isinstance(ub, list):
    #    ub = [ub] * dim
        
    
    # initialize position vector and score for the leader
    Leader_pos=numpy.zeros(dim)
    Leader_score=float("inf")  #change this to -inf for maximization problems
    
    
    #Initialize the positions of search agents
    #Positions = numpy.zeros((SearchAgents_no, dim))
    Positions = numpy.zeros((Nro_serv,4))
    l=0

    for j in Serv_List:
        for i in range(dim):
            #Positions[:, i] = numpy.random.uniform(0,1,SearchAgents_no) *(ub[i]-lb[i])+lb[i]
            #Positions[:, i] = numpy.random.uniform(0,1,SearchAgents_no) *(ub[i]-lb[i])+lb[i]
            y = numpy.array([Serv_List[j][i] / 100])
            z = numpy.array([sw[0][i]])
            Positions[i, l] = euclidiana(z,y)
            #Positions[i, l] = y #euclidiana(z,y)
        l += 1    
    
    #Initialize convergence
    convergence_curve=numpy.zeros(Max_iter)
    
    
    ############################
    #s=solution()

    #print("WOA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
    
    t=0  # Loop counter
    
    # Main loop
    while t<Max_iter:
        for i in range(0,Nro_serv):
            
            # Return back the search agents that go beyond the boundaries of the search space
            
            #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)
            #for j in range(dim):        
            #    Positions[i,j]=numpy.clip(Positions[i,j], lb[j], ub[j])
            
            # Calculate objective function for each search agent
            fitness=F10(Positions[i,:])
            
            # Update the leader
            if fitness<Leader_score: # Change this to > for maximization problem
                Leader_score=fitness; # Update alpha
                Leader_pos=Positions[i,:].copy() # copy current whale position into the leader position
                Leader = i
            
        
        
        a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0 in Eq. (2.3)
        
        # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
        a2=-1+t*((-1)/Max_iter);
        
        # Update the Position of search agents 
        for i in range(0,Nro_serv):
            r1=random.random() # r1 is a random number in [0,1]
            r2=random.random() # r2 is a random number in [0,1]
            
            A=2*a*r1-a  # Eq. (2.3) in the paper
            C=2*r2      # Eq. (2.4) in the paper
            
            
            b=1;               #  parameters in Eq. (2.5)
            l=(a2-1)*random.random()+1   #  parameters in Eq. (2.5)
            
            p = random.random()        # p in Eq. (2.6)
            
            for j in range(0,dim):
                
                if p<0.5:
                    if abs(A)>=1:
                        rand_leader_index = math.floor(Nro_serv*random.random());
                        X_rand = Positions[rand_leader_index, :]
                        D_X_rand=abs(C*X_rand[j]-Positions[i,j]) 
                        Positions[i,j]=X_rand[j]-A*D_X_rand      
                        
                    elif abs(A)<1:
                        D_Leader=abs(C*Leader_pos[j]-Positions[i,j]) 
                        Positions[i,j]=Leader_pos[j]-A*D_Leader      
                    
                    
                elif p>=0.5:
                  
                    distance2Leader=abs(Leader_pos[j]-Positions[i,j])
                    # Eq. (2.5)
                    Positions[i,j]=distance2Leader*math.exp(b*l)*math.cos(l*2*math.pi)+Leader_pos[j]
                    
      
        
        convergence_curve[t]=Leader_score
        #if (t%1==0):
        #       print(['At iteration '+ str(t)+ ' the best fitness is '+ str(Leader_score)]);
        t=t+1
    

    timerEnd=time.time()  
    endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    executionTime=timerEnd-timerStart


    arquivo = open('convergenciaWOA1.py', 'a')
    arquivo.write(str(convergence_curve)+"\n")
    arquivo.close()

    #print (convergence_curve)
    sel = ""
    if (Leader==0):
        sel = "atual"
    elif (Leader==1):
        sel = "Edge1"
    elif (Leader==2):
        sel = "Edge2"
    elif (Leader==3):
        sel = "Edge3"
    else:
        sel = "erro"
    #print ("Selecionado:   ", sel, Serv_List[sel])
    return sel

    
    


