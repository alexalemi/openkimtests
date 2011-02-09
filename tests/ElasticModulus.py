#! /usr/bin/env python

#import BaseTest and ase
from BaseTest import *

#import bin scripts, and sys for argv
import sys

#Test specific imports
import scipy as sp
import pylab as py
from ase.structure import bulk
from scipy.optimize import fmin


class ElasticModulus(BaseTest):
    """ElasticModulus test returns the elastic moduli"""
    
    def __init__(self,potentialname,element,TestDependencies=[],*args,**kwargs):
        """Pass the initialization arguments to the BaseTest initializer"""
        BaseTest.__init__(self,potentialname,element,TestDependencies,*args,**kwargs)
        #self.potential = self.getASEPotentialByName(potentialname)

    def FCCEnergy(self,a):
        """This function computes the energy of the crystal formation given 
        a certain lattice constant
        
        It uses the ase helper function bulk to create a 1 atom periodic boundary
        condition crystal with a specific structure"""
        slab = bulk(self.element,'fcc',a=a,cubic=True)
        self.volume = slab.get_volume()
        
        #set the calculator
        slab.set_calculator(self.potential)
       
        #calculate and return the potential energy
        return slab.get_potential_energy()

    def FCCTensileLoaded(self, side):
        slab = bulk(self.element,'fcc',a=self.a, cubic=True)
        #set the calculator
        slab.set_calculator(self.potential)
  
        #set boundaries
        slab.set_cell([slab.cell[0]*(1.0+self.eps), slab.cell[1]*side,
            slab.cell[2]*side], scale_atoms=True)

        return slab.get_potential_energy()
        
    def getFCCLattice(self):
        """
        import FCCLattice
        fcclattice = FCCLattice.FCCLattice(self.potentialname,self.element)
        results = fcclattice.TestResults()
        """
        results = self.RequireTest('FCCLattice')
        a = results['FCCLatticeConstant']
        print "Using a=", a
        return float(a)

    def TestResults(self):
        """FCC Lattice Test Result
        
        uses scipy fmin (a simplex method minimization tool), to find the optimal
        lattice constant, and corresponding energy per atom"""
        
        results = {}
        #choose a reasonable starting constant
        x0 = self.getFCCLattice()
        self.a = x0
        self.eps = 0.01

        energyoriginal = self.FCCEnergy(x0)

        #minimize the energy per atom, using scipy fmin simplex minimizer.
        minimum, energyminimum, iterations, funcalls, warnflag = fmin(self.FCCTensileLoaded,1.0,full_output=1,disp=0)
      
        energydiff = energyminimum-energyoriginal

        E = 2.0 * energydiff / self.eps**2 / self.volume

        from ase.units import *

        #ensure that the minimization performed as expected
        if not warnflag:
            results['YoungsModulus'] = E/GPa
            results['PoissonRatio'] = (1.0-minimum[0])/self.eps
        else:
            raise MinimizationError

        energydiff = self.FCCEnergy(x0*(1.0-self.eps))-self.FCCEnergy(x0)
        K = 2.0*energydiff/(3*self.eps)**2/self.volume
        results['BulkModulus'] = K/GPa

        return results

    def Verify(self):
        print
        print "Verifying numbers... "
        resultsdict = self.TestResults()
        E = resultsdict['YoungsModulus']
        print E, 'GPa'
        K = resultsdict['BulkModulus']
        print K, 'GPa'
        nu = resultsdict['PoissonRatio']
        print nu, ' compared to ', (3*K-E)/6/K
        
#Ensures the script can be called from the command line
if __name__ == '__main__':
    potential = args.potential
    element = args.element
    TestDependencies = args.TestDependencies
    
    test = ElasticModulus(args.potential,args.element,args.TestDependencies,verify=args.verify,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
