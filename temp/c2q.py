import ase.db 
from ase import Atoms
import numpy as np

db = ase.db.connect('c2db.db')
rows = db.select('formula=GeSe2')
formula=[]
for row in rows:
    formula.append(row.formula)

print(formula)
