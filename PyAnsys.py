from ansys.mapdl.reader import read_binary
from glob import glob
import os
from tqdm import tqdm
import numpy as np

paths = glob(os.path.join('Here goes simulation .rst file location', '*.rst'))

for path in tqdm(paths):
    fn = os.path.splitext(os.path.basename(path))[0]
    result = read_binary(path)
    grid = result.grid
    _, disp = result.nodal_displacement(0)
    deformed = grid.copy()
    deformed.save (f'Here goes the destination of Not deformed shape/{fn}ND.vtk') 
    deformed.points += disp
    deformed.save(f'Here goes the destination of deformed shape/{fn}.vtk')
