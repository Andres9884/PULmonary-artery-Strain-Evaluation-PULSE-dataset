import numpy as np
import re
import os

path = path = os.path.join('Patient01_Pressure15_ElasticModule200_.in')

# This function receives a string containing 3 numbers
def separar_numeros(linea, op):
    if op == 1: # Option 1 for NotDeformed model
        numeros = re.findall(r'[+-]?\d+\.\d+E[+-]?\d+', linea)
        return [float(num) for num in numeros]
    elif op == 2: # Option 2 for Deformed model
        numeros = re.findall(r'[+-]?\d+\.\d+E?[+-]?\d+', linea)
        # Returns a single node
        return [float(num) for num in numeros][:3]

# This function cleans trash strings in NotDeformed model
def get_coordinates(path):
    with open(path, 'r') as IN_line:
        raw_coordinates = IN_line.readlines()
    keyIndex = 0
    raw_coordinates = raw_coordinates[12:]
    cen = True
    i = 0
    # This line eliminate trash
    while cen:
        if 'N ,R5.3,LOC,     -1' in raw_coordinates[i]:
            keyIndex = i
            cen = False
        i += 1
    raw_coordinates = raw_coordinates[:keyIndex]
    return raw_coordinates

# This function organices each node in a list
def find_numbers(raw_coordinates, op):
    lst = []
    for coordinate in raw_coordinates:
        trip = separar_numeros(coordinate, op)
        if trip != []:
            lst.append(trip)
    return np.array(lst)

NotDeformedShape = find_numbers(get_coordinates(path), 1)
