import numpy as np
import re
import os

# Function to separate numbers from the line
def separar_numeros(linea, op):
    # Uses a regular expression to detect numbers in scientific notation
    # Option 1 is to filter the coordinates of the .in file without simulation
    if op == 1:
        numeros = re.findall(r'[+-]?\d+\.\d+E[+-]?\d+', linea)
        return [float(num) for num in numeros]
    # Option 2 is to filter the coordinates of the file after simulation
    elif op == 2:
        numeros = re.findall(r'[+-]?\d+\.\d+E?[+-]?\d+', linea)

        return [float(num) for num in numeros][:3]

# Function that extracts coordinates from .in files
def get_coordinates(path):
    # Open the .txt file
    with open(path, 'r') as IN_line:
        raw_coordinates = IN_line.readlines()
    keyIndex = 0
    # All IN files have in common that the list of nodes starts at coordinate 13
    raw_coordinates = raw_coordinates[12:]
    cen = True
    i = 0
    # Iterate through the .txt until the text N ,R5.3,LOC,     -1 is found, which is after the coordinates
    while cen:
        if 'N ,R5.3,LOC,     -1' in raw_coordinates[i]:
            keyIndex = i
            cen = False
        i += 1
    # Index the coordinates with the index found during the iteration
    raw_coordinates = raw_coordinates[:keyIndex]
    return raw_coordinates

# Function that extracts coordinates from simulation files
def get_sim_coordinates(path):
    # Open the file and extract all the information
    with open(path, 'r') as sim_file:
        raw_coordinates = sim_file.readlines()
    # Simulation .txt files have in common that the coordinates start at line 11, so they are indexed
    raw_coordinates = raw_coordinates[11:]
    cen = True
    i = 0
    keyIndex = []
    # Get the list indices of the information we are not interested in
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
    # Iterate through the indices and use pop() to remove the information we are not interested in,
    # and decrease the index by 1 because the coordinates shrink in size by 1
    for j in keyIndex:
        raw_coordinates.pop(j)
        keyIndex -= 1
    
    # Index the last 3 positions since we are not interested in them and they are common in the simulation .txt files
    raw_coordinates = raw_coordinates[:-3]
    return raw_coordinates
    
# Function that organizes the coordinates into triplets of 3 with their scientific notation
def find_numbers(raw_coordinates, op):
    lst = []
    # Iterate through all the coordinate lines and convert the scientific notation
    for coordinate in raw_coordinates:
        trip = separar_numeros(coordinate, op)
        if trip != []:
            lst.append(trip)
    # Convert the list to an array to be able to plot

    return np.array(lst)
