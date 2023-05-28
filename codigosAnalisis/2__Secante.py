import pandas as pd
from sympy import *
from sympy.calculus.util import continuous_domain
import sys
x, y, z = symbols('x y z')


def Secante(): 
    x, y, z = symbols('x y z')
    Fun = input() #funcion
    X0 = float(input()) #punto inicial
    X1 = float(input()) #segundo punto inicial
    tipo_error = int(input()) # 1 = decimales correctos, 2 = cifras significativas
    num_tol = float(input()) #numero de decimales correctos o cifras significativas
    Niter = int(input()) #iteraciones maximas
    
    if tipo_error == 1: 
        tipo = "decimales correctos"
        Tol = 0.5*(10**-num_tol)
    elif tipo_error == 2: 
        tipo = "cifras significativas"
        Tol = 5*(10**-num_tol)
    
    Fun = sympify(Fun)
    func = lambda m: Fun.evalf(15, subs = {x: m})
    
    domf = continuous_domain(Fun, x, S.Reals)
    if not domf.contains(X0):
        print(f"La función no está definida en x = {X0}. El método falla.")
    elif not domf.contains(X1):
        print(f"La función no está definida en x = {X1}. El método falla.")
    
    else: 
        fn, xn, E, iters = [], [], [], []
        f0, f1 = func(X0), func(X1)
        fn.extend([f0,f1])
        xn.extend([X0,X1])
        E.extend([abs(100), abs(X0-X1)])
        iters.extend([0,1])
        
        if f0 == 0:
            print(X0, "es raiz de f(x)")
        
        elif f1 == 0:
            print(X1, "es raiz de f(x)")
        
        else:
            c = 1
            x_val = X1
            while (E[c] >= Tol) and (fn[c] != 0) and (f1-f0 != 0)  and (c < Niter):
                X1, X0 = xn[c], xn[c-1]
                f1, f0 = fn[c], fn[c-1]
                c = c+1
                x_val = X1 - (f1*(X1-X0))/(f1 - f0)   
                
                if not domf.contains(x_val):
                    print(f"La función no está definida en x{c} = {x_val}. El método falla.")
                    sys.exit()
                    
                fe = func(x_val)
                fn.append(fe)
                xn.append(x_val)
                iters.append(c)
    
                if tipo_error == 1: 
                    Error_abs = abs(xn[c] - xn[c-1])
                    E.append(Error_abs)
                elif tipo_error == 2: 
                    Error_rel = abs((xn[c] - xn[c-1])/xn[c])
                    E.append(Error_rel)
              
            if fn[c] == 0:
                s = x_val
                print(s,"es raiz de f(x)")
                sys.exit()
               
            if (f1-f0 == 0):
                print("El método falla")
               
            elif E[c] < Tol:
                s = x_val
                d = {"Iteraciones": iters, "Xn": xn, "f(Xn)": fn, "Error": E}
                df = pd.DataFrame(d) 
                print(df, "\n")
                print(f"La solución aproximada es: {s}, con una tolerancia = {Tol} ({tipo})")
            
            else:
                s = x_val
                print(f"Fracaso en {Niter} iteraciones ") 
    
Secante()