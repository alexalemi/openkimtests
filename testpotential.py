""" This will serve as a test of using ASE
to drive LAMMPS
to drive KIM
"""

import ase
from ase.structure import bulk
from bin.potential import KIM_loader


el1 = 'Ar'
slab = bulk(el1,'fcc',a=3.1)
slab = slab.repeat((5,5,5))



calc = KIM_loader('model_Ar_P_MLJ_NEIGH_PURE_H_F',el1,slab=slab)

slab.set_calculator(calc)

print slab.get_potential_energy()


