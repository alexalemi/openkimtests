#! /usr/bin/env python

#import BaseTest and ase
from BaseTest import *

#import bin scripts, and sys for argv
import sys

#Test specific imports go here
from ase.structure import bulk
from ase import FIRE
from scipy import array
import scipy as sp

class VacancyTest(BaseTest):
    """Vacancy Test creates an FCC crystal with the computed lattice constant
        and then puts a vacancy in it, and returns the atomic positions, displacements
        and the vacancy formation energy.
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
       
        return slab, e_original, e_loss, e_final, array(disp_original), disp_field, slab.cell
        
    def getElasticConstants(self):
        """
        import FCCLattice
        fcclattice = FCCLattice.FCCLattice(self.potentialname,self.element)
        results = fcclattice.TestResults()
        """
        results = self.RequireTest('ElasticConstants')
        C11 = results['C11']
        C12 = results['C12']
        C44 = results['C44']
        
        return float(C11), float(C12), float(C44)


    def kspaceLattice(self,cell):
        
        S = sum(cell,0)
        
        N = 10
        
        kspace = sp.mgrid[ 0:N, 0:N, 0:N]
        
        kspace = sp.reshape( kspace, (3,  N**3  ) )
        kspace = kspace.T *  sp.pi/(2.0* S)
        
        return kspace

    def doGreenFunctionCalc(self,disp_original,disp_field,cell):
        
        C11, C12, C44 = self.getElasticConstants()
        
        C0 = 1.0/3 * ( C11 + 2 * C12 )
        
        kspace = self.kspaceLattice(cell)
        
        print "Inside the green function calc"
        
        kx = kspace[:,0]
        ky = kspace[:,1]
        kz = kspace[:,2]
        
        Q1,Q2,Q3,Q4,Q5,Q6 = [1,1,1,1,1,1]
        
        denom = 1.0/C0 * (C12*kx*kz + C44*kx*kz)*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) - \
            (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2)) - \
            (C12*ky*kz + C44*ky*kz)*(-((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz)) + \
            (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2)) + \
            (C44*kx**2 + C44*ky**2 + C11*kz**2)*(-(C12*kx*ky + C44*kx*ky)**2 + \
            (C44*kx**2 + C11*ky**2 + C44*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))
        
        xval = 1.0/denom * -1j*(kx*(-(C12*ky*kz + C44*ky*kz)**2 + (C44*kx**2 + C44*ky**2 + C11*kz**2)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*Q1 + \
            ky*((C12*kx*kz + C44*kx*kz)*(C12*ky*kz + C44*ky*kz) - (C12*kx*ky + C44*kx*ky)*(C44*kx**2 + C44*ky**2 + C11*kz**2))*\
            Q2 + kz*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) - \
            (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*Q3 + \
            kz*((C12*kx*kz + C44*kx*kz)*(C12*ky*kz + C44*ky*kz) - (C12*kx*ky + C44*kx*ky)*(C44*kx**2 + C44*ky**2 + C11*kz**2))*\
            Q4 + ky*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) -\
            (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*Q4 + \
            kx*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) - (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*\
            Q5 + kz*(-(C12*ky*kz + C44*ky*kz)**2 + (C44*kx**2 + C44*ky**2 + C11*kz**2)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*Q5 + \
            kx*((C12*kx*kz + C44*kx*kz)*(C12*ky*kz + C44*ky*kz) - (C12*kx*ky + C44*kx*ky)*(C44*kx**2 + C44*ky**2 + C11*kz**2))*\
            Q6 + ky*(-(C12*ky*kz + C44*ky*kz)**2 + (C44*kx**2 + C44*ky**2 + C11*kz**2)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*Q6)
       
        yval =  -1j*(kx*((C12*kx*kz + C44*kx*kz)*(C12*ky*kz + C44*ky*kz) - \
            (C12*kx*ky + C44*kx*ky)*(C44*kx**2 + C44*ky**2 + C11*kz**2))*Q1 + \
            ky*(-(C12*kx*kz + C44*kx*kz)**2 + (C44*kx**2 + C44*ky**2 + C11*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q2 + \
            kz*((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz) - (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*\
            Q3 + ky*((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz) -\
            (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q4 + \
            kz*(-(C12*kx*kz + C44*kx*kz)**2 + (C44*kx**2 + C44*ky**2 + C11*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q4 + \
            kz*((C12*kx*kz + C44*kx*kz)*(C12*ky*kz + C44*ky*kz) - (C12*kx*ky + C44*kx*ky)*(C44*kx**2 + C44*ky**2 + C11*kz**2))*\
            Q5 + kx*((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz) -\
            (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q5 + \
            ky*((C12*kx*kz + C44*kx*kz)*(C12*ky*kz + C44*ky*kz) - (C12*kx*ky + C44*kx*ky)*(C44*kx**2 + C44*ky**2 + C11*kz**2))*\
            Q6 + kx*(-(C12*kx*kz + C44*kx*kz)**2 + (C44*kx**2 + C44*ky**2 + C11*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q6)
              
        zval = -1j*(kx*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) - \
            (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*Q1 + \
            ky*((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz) - (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*\
            Q2 + kz*(-(C12*kx*ky + C44*kx*ky)**2 + (C44*kx**2 + C11*ky**2 + C44*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q3 + \
            kz*((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz) - (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*\
            Q4 + ky*(-(C12*kx*ky + C44*kx*ky)**2 + (C44*kx**2 + C11*ky**2 + C44*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q4 + \
            kz*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) - (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*\
            Q5 + kx*(-(C12*kx*ky + C44*kx*ky)**2 + (C44*kx**2 + C11*ky**2 + C44*kz**2)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q5 + \
            ky*((C12*kx*ky + C44*kx*ky)*(C12*ky*kz + C44*ky*kz) - (C12*kx*kz + C44*kx*kz)*(C44*kx**2 + C11*ky**2 + C44*kz**2))*\
            Q6 + kx*((C12*kx*ky + C44*kx*ky)*(C12*kx*kz + C44*kx*kz) -\
            (C12*ky*kz + C44*ky*kz)*(C11*kx**2 + C44*ky**2 + C44*kz**2))*Q6)
            
        kdisp = array([ xval, yval, zval ] ).T
               
        
        disp = sp.dot(   kdisp.T ,  sp.exp(  1j * sp.dot( kspace , disp_field.T ) ) ) 
        
               
        return disp
        
    def TestResults(self):
        """Required module, the TestResults Module returns a dictionary of result. 
        
        of the form { 'NameOfValue' : value, 'NameOfSecondValue' : secondvalue }
        
        This is where your test code goes.  Feel free to write other methods if necessary.
        """
        
        if self.potentialname == 'EMT':
            print "Not recommended to use EMT for this Test, takes too long, use ASAP instead"
            raise Exception("PotentialError")

        slab, e_original, e_loss, e_final, disp_original, disp_field, cell = self.createLattice()
        
        vacancyformation = e_final - e_original
        
        results = {'VacancyFormationEnergy': vacancyformation, "AtomPositions": disp_original.tolist(), 'DisplacementField': disp_field.tolist() } 
        
        self.doGreenFunctionCalc(disp_original, disp_field, cell) 
        

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
    
        
