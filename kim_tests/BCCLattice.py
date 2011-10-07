#! /usr/bin/env python

#import BaseTest and ase
from _BaseTest import *

#Test specific imports
import scipy as sp
import pylab as py
from ase.structure import bulk
from scipy.optimize import fmin


class BCCLattice(BaseTest):
    """BCCLattice test returns the optimal fcc lattice constant and energy per atom"""
    
    def BCCEnergy(self,a):
        """This function computes the energy of the crystal formation given 
        a certain lattice constant
        
        It uses the ase helper function bulk to create a 1 atom periodic boundary
        condition crystal with a specific structure"""
        self.slab = bulk(self.element,'bcc',a=a)
        if self.potentialname.lower() == 'asap':
            self.slab = self.slab.repeat((10,10,10))

        #set the calculator
        self.slab.set_calculator(self.calculator)
        
        #calculate and return the potential energy
        return self.slab.get_potential_energy()        


    def results(self):
        """BCC Lattice Test Result
        
        uses scipy fmin (a simplex method minimization tool), to find the optimal
        lattice constant, and corresponding energy per atom"""
        
        #choose a reasonable starting constant
        x0 = 3.00
        
        #minimize the energy per atom, using scipy fmin simplex minimizer.
        minimum, energyminimum, iterations, funcalls, warnflag = fmin(self.BCCEnergy,x0,full_output=1,disp=0)
        
        #ensure that the minimization performed as expected
        if not warnflag:
            return {'BCCLatticeConstant':minimum[0], 'BCCEnergyPerAtom':energyminimum}
        else:
            raise Exception('MinimizationError')
            
        
#Ensures the script can be called from the command line
if __name__ == '__main__':
    test = BCCLattice(args.potential,args.element,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
