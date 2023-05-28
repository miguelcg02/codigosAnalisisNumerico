import numpy as np
import pandas as pd
# se le debe enviar el tamaño de la matriz cuadrada
# Ingresar por filas los valores de la matriz
# ingresar b
# ingresar x0
# ingresar 1 = decimales correctos, 2 = cifras significativas
# ingresar numero de decimales correctos o cifras significativas
# ingresar número máximo de iteraciones
# ingresar la norma 1,2,3,... 'inf', si lo que se ingresa no es valido toma la norma infinita como predeterminada

def MatJacobiSeid():
    size = int(input())
    input_data = input()
    b = input()
    x0 = input()
    tipo_error = int(input()) #1 = decimales correctos, 2 = cifras significativas
    num_tol = float(input()) #numero de decimales correctos o cifras significativas
    niter = int(input())
    norma = input()  #Escribir que puede ser un numero o inf 
    
    #---------- Creacion de A
    b = np.asarray(list(map(float, b.split()))).T
    x0 = np.asarray(list(map(float, x0.split()))).T
    
    if len(b) != size : print(f"Error: El vector b debe tener un tamaño de {size} componentes")
    if len(x0) != size : print(f"Error: El vector inicial (x0) debe tener un tamaño de {size} componentes")
    rows = input_data.split(';')
    A, A_flag=[], True
    for row in rows:
        row_data = row.strip().split()
        row_numbers = list(map(float, row_data))
        if len(row_numbers) != size: A_flag= False
        A.append(row_numbers)
    A = np.array(A)
    if not A_flag: print(f"Error: La matriz A no corresponde una una matriz cuadrada de dimensión {size} ")
   # -----------------------------------------

    if tipo_error == 1: 
        tipo = "decimales correctos"
        Tol = 0.5*(10**-num_tol)
    elif tipo_error == 2: 
        tipo = "cifras significativas"
        Tol = 5*(10**-num_tol)
    
        
    row_sums = np.sum(np.abs(A), axis=1)
    diag = np.abs(np.diag(A))
    dominant = np.all(diag > row_sums - diag)
    
    if norma =="inf": norma=np.inf
    elif int(norma) >=1: norma = int(norma)
    else : norma = np.inf
    
    c = 0
    error = Tol + 1
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    E, xn = [],[]
    T = np.linalg.inv(D) @ (L + U)
    C = np.linalg.inv(D) @ b
    if(np.linalg.det(D)==0) : print("Matriz D es singular, el método falla") ### error
    else:
        while error > Tol and c < niter:
            x1 = T @ x0 + C
            error = np.linalg.norm(x1 - x0, norma)
            if tipo_error == 2:
                error = error/np.linalg.norm(x1, norma)
            E.append(error)
            xn.append(x0)
            x0 = x1
            c += 1
        
        eigenvals = np.linalg.eigvals(T)
        rho = np.max(np.abs(eigenvals))   
        if error < Tol:
            s = x0
            error = np.linalg.norm(x1 - x0, norma)
            if tipo_error == 2:
                error = error/np.linalg.norm(x1, norma)
            E.append(error)
            xn.append(x0)
            itera = np.arange(0,c+1,1)
            df = pd.DataFrame({"Iteraciones": itera,"Xn": xn, "Error": E})
            print(df)
            print(f"La solución aproximada es: {np.ravel(s)}, con una tolerancia = {Tol} ({tipo})")
            if rho < 1: print(f"Esta solucion es única porque el radio espectral de T es {rho} y es menor a 1")
        else:
            s = x0
            print(f"Fracasó en {niter} iteraciones")
            if rho >= 1:
                    print(f"Es posible que haya fallado el método porque el radio espectral de T es {rho} y es mayor a 1")
                
            if not dominant:
                print("Es posible que haya fallado el método porque A no es diagonal dominante")

MatJacobiSeid()
