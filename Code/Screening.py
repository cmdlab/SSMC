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
                                                                                

def layered_MX_bulk(M):
    """
    Parameters:
    
    M(String): Elemental symbol of the Metal for which Sulphides and
    selenides are being queried

    Returns:
    
    output(list): returns[formula(String),dimension(String),icsd_ids(list),mpid(String)]
    of the metal sulphides and selenides

    """

    Anions = ['S','Se','Te']
    Candidates = []
    output = []
    for anion in Anions:
        Candidates.append(M+'-'+anion)
    for candidate in Candidates:
        formula = a.get_data(candidate,prop="pretty_formula")
        for entries in formula:
            mpid = entries['material_id']
            icsd = a.get_data(mpid,prop="icsd_ids")
            nsites = a.get_data(mpid,prop="nsites")
            nsite = nsites[0]['nsites']
            if (icsd[0]['icsd_ids'] != []) and (nsite<50):
                structure = a.get_data(mpid,prop="structure")
                try:
                    dimension = ana.get_dimensionality_cheon(structure[0]['structure'])
                except ZeroDivisionError:
                    print('Oops')
                if (dimension == '2D') or (dimension == '1D'):
                    results = [entries['pretty_formula'],dimension,icsd[0]['icsd_ids'],mpid]
                    output.append(results)
    return(output)

def layered_oxide(M, switch):
    """
    Parameters: 
    
    M(String): Elemental symbol of the Metal for which Sulphides and            
    selenides are being queried                                                 
                                                                                
    Returns:                                                                    
                                                                                
    count(int): The number of layered oxides of the metal
    """

    formula = a.get_data(M+'-O',prop="pretty_formula")
    count = 0
    for entry in formula:
        mpid = entry['material_id']                                       
        icsd = a.get_data(mpid,prop="icsd_ids")                             
        nsites = a.get_data(mpid,prop="nsites")                             
        nsite = nsites[0]['nsites']                                         
        if (icsd[0]['icsd_ids'] != []) and (nsite<50):                      
            structure = a.get_data(mpid,prop="structure")
            try:                       
                dimension = ana.get_dimensionality_cheon(structure[0]['structure'])
            except ZeroDivisionError:
                print('Oops')       
            if (dimension == '2D') or (dimension == '1D'):
                count = count + 1
                if (switch==1):
                    print(entry['pretty_formula'],dimension,icsd[0]['icsd_ids'],mpid,file=f)
    return(count)
           

#Create the search list:                                                        
Metals = ['Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Y','Zr','Nb','Mo','Tc',  
'Ru','Rh','Pd','Ag','Hf','Ta','W','Re','Os','Ir','Pt','Au'] 

#Metals = ['Hf','Ta','W','Re','Os','Ir','Pt','Au'] 
#Metals =['Ni','Hg','Pb','Sn']
#Metals = ['Ge','Hf']

for M in Metals:
    number_of_2D_oxides = layered_oxide(M,1)
    print(M+' has '+str(number_of_2D_oxides)+' layered oxides',file=f)
    if (number_of_2D_oxides == 0):
        MX_bulk = layered_MX_bulk(M)
        if(MX_bulk != []):
            print('The Candidates for '+M+' are:',file=f)
        for entry in MX_bulk:
            MX_2D = db.select('formula='+entry[0])           
            for material in MX_2D:                       
                Formula = material.formula              
                E_hull = material.ehull
                if(E_hull>E_hull_req):
                    print(entry,'Ehull ='+str(E_hull)+' eV',file=f)
                             
