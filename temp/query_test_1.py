import numpy as np
from pymatgen import MPRester
import ase.db                                                                   
from ase import Atoms                                                           

#importing C2DB                                                           
db = ase.db.connect('c2db.db')

#Connecting to Materials Project
a = MPRester("ipKWB3wlJ5FgAV4L")                                                  

#Create the search list:
Metals = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Y','Zr','Nb','Mo','Tc',\
'Ru','Rh','Pd','Ag','Hf','Ta','W','Re','Os','Ir','Pt','Au']
Ogroup = ['S','Se','Te']
Candidates = []
for M in Metals:
    for X in Ogroup:
        Candidates.append(M+'-'+X)
#print(Candidates)

TDforms = []
dummy = []
for candidate in Candidates:
    TDforms.append(a.get_data(candidate,prop="pretty_formula"))
#        dummy.append('formula='+Candidates[i])

#for candidate in Candidates:
#   if (a.get_data(candidate,prop="pretty_formula") != []): 
#    TDforms.append(a.get_data(candidate, prop="structure"))

print(TDforms)
#print('3D forms')
#print(dummy)

#formula = []
#for x in dummy:
#    rows = db.select(x)                                               
#    for row in rows:                                                                
#        formula.append(row.formula)                                                   
                                                                                
#print('2D forms')
#print(formula)

#for i in print(energy)        

