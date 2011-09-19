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
from scipy import dot, array, linspace
import numpy as np
from scipy.linalg import inv


class ElasticConstants(BaseTest):
    """This test computes the 6 elastic constants"""
    
    def __init__(self,potentialname,element,TestDependencies=[],*args,**kwargs):
        """Pass the initialization arguments to the BaseTest initializer"""
        TestDependencies = ['FCCLattice']
        BaseTest.__init__(self,potentialname,element,TestDependencies,*args,**kwargs)
        #self.potential = self.getASEPotentialByName(potentialname)

    def FCCEnergy(self,a):
        """This function computes the energy of the crystal formation given 
        a certain lattice constant
        
        It uses the ase helper function bulk to create a 1 atom periodic boundary
        condition crystal with a specific structure"""
        slab = bulk(self.element,'fcc',a=a,cubic=True)
        if self.potentialname == "ASAP":
            slab = slab.repeat((10,10,10))
        self.volume = slab.get_volume()
        
        #set the calculator
        slab.set_calculator(self.potential)
       
        #calculate and return the potential energy
        return slab.get_potential_energy(), slab.get_volume()

    def Strains(self,x,ind):
        
        if ind == 0:
            return [ x, x, 0 , 0 ,0 ,0 ]
        elif ind == 1:
            return [ x ,x , -x*(2.0 + x )/(1 + x)**2, 0 ,0 ,0 ]
        elif ind == 2:
            return [ 0, 0, x ,0 ,0, 0]
        elif ind == 3:
            return [ ( (1 + x ) /( 1 - x) )**(0.5) - 1,  ( (1-x)/(1+x) )**(0.5) - 1, 0, 0, 0, 0]
        elif ind == 4:
            return [ 0, 0, x**2/4.0, x, x ,0 ]
            
        elif ind == 5:
            return [ (1 + x**2/4.0)**(0.5) - 1 , (1 + x**2/4.0)**(0.5) - 1 , 0, 0, 0, x]
        
        else:
            print "Index not understood "
            raise "BadIndex"    


    def ConstructStrainTensor(self,es):
        e1,e2,e3,e4,e5,e6 = es
        
        e = array( [[ e1, e6/2.0, e3/2.0], [e6/2.0, e2, e4/2.0], [e5/2.0, e4/2.0, e3] ] )
        
        return e
         

    def FCCTensileLoaded(self, strain):
        slab = bulk(self.element,'fcc',a=self.a, cubic=True)
        if self.potentialname == 'ASAP':
            slab = slab.repeat((10,10,10))
        
        #set the calculator
        slab.set_calculator(self.potential)
  
        #set boundaries

        deltacell = dot( strain, slab.cell )

        
        
        slab.set_cell( slab.cell + deltacell  , scale_atoms=True)
        

        return slab.get_potential_energy(), slab.get_volume()
        
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




    def runaFit(self,ind):
        
        self.eps = 0.000001
        
        xs = linspace(0,self.eps,10)
        
        posstrains = []
        negstrains = []
        for x in xs:
            posstrains.append( self.Strains( x, ind) )
            negstrains.append( self.Strains( -x, ind) )
            
        postensors = map( self.ConstructStrainTensor , posstrains)
        negtensors = map( self.ConstructStrainTensor, negstrains)
                
        posenergies = []
        posvolumes = []
        
        negenergies= []
        negvolumes = []
        
        
        for tensor in postensors:
            energy, volume = self.FCCTensileLoaded( tensor )
            posenergies.append(energy)
            posvolumes.append(volume)
            
        for tensor in negtensors:
            energy, volume = self.FCCTensileLoaded( tensor )
            negenergies.append(energy)
            negvolumes.append(volume)
            
        energies=  (array(posenergies) + array(negenergies))/2
        volumes = ( array(posvolumes) + array(negvolumes) )/2
        
        volume = posvolumes[0]
        
        
        ydat = energies/volumes
        
         
        fit = np.polyfit( xs, ydat, 2)
        
        print "The fit coefficients are: "
        print fit
        
        coeffx2 = fit[0]
        
        #Plot to verify
        
        py.figure(1)
        py.plot( xs, ydat, 'r+')
        poly = np.poly1d(fit)
        
        filledx = linspace(0,self.eps,100)
        py.plot(filledx, poly(filledx), 'g--')
        py.show()     
        
        
        return coeffx2


    def findConstants(self):
    
        #Find the quadratic coefficients for each direction
        coeffs = np.zeros(6)
        
        for i in range(6): 
            coeffs[i] = self.runaFit(i)
        
        
        #Find the transformation matrix
        transform = inv( array( [ [ 1,1,0,0,0,0] , [1,1,2,-4,0,0] , [0,0,0,1,0,0], [1,-1,0,0,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1] ]) )
        
        elasticconstants = dot( transform, coeffs) 
        
        
        print
        print "ELASTIC CONSTANTS SHOULD BE: "
        print elasticconstants
        
        
        return elasticconstants



    def TestResults(self):
        """FCC Lattice Test Result
        
        uses scipy fmin (a simplex method minimization tool), to find the optimal
        lattice constant, and corresponding energy per atom"""
        
        self.a = self.getFCCLattice()
        
        results = {}
        #choose a reasonable starting constant

        from ase.units import GPa

        C11,C12,C13,C33,C44,C66 = self.findConstants()/GPa

        results['BulkModulus'] = 1.0/3 * ( C11 + 2 * C12 )
        results['C11'] = C11
        results['C12'] = C12
        results['C13'] = C13
        results['C33'] = C33
        results['C44'] = C44
        results['C66'] = C66

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
        
    test = ElasticConstants(args.potential,args.element,verify=args.verify,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
