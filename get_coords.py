# Tests
in_route = "Here goes .in location"
sim_route = "Here goes simulation result .txt location"
import os
from glob import glob
from tqdm import tqdm
import numpy as np
import file_lecture as fl
import csv


def getNotDeformedCoors(in_route):
    ND = fl.find_numbers(fl.get_coordinates(in_route), 1)
    return ND

def getDeformedCoors(sim_route, ND):
    D = fl.find_numbers(fl.get_sim_coordinates(sim_route), 2) + ND
    return D

ND = getNotDeformedCoors(in_route)
D = getDeformedCoors(sim_route, ND)    


with open('Here goes the destination of Not Deformed shape', 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(['x', 'y', 'z'])
    escritor.writerows(ND)

with open('Here goes the destination of Deformed shape', 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(['x', 'y', 'z'])
    escritor.writerows(D)
