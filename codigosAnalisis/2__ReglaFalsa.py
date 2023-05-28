import pandas as pd
from sympy import *
from sympy.calculus.util import continuous_domain
import sys
x, y, z = symbols('x y z')


def ReglaFalsa():
    Fun = input() #funcion
    a = float(input()) #limite inferior
    b = float(input()) #limite superior
    tipo_error = int(input()) # 1 = decimales correctos, 2 = cifras significativas
    num_tol = float(input()) #numero de decimales correctos o cifras significativas
    Niter = int(input()) #iteraciones maximas
    
    if tipo_error == 1: 
        tipo = "decimales correctos"
        Tol = 0.5*(10**-num_tol)
    elif tipo_error == 2: 
        tipo = "cifras significativas"
        Tol = 5*(10**-num_tol)
        
    if a > b:
        temp = a
        a, b = b, temp
    
    Fun = sympify(Fun)
    func = lambda m: Fun.evalf(15, subs = {x: m})
    dom = continuous_domain(Fun, x, S.Reals)
    interval = Interval(a,b)
    if not interval.is_subset(dom):
        print(f"La función no es continua en el intervalo [{a},{b}]. El método falla.")
        
    else: 
        x_vals, fm, E, iters = [], [], [], []
        fa = func(a)
        fb = func(b)
        
        if fa == 0:
            s = a
            E = 0
            print(s, "es raiz de f(x)")
          
        elif fb == 0:
        	s = b
        	E = 0
        	print(s, "es raiz de f(x)")
            
        elif fa*fb < 0:
            c = 0
            Xm = a - (fa*(b-a))/(fb - fa)         
            fe = func(Xm)
            fm.append(fe)
            x_vals.append(Xm)
            E.append(100)
            iters.append(c)
        
            while E[c] >= Tol and fe!= 0 and c < Niter:
                if fa*fe < 0: 
                    b = Xm              
                    fb = func(b)
                else:
                    a = Xm
                    fa = func(a)
                
                c = c+1
                Xm = a - (fa*(b-a))/(fb - fa)   
                fe = func(Xm)
                fm.append(fe)
                x_vals.append(Xm)
                iters.append(c)
                
                if tipo_error == 1: 
                    Error_abs = abs(x_vals[c] - x_vals[c-1])
                    E.append(Error_abs)
                elif tipo_error == 2: 
                    Error_rel = abs((x_vals[c] - x_vals[c-1])/x_vals[c])
                    E.append(Error_rel)
                   
            if fe == 0:
                s = Xm
                print(s,"es raiz de f(x)")
            
            elif E[c] < Tol:
                s = Xm
                d = {"Iteraciones": iters, "Xn": x_vals, "f(Xn)": fm, "Error": E}
                df = pd.DataFrame(d)
                print(df, "\n")
                print(f"La solución aproximada es: {s}, con una tolerancia = {Tol} ({tipo})")
                
            else:
                s = Xm
                print(f"Fracaso en {Niter} iteraciones") 
        
        else:
        	print("El intervalo es inadecuado")
        
ReglaFalsa()