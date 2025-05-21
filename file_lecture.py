import numpy as np
import re
import os

# Función para separar los números de la línea
def separar_numeros(linea, op):
    # Utiliza una expresión regular para detectar números en notación científica
    # La opción 1 es para filtrar las coordenadas del archivo .in sin simular
    if op == 1:
        numeros = re.findall(r'[+-]?\d+\.\d+E[+-]?\d+', linea)
        return [float(num) for num in numeros]
    # La opción 2 es para filtrar las coordenadas del archivo después de simular
    elif op == 2:
        numeros = re.findall(r'[+-]?\d+\.\d+E?[+-]?\d+', linea)

        return [float(num) for num in numeros][:3]

# Función que extrae las coordenadas de los archivos .in
def get_coordinates(path):
    # Se abre el archivo .txt
    with open(path, 'r') as IN_line:
        raw_coordinates = IN_line.readlines()
    keyIndex = 0
    # Todos los IN tienen en común que la lista de nodos inicia en la coordenada 13
    raw_coordinates = raw_coordinates[12:]
    cen = True
    i = 0
    # Se recorre el .txt hasta encontrar el texto N ,R5.3,LOC,     -1 que está después de las cooordenadas
    while cen:
        if 'N ,R5.3,LOC,     -1' in raw_coordinates[i]:
            keyIndex = i
            cen = False
        i += 1
    # Se indexan las coordenadas con el índice que devuelva el recorrido
    raw_coordinates = raw_coordinates[:keyIndex]
    return raw_coordinates

# Función que extrae las coordenadas de los archivos de simulación
def get_sim_coordinates(path):
    # Se abre archivo y se extrae toda la info
    with open(path, 'r') as sim_file:
        raw_coordinates = sim_file.readlines()
    # Tienen en común los .txt de las simulaciones que las coorrdenadas empiezan en la linea 11 entonces se index
    raw_coordinates = raw_coordinates[11:]
    cen = True
    i = 0
    keyIndex = []
    # Se obtienen los indices de lista de la información que no nos interesa
    for i in range(len(raw_coordinates)):
        if 'PRINT U    NODAL SOLUTION PER NODE' in raw_coordinates[i]:
            keyIndex.append(i)
        elif '*** ANSYS - ENGINEERING' in raw_coordinates[i]:
            keyIndex.append(i)
        elif 'ANSYS Mechanical Enterprise' in raw_coordinates[i]:
            keyIndex.append(i)
        elif 'VERSION=WINDOWS x64' in raw_coordinates[i]:
            keyIndex.append(i)
        elif ' \n' == raw_coordinates[i] or '\n' == raw_coordinates[i] or '                              \n' in raw_coordinates[i]:
            keyIndex.append(i)
        elif '***** POST1 NODAL DEGREE OF FREEDOM LISTING *****' in raw_coordinates[i]:
            keyIndex.append(i)
        elif 'LOAD STEP=     1  SUBSTEP=     1' in raw_coordinates[i]:
            keyIndex.append(i)
        elif 'TIME=    1.0000      LOAD CASE=   0' in raw_coordinates[i]:
            keyIndex.append(i)
        elif 'THE FOLLOWING DEGREE OF FREEDOM RESULTS ARE IN THE GLOBAL COORDINATE SYSTEM' in raw_coordinates[i]:
            keyIndex.append(i)
        elif 'NODE       UX           UY           UZ           USUM' in raw_coordinates[i]:
            keyIndex.append(i)
    
    keyIndex = np.array(keyIndex)
    # Se recorren los indices y se usa pop() para eliminar la info que no interesa y se disminuye el indice en 1 porque las coordenadas
    # pierden tamaño en magnitud de 1
    for j in keyIndex:
        raw_coordinates.pop(j)
        keyIndex -= 1
    
    # Se indexan las ultimas 5 posiciones ya que no nos interesan y estan son comúnes en los .txt de simulación
    raw_coordinates = raw_coordinates[:-3]
    return raw_coordinates
    
# Función que organiza las coordenadas en tripletes de 3 con su notación científica
def find_numbers(raw_coordinates, op):
    lst = []
    # Se recorren todas las lineas de las coordenadas y se convierte la notación científica
    for coordinate in raw_coordinates:
        trip = separar_numeros(coordinate, op)
        if trip != []:
            lst.append(trip)
    # Se convierte la lista en array para poder plotear

    return np.array(lst)
