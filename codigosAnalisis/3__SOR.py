import numpy as np
import pandas as pd

# se le debe enviar el tamaño de la matriz cuadrada
# Ingresar por filas los valores de la matriz
# ingresar b 
# ingresar x0
# ingresar w entre 0 y 2, factor de ponderación
# ingresar 1 = decimales correctos, 2 = cifras significativas
# ingresar numero de decimales correctos o cifras significativas
# ingresar número máximo de iteraciones
# ingresar la norma 1,2,3,... 'inf'

# Posibles errores tomados en cuenta:
# w no está en el rango de (0,2)
# Matriz D-wL es singular

def SOR():
    size = int(input())
    input_data = input()
    b = input()
    x0 = input()
    w = float(input())
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
    
    if w<=0 or w>=2: print(" El peso de w no está dentro de su dominio. Elige un número entre I(0,2) para que el método converja") #Imprimir este error

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
    
    simetria = np.all(np.abs(A-A.T) < 1e-8)
    def_positiva = np.all(np.linalg.eigvals(A) > 0)
    
    c = 0
    error = Tol + 1
    D = np.diag(np.diag(A))
    L = -np.tril(A, k=-1)
    U = -np.triu(A, k=1)
    E = [Tol + 1]
    x_n = [x0]
    
    if np.linalg.det(D - w * L)== 0:  print("Matriz D-wL es singular, el método falla") ### error
    T = np.linalg.inv(D - w * L) @ ((1 - w) * D + w * U)
    C = w * np.linalg.inv(D - w * L) @ b
    
    eigenvals = np.linalg.eigvals(T)
    rho = np.max(np.abs(eigenvals))
    while error > Tol and c < niter:
        x1 = T @ x0 + C
        error = np.linalg.norm(x1 - x0, norma)
        if tipo_error == 2:
            error = error/np.linalg.norm(x1, norma)
        E.append(error)
        x0 = x1
        x_n.append(x0)
        c += 1
    if error < Tol:
        s = x0
        itera = np.arange(0,c+1,1)
        print(f"La solución aproximada es: {np.ravel(s)}, con una tolerancia = {Tol} ({tipo}) ")
        df = pd.DataFrame({"Iteraciones": itera,"Xn": x_n, "Error":E})
        print(df)
        print(f'La solución aproximada es: {np.ravel(s)}, con una tolerancia = {Tol} ({tipo})')
        if rho < 1: print(f"Esta solucion es única porque el radio espectral de T es {rho} y es menor a 1")
    else:
        s = x0
        print(f'Fracasó en {niter} iteraciones')
        if not dominant:
            print("El método puede diverger porque la matriz A no es estrictamente diagonal dominante") 
        print("Es posible que haya fallado el método porque: ")
        if rho >= 1:
            print(f"- El radio espectral de T es {rho} y es mayor a 1")
        if not simetria: 
            print("- La matriz A no es simétrica")
        if not def_positiva:
            print("- La matriz A no es definida positiva")

# Casos SOR
# 4
# 45 13 -4 8; -5 -28 4 -14 ; 9 15 63 -7 ; 2 3 -8 -42 
# -25 82 75 -43
# 2 2 2 2
# 1.3 
# 1
# 5
# 100
# 2
# Casos Jacobi y gauss
# 4
# 45 13 -4 8; -5 -28 4 -14 ; 9 15 63 -7 ; 2 3 -8 -42 
# -25 82 75 -43
# 2 2 2 2
# 1
# 5
# 100
# 2

SOR()

