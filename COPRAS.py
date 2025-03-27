##############################################################################
# Nombre del archivo: COPRAS.py
# Fecha última modificación: 08/11/2023
# Autor/es:
#   Néstor Velaz
# Pag 87 libro
###############################################################################

import numpy as np

def NormalizedDecisionMatrix(X,signo):
    
       
    NumAlternativas=X.shape[0]
    NumCriterios=X.shape[1]
    
    r_asterisco=np.zeros((NumAlternativas,NumCriterios)) 

    SumaColumna=np.sum(X, axis=0) # 0 suma columnas; 1 suma filas
    
    for i in range (0,NumAlternativas):
        
        for j in range (0,NumCriterios):
            
            r_asterisco[i][j]=X[i][j]/SumaColumna[j]

    #r_asterisco nan ???
    return r_asterisco

def WeightedNormalizedDecisionMatrix(r_asterisco,omega):
    
    NumAlternativas=r_asterisco.shape[0]
    NumCriterios=r_asterisco.shape[1]

    r_virgulilla=np.zeros((NumAlternativas,NumCriterios))

    for i in range (0,NumAlternativas):

        r_virgulilla[i][:]=np.multiply(r_asterisco[i][:],omega)
    return r_virgulilla

def MaximinizingMinimizingIndexes(r_virgulilla,signo):
    
    NumAlternativas=r_virgulilla.shape[0]
    NumCriterios=r_virgulilla.shape[1] 
    
    S_Negativo=[]
    S_Positivo=[]
    
    
    for i in range(0,NumAlternativas):
        Negativo=0
        Positivo=0
        
        for j in range(0,NumCriterios):
            
            if signo[j]=='-':
                Negativo=Negativo+r_virgulilla[i][j]
            else:
                Positivo=Positivo+r_virgulilla[i][j]
                
        S_Negativo.append(Negativo)
        S_Positivo.append(Positivo)
        
#    
#    print(S_Negativo)
#    print(S_Positivo)
    return S_Negativo,S_Positivo

def RelativeSignificanceValue(X,S_Negativo,S_Positivo):

    NumAlternativas=X.shape[0]
    
    Q_eq1=np.zeros(NumAlternativas)
    Q_eq2=np.zeros(NumAlternativas)
    
    Inv_Negativo=[]
    
    for i in range (0,NumAlternativas):
        #HE tenido que poner el if porque sino si todos los valores negativos son 0 entonces el resultado es inf
        if S_Negativo[i] != 0:
            Inv_Negativo.append(1 / S_Negativo[i])
        else:
            Inv_Negativo.append(1)
            S_Negativo[i] = 1


    for i in range(0, NumAlternativas):
        Q_eq1[i]=S_Positivo[i]+((min(S_Negativo)*sum(S_Negativo))/(S_Negativo[i]*min(S_Negativo)*sum(Inv_Negativo)))
        
        Q_eq2[i]=S_Positivo[i]+(sum(S_Negativo)/(S_Negativo[i]*sum(Inv_Negativo)))
        
    return Q_eq1,Q_eq2

def FinalRankingAlternatives(Q):
    
    Q_orden=sorted(Q, reverse=True)
        
    Q=Q.tolist()
  
    Solucion=[]

    for i in range (0,len(Q_orden)):
        Solucion.append(Q.index(Q_orden[i]))
    
    return Solucion,Q_orden

def copras(X,omega,signo):

################################################################################    
###    Ejemplo libro pag 89
#    
#    X=np.array([[0.710, 4.100, 0.180, 0.720, 0.990, 0.250],
#                [1.330, 5.900, 0.740, 0.310, 0.420, 0.830],
#                [1.450, 4.900, 0.270, 0.650, 0.420, 0.440]])
#    
#    omega=np.array([0.171, 0.185, 0.177,0.225,0.157,0.085])
#    signo=['-','-','+','-','-','+']
###############################################################################      

    r_asterisco=NormalizedDecisionMatrix(X,signo)
    r_virgulilla=WeightedNormalizedDecisionMatrix(r_asterisco,omega)

    S_Negativo,S_Positivo=MaximinizingMinimizingIndexes(r_virgulilla,signo)
    
    Qeq1,Qeq2=RelativeSignificanceValue(X,S_Negativo,S_Positivo)
    Q=Qeq1 #/ np.max(Qeq1) #Hay dos ecuaciones, se ha escogido la segunda
    
    #Ranking,Value=FinalRankingAlternatives(Q)

        
    return Q
    #return S_Negativo, Q

