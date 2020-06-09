import numpy as np                                                              
from pymatgen import MPRester                                                   
import pymatgen.analysis.dimensionality as ana
import ase.db                                                                   
from ase import Atoms                                                           
import time
                                                                                
#importing C2DB                                                                 
db = ase.db.connect('c2db.db')                                                  
                                                                                
#Connecting to Materials Project                                                
a = MPRester("ipKWB3wlJ5FgAV4L")                                                
                                                                                
#Create the search list:                                                        
Metals = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Y','Zr','Nb','Mo','Tc', 
'Ru','Rh','Pd','Ag','Hf','Ta','W','Re','Os','Ir','Pt','Au']                     
Ogroup = ['S','Se','Te']                                                        
Candidates = []                                                                 
for M in Metals:                                                                
    for X in Ogroup:                                                            
        Candidates.append(M+'-'+X)                                              
                                                                                
mpid  = []
structures = []
sites = []

for candidate in Candidates:
    structures.append(a.get_data(candidate,prop="structure"))

nsite=[]

for row in structures:
    for entry in row:
        mpid = entry['material_id']
        nsite = a.get_data(mpid,prop="nsites")
        if (nsite[0]['nsites']<50):
            k= ana.get_dimensionality_cheon(entry['structure'])
            if (k=='2D') or (k==1D):
                formula = a.get_data(mpid,prop="pretty_formula")
                form = formula[0]['pretty_formula']
                form.replace("Se","O")
                form.replace("Te","O")
                form.replace("S","O")
                print(k, form)


#print(dimension[0][2])
#for structure in Structures:
    
#print (ana.get_dimensionality_cheon(TDforms[1][0]))
#for i in range(1,10,1):
#    for entry in TDforms[i]:
#        k = ana.get_dimensionality_cheon(entry)
#        print (k)
                                                                                
#for candidate in Candidates:                                                   
#   if (a.get_data(candidate,prop="pretty_formula") != []):                     
#    TDforms.append(a.get_data(candidate, prop="structure"))                    
                                                                                
#print(TDforms)                                                                  
#print('3D forms')                                                              
#print(dummy)                                                                   
                                                                                
#formula = []                                                                   
#for x in dummy:                                                                
#    rows = db.select(x)                                                        
#    for row in rows:                                                                
#        formula.append(row.formula)                                                   
                                                                                
#print('2D forms')                                                              
#print(formula)                                                                 
                                                                                
#for i in print(energy)                                                         i
