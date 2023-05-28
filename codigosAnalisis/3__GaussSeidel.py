import numpy as np
import pandas as pd

def MatGaussSeid():
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
    
    if tipo_error == 1: 
        tipo = "decimales correctos"
        Tol = 0.5*(10**-num_tol)
    elif tipo_error == 2: 
        tipo = "cifras significativas"
        Tol = 5*(10**-num_tol)
    
    if norma =="inf": norma=np.inf
    elif int(norma) >=1: norma = int(norma)
    else : norma = np.inf
    
    row_sums = np.sum(np.abs(A), axis=1)
    diag = np.abs(np.diag(A))
    dominant = np.all(diag > row_sums - diag)

    c = 0
    error = Tol + 1
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    E = np.zeros(niter)
    T = np.linalg.inv(D - L) @ U
    C = np.linalg.inv(D - L) @ b
    
    eigenvalues = np.linalg.eigvals(T)
    radio_espectral = max(abs(eigenvalues))
    
    x_vals, E, iters = [], [], []
    x_vals.append(np.ravel(x0))
    E.append(error)
    iters.append(c)
    
    if np.linalg.det(D - L) == 0: 
        print("La matriz (D - L) no es invertible. El método falla")

    else: 
        while error > Tol and c < niter:
            x1 = T @ x0 + C
            x_vals.append(np.ravel(x1))
            error = np.linalg.norm(x1 - x0, norma)
            
            if tipo_error == 2:
                error = error/np.linalg.norm(x1, norma)
          
            E.append(error)
            x0 = x1
            c += 1
            iters.append(c)

        if error < Tol:
            s = x0
            d = {"Iteraciones": iters, "Xn": x_vals, "Error": E}
            df = pd.DataFrame(d) 
            print(df, "\n")
            print(f"La solución aproximada es: {np.ravel(s)}, con una tolerancia = {Tol} ({tipo})")
            if radio_espectral < 1:
                print(f"Esta solucion es única porque el radio espectral de T es {radio_espectral} y es menor a 1")
        else:
            s = x0
            print(f'Fracasó en {niter} iteraciones')
            if radio_espectral >= 1:
                print(f"Es posible que haya fallado el método porque el radio espectral de T es {radio_espectral} y es mayor a 1")
            if not dominant: 
                print("Es posible que haya fallado el método porque A no es diagonal dominante")

MatGaussSeid()
