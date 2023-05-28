import numpy as np
import matplotlib.pyplot as plt 

# Posibles errores tomados en cuenta:
# Los valores dados de x son diferentes para que sea una función y no una relación
#------- Falta teorema de aproximación de Wierstrass


def Lagrange():
    x = input()
    y = input()
    
    x = np.asarray(list(map(float, x.split())))
    y = np.asarray(list(map(float, y.split())))
    
    if len(np.unique(x)) == len(x): different = True
    else: different = False
    if not different: print("Los valores de x no deben repertirse para que sea una función ") 
    
    n = len(x)
    Tabla = np.zeros((n, n))
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]
    for i in range(n):
        Li = 1
        den = 1
        for j in range(n):
            if j != i:
                paux = [1, -x[j]]
                Li = np.convolve(Li, paux)
                den *= (x[i] - x[j])
        Tabla[i, :] = y[i] * Li / den
    pol = np.sum(Tabla, axis=0)
    
    #Imprimir el polinomio---------------------------------------
    pol_string, i = str(round(pol[0],3)) + " x^" + str(len(pol)-1), 1
    for comp in pol[1:-1]:
        if round(comp,3)>0: pol_string+= " + " + str(round(comp,3)) + " x^" + str(len(pol)-1-i) +" "
        else : pol_string+= str(round(comp,3)) + " x^" + str(len(pol)-1-i) +" "
        i+=1
    pol_string+=str(round(pol[-1],3))
    #----------------------------------------------------------------
    print(f"El polinomio que interpola los puntos dados es: {pol_string}")
    #Grafica del polinomio ------------------------------------------
    z, paso = 0, 0.1
    t = np.arange(min(x),max(x)+paso,paso) #domain function
    for i, val in zip(range(len(pol)), pol):
        z += val*t**(len(pol)-i-1)
    plt.plot(x,y, marker='.', ls='none', ms=10, color="k")
    plt.plot(t,z)
    plt.title(f"Gráfica de la interpolación de los puntos")
    plt.legend(["Puntos dados", "Interpolación"])
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
Lagrange()


