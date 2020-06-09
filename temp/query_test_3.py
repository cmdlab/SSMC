import numpy as np                                                              
from pymatgen import MPRester                                                   
import pymatgen.analysis.dimensionality as ana                                  
import ase.db                                                                   
from ase import Atoms                                                           
import time                                                                     

#------------------------------

E_hull_req = 0.0

#-----------------------------

f = open("Screening.txt","w")
                                                                                
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
                                                                                
#Defining some Empty Lists:
MX_Structures = []                                                                 
MX_sites = []
                                                                                
#Get all the structures for the Sulphides, Selenides and Tellurides:
for candidate in Candidates:                                                    
    MX_Structures.append(a.get_data(candidate,prop="structure"))                   

print('MX_dim  MX_form  MX_id  MO_dim  MO_form  MO_id  2DMX EHull')
# 1. Pick one initial structure:                                                                                
for row in MX_Structures:                                                          
    for entry in row:                                                           
        mpid = entry['material_id'] 
# 2. Find number of sites in the Structure:                                            
        MX_sites = a.get_data(mpid,prop="nsites")                                  
        if (MX_sites[0]['nsites']<50):                                             
            MX_dimension= ana.get_dimensionality_cheon(entry['structure'])                 
# 3. Check if M-X is layered:
            if (MX_dimension=='2D') or (MX_dimension=='1D'):
                MX_formula = a.get_data(mpid, prop="pretty_formula")
                form = MX_formula[0]['pretty_formula']
                In_formula = MX_formula[0]['pretty_formula']
# 4. Find the formula for the corresponding oxide:
                form = form.replace("Sc","ZZ")
                form = form.replace("Se","O")
                form = form.replace("Te","O")
                form = form.replace("S","O")
                form = form.replace("ZZ","Sc")
                Onsite = a.get_data(form,prop="nsites")
# 5. Find number of sites in the Oxide structure
                for material in Onsite:
                    if (material['nsites']<50):
                        O_struct = a.get_data(material['material_id'],prop="structure")
                        MO_dimension = ana.get_dimensionality_cheon(O_struct[0]['structure'])
# 6. Check if Oxide is layered
                        if (MO_dimension=='3D'):
#                            print(MX_dimension, In_formula, mpid, MO_dimension,form,material['material_id'])
                            Two_rows=db.select('formula='+In_formula)
                            for Two_material in Two_rows:
                                Two_formula = Two_material.formula
                                E_hull = Two_material.ehull
                                print(MX_dimension,In_formula,mpid,MO_dimension,form,material['material_id'],Two_formula,E_hull,file=f)
f.close()
