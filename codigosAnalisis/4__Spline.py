import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import sys

def Spline():
    x = input()
    y = input()
    d = int(input()) # 1: lineal, 2: cuadratico, 3: cubico
    
    x = np.asarray(list(map(float, x.split())))
    y = np.asarray(list(map(float, y.split())))
   
    if len(np.unique(x)) == len(x): different = True
    else: different = False
    if not different: 
        print("Los valores de x no deben repertirse para que sea una función ") #error
        sys.exit()

    n = len(x)
    
    # Ordenar los vectores
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]
    
    A = np.zeros(((d+1)*(n-1),(d+1)*(n-1)))
    b = np.zeros((d+1)*(n-1))
    
    cua = np.power(x, 2)
    cub = np.power(x, 3)
    flag, bad = False, False
    # Lineal
    if d == 1:
        c = 0
        h = 0
        for i in range(n-1):
            A[i, c] = x[i]
            A[i, c+1] = 1
            b[i] = y[i]
            c += 2
            h += 1
        
        c = 0
        for i in range(1, n):
            A[h, c] = x[i]
            A[h, c+1] = 1
            b[h] = y[i]
            c += 2
            h += 1
    
    # Quadratic
    elif d == 2:
        try:
            c, h = 0, 0
            for i in range(0, n-1):
                A[i, c] = cua[i]
                A[i, c+1] = x[i]
                A[i, c+2] = 1
                b[i] = y[i]
                c += 3
                h += 1

            c = 0
            for i in range(1, n):
                A[h, c] = cua[i]
                A[h, c+1] = x[i]
                A[h, c+2] = 1
                b[h] = y[i]
                c += 3
                h += 1

            c = 0
            for i in range(1, n-1):
                A[h, c] = 2 * x[i]
                A[h, c+1] = 1
                A[h, c+3] = -2 * x[i]
                A[h, c+4] = -1
                b[h] = 0
                c += 4
                h += 1

            A[h, 0] = 2
            b[h] = 0
        except IndexError:
            bad= True
            print("La función no puede ser solucionada con este algoritmo")
        if np.linalg.det(A)==0 or bad: 
            flag=True
            print("La matriz obtenida es no es invertible, por lo tanto se presenta la siguiente aproximación del polinomio por medio de la implementación de la librería interp1d de spline")
            spline = interp1d(x, y, kind='quadratic')
            x_new = np.linspace(min(x), max(x), num=100)
            y_new = spline(x_new)
            plt.plot(x_new,y_new)
            plt.show()
            
    # Cubic
    elif d == 3:
        c, h = 0, 0
        for i in range(n-1):
            A[i, c] = cub[i]
            A[i, c+1] = cua[i]
            A[i, c+2] = x[i]
            A[i, c+3] = 1
            b[i] = y[i]
            c += 4
            h += 1
        
        c = 0
        for i in range(1, n):
            A[h, c] = cub[i]
            A[h, c+1] = cua[i]
            A[h, c+2] = x[i]
            A[h, c+3] = 1
            b[h] = y[i]
            c += 4
            h += 1
        
        c = 0
        for i in range(1, n-1):
            A[h, c] = 3*cua[i]
            A[h, c+1] = 2*x[i]
            A[h, c+2] = 1
            A[h, c+4] = -3*cua[i]
            A[h, c+5] = -2*x[i]
            A[h, c+6] = -1
            b[h] = 0
            c += 4
            h += 1
        
        c = 0
        for i in range(1, n-1):
            A[h, c] = 6*x[i]
            A[h, c+1] = 2
            A[h, c+4] = -6*x[i]
            A[h, c+5] = -2
            b[h] = 0
            c += 4
            h += 1
        
        A[h, 0] = 6*x[0]
        A[h, 1] = 2
        b[h] = 0
        h += 1
        A[h, c] = 6*x[-1]
        A[h, c+1] = 2
        b[h] = 0
    if not flag:
        val = np.linalg.inv(A).dot(b)
        reshaped_matrix = val.reshape(len(x)-1, d+1)
        Tabla = reshaped_matrix
        #---Imprimir polinomio --------
        Tabla_string, j= [0]*len(Tabla),0
        l=1
        for pol in Tabla:
            pol_string, i = str(round(pol[0],3)) + " x^" + str(len(pol)-1), 1
            for comp in pol[1:-1]:
                if round(comp,3)>0: pol_string+= " + " + str(round(comp,3)) + " x^" + str(len(pol)-1-i) +" "
                else : pol_string+= str(round(comp,3)) + " x^" + str(len(pol)-1-i) +" "
                i+=1
                
            print(f"El polinomio que interpola en el tramo {l} dados es: {pol_string}")
            l+=1
            if round(pol[-1],3)>0: pol_string+=" + "+str(round(pol[-1],3))
            else: pol_string+= str(round(pol[-1],3))
            
            Tabla_string[j]= pol_string
            j+=1
        print(f"Los polinomios de grado {d} que interpolan los puntos son :")
        df = pd.DataFrame({"NumPol":np.arange(1,len(x),1),"Polinomios": np.transpose(Tabla_string)})
        print(df)
        
        for pol, x_el in zip(Tabla, range(len(x)-1)):
            t = np.linspace(x[x_el],x[x_el+1], 100) #domain function
            z=0
            for i, val in zip(range(len(pol)), pol):
                z += val*t**(len(pol)-i-1)
            plt.plot(t,z)
            
        plt.title(f"Gráfica de la interpolación de los puntos")
        plt.plot(x,y, marker='.', ls='none', ms=10, color="k")
        plt.legend(["Puntos dados", "Interpolación"])
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()
        plt.show()

Spline()