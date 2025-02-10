import numpy as np
import re
import ICEM_COORDS
import os

path = os.path.join('Patient01_Pressure15_ElasticModule200_Sim.txt')
NotDeformed = ICEM_COORDS.NotDeformedShape 
# This function receives a string containing 3 numbers
def separar_numeros(linea, op):
    if op == 1: # Option 1 for NotDeformed model
        numeros = re.findall(r'[+-]?\d+\.\d+E[+-]?\d+', linea)
        return [float(num) for num in numeros]
    elif op == 2: # Option 2 for Deformed model
        numeros = re.findall(r'[+-]?\d+\.\d+E?[+-]?\d+', linea)
        # Returns a single node
        return [float(num) for num in numeros][:3]

# This function cleans trash string in Deformed model
def get_sim_coordinates(path):
    with open(path, 'r') as sim_file:
        raw_coordinates = sim_file.readlines()
    raw_coordinates = raw_coordinates[11:]
    cen = True
    i = 0
    keyIndex = []
    # Trash is eliminated using indexes that contains the trash position
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
    for j in keyIndex:
        raw_coordinates.pop(j)
        keyIndex -= 1
    raw_coordinates = raw_coordinates[:-3]
    return raw_coordinates

# This function organices each node in a list
def find_numbers(raw_coordinates, op):
    lst = []
    for coordinate in raw_coordinates:
        trip = separar_numeros(coordinate, op)
        if trip != []:
            lst.append(trip)
    return np.array(lst)

DeformedShape = find_numbers(get_sim_coordinates(path), 2) + NotDeformed # Deformed shape is obtained by adding displacemente to original model

print(NotDeformed[0:10])
print(DeformedShape[0:10])
