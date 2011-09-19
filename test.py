""" This will serve as a test of using ASE
to drive LAMMPS
to drive KIM
"""

import ase
from ase.structure import bulk
from ase.calculators.lammps import LAMMPS

el1 = 'Fe'
slab = bulk(el1,'fcc',a=3.1)
slab = slab.repeat((5,5,5))


pair_style = "pair_KIM model_Al_PF_ErcolessiAdams Al"
subspec = [ el1 ]


parameters = { "pair_style" : pair_style, 'pair_coeff' : ['* *'], 'mass': ['1 26.981539'] }


calc = LAMMPS(parameters=parameters, specorder=subspec, tmp_dir = 'tmp',
              keep_tmp_files=True, keep_alive=False)

slab.set_calculator(calc)

print slab.get_potential_energy()


