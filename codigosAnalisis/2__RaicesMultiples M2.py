import pandas as pd
from sympy import *
from sympy.calculus.util import continuous_domain
import sys
x, y, z = symbols('x y z')


def RaicesMultiplesM2(): 
    Fun = input() #funcion
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
    func = lambda a: Fun.evalf(15, subs = {x: a})
    derivative = diff(Fun, x)
    deriv = lambda a: diff(Fun, x).evalf(15, subs = {x: a})
    derivative2 = diff(Fun, x, 2)
    deriv2 = lambda a: diff(Fun, x, 2).evalf(15, subs = {x: a})
    
    domf = continuous_domain(Fun, x, S.Reals)
    if not domf.contains(X0):
        print(f"La función no está definida en x = {X0}. El método falla.")
        
    elif not derivative.subs(x, X0).is_finite:
        print(f"La función no es diferenciable en x = {X0}. El método falla.")
    
    elif not derivative2.subs(x, X0).is_finite:
        print(f"La función no tiene segunda derivada en x = {X0}. El método falla.")
    
    else: 
        fn, x_vals, E, dvs, dvs2, iters = [], [], [], [], [], []
        xn = X0
        f, derivada, derivada2 = func(xn), deriv(xn), deriv2(xn)
        c, Error = 0, 100         
        fn.append(f)
        dvs.append(derivada)
        dvs2.append(derivada2)
        x_vals.append(xn)
        E.append(Error)
        iters.append(c)
        
        while (E[c] >= Tol) and (f != 0) and (derivada**2 - (f*derivada2)) != 0  and (c < Niter):
          c = c + 1
          xn = xn - (f*derivada)/(derivada**2 - (f*derivada2))
          
          if not domf.contains(xn):
              print(f"La función no está definida en x{c} = {xn}. El método falla.")
              sys.exit()

          elif not derivative.subs(x,xn).is_finite:
              print(f"La función no es diferenciable en x{c} = {xn}. El método falla.")
              sys.exit()
        
          elif not derivative2.subs(x,xn).is_finite:
              print(f"La función no tiene segunda derivada en x{c} = {xn}. El método falla.")
              sys.exit()
              
          f, derivada, derivada2 = func(xn), deriv(xn), deriv2(xn)
          fn.append(f)
          dvs.append(derivada)
          dvs2.append(derivada2)
          x_vals.append(xn)
          iters.append(c)
          
          if tipo_error == 1: 
              Error_abs = abs(x_vals[c] - x_vals[c-1])
              E.append(Error_abs)
          elif tipo_error == 2: 
              Error_rel = abs((x_vals[c] - x_vals[c-1])/x_vals[c])
              E.append(Error_rel)
        
        if f == 0:
            s = xn
            print(s,"es raiz de f(x)")
            sys.exit()
        
        if (derivada**2 - (f*derivada2)) == 0:
            s = xn
            print("El método falla. El denominador es 0.") 
             
        elif E[c] < Tol:
            s = xn
            d = {"Iteraciones": iters, "Xn": x_vals, "f(Xn)": fn, "f'(Xn)": dvs, "f''(Xn)": dvs2, "Error": E}
            df = pd.DataFrame(d) 
            print(df, "\n")
            print(f"La solución aproximada es: {s}, con una tolerancia = {Tol} ({tipo})")
        
        else:
            s = xn
            print(f"Fracaso en {Niter} iteraciones") 

RaicesMultiplesM2()