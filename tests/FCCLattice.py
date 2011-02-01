#import BaseTest and ase
from BaseTest import *

#import bin scripts, and sys for argv
import sys

#Test specific imports
import scipy as sp
import pylab as py
from ase.structure import bulk
from scipy.optimize import fmin


class FCCLattice(BaseTest):
    """FCCLattice test returns the optimal fcc lattice constant and energy"""
    
    def __init__(self,potentialname,energy,TestDependencies=[],*args,**kwargs):
        BaseTest.__init__(self,potentialname,energy,TestDependencies,*args,**kwargs)
        #self.potential = self.getASEPotentialByName(potentialname)

    def FCCEnergy(self,a):
        """This function computes the energy of the crystal formation given 
        a certain lattice constant"""
        slab = bulk(self.element,'fcc',a=a)
        slab.set_calculator(self.potential)
        return slab.get_potential_energy()        


    def TestResults(self):
        """FCC Lattice Test Result"""
        
        x0 = 3.00
        minimum, energyminimum, iterations, funcalls, warnflag = fmin(self.FCCEnergy,x0,full_output=1,disp=0)
        if not warnflag:
            return minimum, energyminimum
        else:
            raise MinimizationError


    def Verify(self):
        print
        print "Verifying minimization with plot... "
        minimum, energyminimum = self.TestResults()
        vals = minimum* sp.linspace(0.9,1.1,100)
        ens = map(self.FCCEnergy, vals)
        py.figure(1)
        py.clf()
        py.title('Energy minimization verification')
        py.xlabel('Lattice constant (ang)')
        py.ylabel('Energy (eV)')
        py.plot(vals,ens)
        py.plot(minimum,energyminimum,'r+')
            
        
        
if __name__ == '__main__':
    test = FCCLattice(sys.argv[1],sys.argv[2],sys.argv[3:])
    print test.main()
    
        
