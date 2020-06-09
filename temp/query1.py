from pymatgen import MPRester
from pprint import pprint

a = MPRester("ipKWB3wlJ5FgAV4L")

#pprint(a.get_data("Li2O", prop="structure"))
#entries = a.get_entries_in_chemsys(['Sc','S'])
Ogroup = ['S','Se']
search = []
for x in Ogroup:
    search.append('Sc-'+x)
dummy = []
for x in search:    
    dummy = a.get_data(x,prop=("pretty_formula","energy"))
    pprint(dummy)
