=============
Openkim-Tests
=============

A test is a collection of ASE code that get run over and over,
with different elements and different calculators attached.


MinimalTest
-----------

For example, consider openkimtests.kim_tests.\_MinimalTest::

	#! /usr/bin/env python
	from _BaseTest import *

	#request method available as
	#	request(potential,element,test,resultentry)
	#logger available

	class MinimalTest(BaseTest):
		""" This example serves as a minimal example of a test
				Notes:
					* Place slab in self.slab
					* calculator available at self.calculator """

		def results(self):
			""" This method computes the results as a dictionary """

			results = {'answer':42}

			return results


		
	if __name__ == "__main__":
	    test = MinimalTest(args.potential,args.element,verify=args.verify,write=args.write)
	    #raises BaseTest.main
	    print test.main()

A few things to note:
	* We've inherited from \_BaseTest, this does a lot of the heavy lifting.
	* We have a request(potential,element,test,resultentry) method to request other test results
	* We should put our slab in self.slab
	* We can access the calculator at self.calculator
	* We need a results method, which returns a python dictionary of results
	* The if name block at the end ensures we can call it from the command line.

FCCLattice
----------

As a less trivial example, lets consider FCCLattice::

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
	        if self.potentialname.lower() == 'asap':
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
	            raise Exception('MinimizationError')
	            
	        
	#Ensures the script can be called from the command line
	if __name__ == '__main__':
	    test = FCCLattice(args.potential,args.element,write=args.write)
	    #raises BaseTest.main
	    print test.main()
    
        
This test uses fmin to compute the FCCLattice constant of a one atom bulk block.  It returns the lattice constant as well as the energy per atom as results.  Note that ASAP requires a minimal box size, so if we have been called with the ASAP potential, it repeats the cell a few times.