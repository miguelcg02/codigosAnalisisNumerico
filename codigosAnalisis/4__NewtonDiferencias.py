import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Recibe una fila de x y una fila de y
# Revisa que no se repitan valores en x
def Newtonint():
    x = input()
    y = input()
    
    x = np.asarray(list(map(float, x.split())))
    y = np.asarray(list(map(float, y.split())))
    
   
    if len(np.unique(x)) == len(x): different = True
    else: different = False
    if not different: print("Los valores de x no deben repertirse para que sea una función ") #error
   
    n = len(x)
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]
    Tabla = np.zeros((n, n + 1))
    Tabla[:, 0] = x
    Tabla[:, 1] = y
    
    for j in range(2, n + 1):
        for i in range(j - 1, n):
            Tabla[i, j] = (Tabla[i, j - 1] - Tabla[i - 1, j - 1]) / (Tabla[i, 0] - Tabla[i - j + 1, 0])
    df = pd.DataFrame(Tabla)
    coef = np.diag(Tabla[:, 1:])

    #######Newtonor
    pol = np.array([1])
    acum = pol
    pol = coef[0] * acum
    
    for i in range(n - 1):
        pol = np.concatenate(([0], pol))
        acum = np.convolve(acum, [1, -x[i]])
        pol = pol + coef[i + 1] * acum
    
    print("Tabla de diferencias divididas")
    print(df)
    print(f"Se toman los siguientes coeficientes diagonales de la tabla desde la 2da columna, correspondientes a: {coef}")
    
    # Imprimir el polinomio ---------------------------------------------
    pol_string, i = str(round(pol[0],3)) + " x^" + str(len(pol)-1), 1
    for comp in pol[1:-1]:
        if round(comp,3)>0: pol_string+= " + " + str(round(comp,3)) + " x^" + str(len(pol)-1-i) +" "
        else : pol_string+= str(round(comp,3)) + " x^" + str(len(pol)-1-i) +" "
        i+=1
    pol_string+=str(round(pol[-1],3))
    print(f"El polinomio que interpola los puntos dados es: {pol_string}")
    # Grafica -------------------------------------------------------------
    
    z, paso = 0, 0.1
    t = np.arange(min(x),max(x)+paso,paso) #domain function
    for i, val in zip(range(len(pol)), pol):
        z += val*t**(len(pol)-i-1)
    plt.plot(x,y, marker='.', ls='none', ms=10, color="k")
    plt.plot(t,z)
    plt.title(f"Gráfica de la interpolación de los puntos")
    plt.legend(["Puntos dados", "Interpolación"])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.show()

Newtonint()