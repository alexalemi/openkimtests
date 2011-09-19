""" This will serve as a test of using ASE
to drive LAMMPS
to drive KIM
"""

import ase
from ase.structure import bulk
from bin.lammps import LAMMPS

el1 = 'Cu'
slab = bulk(el1,'fcc',a=3.1)
slab = slab.repeat((5,5,5))


pair_style = "meam"
meamf = "meamf"
meamp = "meam.alsimgcufe"
subspec = [ el1 ]
pair_coeff = [ "* * meamf AlS SiS MgS CuS FeS "\
                   + meamp + " " + subspec[0] + "S " ]
parameters = { "pair_style" : pair_style, "pair_coeff" : pair_coeff }
files = [ meamf, meamp ]


calc = LAMMPS(parameters=parameters, specorder=subspec, tmp_dir = 'tmp',
              keep_tmp_files=True, keep_alive=False,files=files)

slab.set_calculator(calc)

print slab.get_potential_energy()


