#! /usr/bin/env python

#import BaseTest and ase
from _BaseTest import *

#Test specific imports
import scipy as sp
import pylab as py
from ase.structure import bulk
from scipy.optimize import fmin


class FCCLattice(BaseTest):
    """FCCLattice test returns the optimal fcc lattice constant and energy per atom"""
    
    def FCCEnergy(self,a):
        """This function computes the energy of the crystal formation given 
        a certain lattice constant
        
        It uses the ase helper function bulk to create a 1 atom periodic boundary
        condition crystal with a specific structure"""
        self.slab = bulk(self.element,'fcc',a=a)
        if self.potentialname == 'ASAP':
            self.slab = self.slab.repeat((10,10,10))

        #set the calculator
        self.slab.set_calculator(self.calculator)
        
        #calculate and return the potential energy
        return self.slab.get_potential_energy()        


    def results(self):
        """FCC Lattice Test Result
        
        uses scipy fmin (a simplex method minimization tool), to find the optimal
        lattice constant, and corresponding energy per atom"""
        
        #choose a reasonable starting constant
        x0 = 3.00
        
        #minimize the energy per atom, using scipy fmin simplex minimizer.
        minimum, energyminimum, iterations, funcalls, warnflag = fmin(self.FCCEnergy,x0,full_output=1,disp=0)
        
        #ensure that the minimization performed as expected
        if not warnflag:
            return {'FCCLatticeConstant':minimum[0], 'FCCEnergyPerAtom':energyminimum}
        else:
            raise MinimizationError


    def verify(self):
        """Simple verification script.  Creates a plot that shows the 
        crystal energy in the neighborhood of the computed minimum, along
        with the computed minimum, as a check """
        
        print
        print "Verifying minimization with plot... "
        resultsdict = self.TestResults()
        minimum = resultsdict['FCCLatticeConstant']
        energyminimum = resultsdict['FCCEnergyPerAtom']
        vals = minimum * sp.linspace(0.9,1.1,100)
        ens = map(self.FCCEnergy, vals)
        py.figure(1)
        py.clf()
        py.title('Energy minimization verification')
        py.xlabel('Lattice constant (ang)')
        py.ylabel('Energy (eV)')
        py.plot(vals,ens)
        py.plot(minimum,energyminimum,'r+')
        py.show()
            
        
#Ensures the script can be called from the command line
if __name__ == '__main__':
    test = FCCLattice(args.potential,args.element,verify=args.verify,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
