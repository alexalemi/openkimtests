#! /usr/bin/env python

#import BaseTest and ase
from _BaseTest import *

#Test specific imports
import scipy as sp
import pylab as py
from ase.structure import bulk
from scipy.optimize import fmin
from ase import FIRE

class FCCVacancy(BaseTest):
    """FCCVacancy test returns the vacancy formation energy"""
    def results(self):
	a = request(self.potentialname,self.element,'FCCLattice','FCCLatticeConstant')
	self.slab = bulk(self.element,'fcc',a=a,cubic=True)
	
	#repeat the cell 8 times
	self.slab = self.slab.repeat((8,8,8))

	self.slab.set_calculator(self.calculator)
	
	energy1 = self.slab.get_potential_energy()
	volume1 = self.slab.get_volume()
	Natoms1 = len(self.slab)

	#remove an atom
	del self.slab[0]
	
	#attach calculator again
	self.slab.set_calculator(self.calculator)
	
	energy2 = self.slab.get_potential_energy()
	volume2 = self.slab.get_volume()
	Natoms2 = len(self.slab)

	#relax the crystal using FIRE
	dyn = FIRE(self.slab)
	dyn.run(fmax=0.01)

	energy3 = self.slab.get_potential_energy()
	volume3 = self.slab.get_volume()
	Natoms3 = len(self.slab)

	vacancy_formation_energy = energy3 - (Natoms1 - 1.)/(1.*Natoms1) * energy1

	results_dict = { 'VacancyFormationEnergy' : vacancy_formation_energy,
			 'NAtoms': Natoms1 }

	return results_dict	

#Ensures the script can be called from the command line
if __name__ == '__main__':
    test = FCCVacancy(args.potential,args.element,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
