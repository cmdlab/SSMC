import numpy as np
from pymatgen import MPRester, Composition

mpr = MPRester()
data = mpr.query(criteria={"elements": ["Mo", "Se"], "nelements": 2}, 
                 properties=['formation_energy_per_atom', 'energy', 
                             'unit_cell_formula'])
print(len(data))
