import pandas as pd
from sympy import *
from sympy.calculus.util import continuous_domain
import sys
x, y, z = symbols('x y z')


def PuntoFijo():
    Fun = input() #funcion
    gf = input() #funcion g
    X0 = float(input()) #punto inicial
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
    gf = sympify(gf)
    func = lambda m: Fun.evalf(15, subs = {x: m})
    g = lambda m: gf.evalf(15, subs = {x: m})
    
    domf = continuous_domain(Fun, x, S.Reals)
    if not domf.contains(X0):
        print(f"La función no está definida en x = {X0}. El método falla.")
        
    else:
        fn, xn, E, iters = [], [], [], []
        x_val = X0
        fe = func(X0)
        c, Error = 0, 100
        fn.append(fe)
        xn.append(X0)
        E.append(Error)
        iters.append(c)
        
        while E[c] >= Tol and fe!=0 and c < Niter:
            c = c+1
            x_val = g(X0)
            
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
        
            X0 = x_val
        
        if fe == 0:
            sol = x_val
            print(sol,"es raiz de f(x)")
            
        elif E[c] < Tol:
            sol = x_val 
            d = {"Iteraciones": iters, "Xn": xn, "f(Xn)": fn, "Error": E}
            df = pd.DataFrame(d)
            print(df, "\n")
            print(f"La solución aproximada es: {sol}, con una tolerancia = {Tol} ({tipo})")
        
        else:
            sol = x_val
            print(f"Fracaso en {Niter} iteraciones") 
            print("Verificar que g(x) cumpla las condiciones de convergencia")
    
PuntoFijo()