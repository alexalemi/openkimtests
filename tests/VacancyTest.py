#! /usr/bin/env python

#import BaseTest and ase
from BaseTest import *

#import bin scripts, and sys for argv
import sys

#Test specific imports go here
from ase.structure import bulk
from ase import FIRE
from scipy import array

class VacancyTest(BaseTest):
    """NullTest does nothing, but serves as an example test.
    
        It inherits its functionality from BaseTest, and serves as a template for future
    tests.  

    Simply copy NullTest.py, and rename the file, and class name, and rewrite TestResults
    """
    
    def __init__(self,potentialname,energy,TestDependencies=[],*args,**kwargs):
        #Passes the initialization arguments to the BaseTest initialization
        BaseTest.__init__(self,potentialname,energy,TestDependencies,*args,**kwargs)


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

    def createLattice(self):
        """Create the slab used for the vacancy calculation.  Find energy, and get
            displacement field, create a vacancy, relax, and return the new displacement
            field and lattice energy
        """
        a = self.getFCCLattice()
        slab = bulk(self.element,'fcc',a=a)
        slab = slab.repeat((10,10,10))
        slab.set_calculator(self.potential)
        #get the original crystal energy
        e_original = slab.get_potential_energy()
        del slab[0]
        
        slab.set_calculator(self.potential)
        
        #get the energy of the crystal with a hole before relaxation
        e_loss = slab.get_potential_energy()
        
        #get the displacement field of the original crystal for all of the atoms
        disp_original = slab.get_positions()
        
        
        #Do the dynamics with FIRE
        dyn = FIRE(slab)
        dyn.run(fmax=0.0001)

        e_final = slab.get_potential_energy()
        disp_final = slab.get_positions()
        
        disp_field = array(disp_final) - array(disp_original)
       
        return slab, e_original, e_loss, e_final, array(disp_original), disp_field
        
        
    def TestResults(self):
        """Required module, the TestResults Module returns a dictionary of result. 
        
        of the form { 'NameOfValue' : value, 'NameOfSecondValue' : secondvalue }
        
        This is where your test code goes.  Feel free to write other methods if necessary.
        """
        
        if self.potentialname == 'EMT':
            print "Not recommended to use EMT for this Test, takes too long, use ASAP instead"
            raise "PotentialError"
        
        slab, e_original, e_loss, e_final, disp_original, disp_field = self.createLattice()
        
        vacancyformation = e_final - e_original
        
        results = {'VacancyFormationEnergy': vacancyformation, "AtomPositions": disp_original.tolist(), 'DisplacementField': disp_field.tolist() } 

        return results


    def Verify(self):
        """ Optional verify script to be used to generate a visual output for
        
        quick check that everything is going alright"""
        pass
            
        
#The following ensures that the test can be called from the command line
if __name__ == '__main__':
    #Make sure you change the NullTest in the next line.
    test = VacancyTest(args.potential,args.element,verify=args.verify,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
