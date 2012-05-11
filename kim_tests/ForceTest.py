#! /usr/bin/env python

from _BaseTest import *


#request method available, as
# 	request(potential,element,test,resultentry)
#logger available

import scipy
import numpy
import ase
from ase.lattice.cubic import FaceCenteredCubic


class ForceTest(BaseTest):
    """  tests whether the forces returned by a given potential are consistent with F = -grad E """

    def getFCCLattice(self):
        """
        use FCCLattice as basis for lattice constant
        """
        a = request(self.potentialname,self.element,'FCCLattice','FCCLatticeConstant')
        print "Using a=", a
        return float(a)

    def makeRandomPositions(self,N=10):
        """
        to make a random configuration of N atoms
        """
        a = self.getFCCLattice()
        # use random number generator to make random positions spaced "a" apart
        positions = scipy.zeros((N,3))
        atom_loc = [0.,0.,0.]
        for i in range(1,N):
                vector = 2*a*scipy.random.randn(3)
                atom_loc = atom_loc + vector
                positions[i]=atom_loc

        return positions


    def makePerturbedLattice(self, shape=(2,2,2)):
        """
        to make perturbed bulk structure lattice positions
        """
        a = self.getFCCLattice()
        slab = FaceCenteredCubic(size = shape, symbol=self.element, latticeconstant=a)
        positions=slab.get_positions()

        perturbations = numpy.random.standard_normal(scipy.shape(positions))*a*0.05

        positions += perturbations

        return positions

    def getPotential(self,atoms_list,positions):
        """
        to get the potential energy as a function of position
        """

        atoms = ase.Atoms(atoms_list,positions)
        atoms.set_calculator(self.calculator)
        potential = atoms.get_potential_energy()

        return potential

    def gradE(self,positions,step_size=None):
        """
        this is to calculate the gradient of the potential energy, 
        """

        a = self.getFCCLattice()

        if step_size is None:
                step_size = 10**(-5)*a # optimal step size for symmetric derivative

        atoms_list = [self.element for i in range(0,len(positions))]

        # need to perturb all atoms in all x-y-z directions

        gradE = scipy.zeros((len(positions),3))

        for i in range(0,len(positions)):

                perturb = scipy.zeros((len(positions),3))
                perturb[i] = scipy.array([1.,0.,0.])*step_size

        # need to perturb in x-y-z directions FOR ALL ATOMS!!!

                pe_x1 = self.getPotential(atoms_list, positions+perturb)
                pe_x2 = self.getPotential(atoms_list, positions-perturb)

                gradE_x = (pe_x1-pe_x2)/(2*step_size)

                perturb[i]=scipy.array([0.,1.,0.])*step_size

                pe_y1 = self.getPotential(atoms_list, positions+perturb)
                pe_y2 = self.getPotential(atoms_list, positions-perturb)

                gradE_y = (pe_y1-pe_y2)/(2*step_size)

                perturb[i] = scipy.array([0.,0.,1.])*step_size

                pe_z1 = self.getPotential(atoms_list,positions+perturb)
                pe_z2 = self.getPotential(atoms_list,positions-perturb)

                gradE_z = (pe_z1-pe_z2)/(2*step_size)

                gradE[i] = [gradE_x,gradE_y,gradE_z]

        print 'gradE', gradE
        return gradE



    def getForce(self, positions):

        atoms_list = [self.element for i in range(0,len(positions))]
        atoms = ase.Atoms(atoms_list, positions)
        atoms.set_calculator(self.calculator)
        force = atoms.get_forces()

        print 'force:', force
        return force


    def	results(self):
	""" This method computes the results as a dictionary """

	result = {}

	# here you can either use a perturbed fcc lattice or completely random positions        
        #positions=self.makeRandomPositions()
        positions = self.makePerturbedLattice()

        gradE = self.gradE(positions)
        force = self.getForce(positions)

        result['gradE'] = gradE
        result['force'] = force

        # what should the error tolerance be on this?
        error = abs((gradE+force)/force)

	max_error = error.max()
	
	# this is to identify where the max error is
	index1 = error.argmax()/scipy.shape(error)[1]  
	index2 = error.argmax()-scipy.shape(error)[1]*(index1)

        if (error > 10**(-8)).any(): # expected error according to numerical recipes
                result['Equal'] = False
        else:
                result['Equal'] = True

        result['errors'] = error
	result['max error'] = max_error
	result['max error location']=scipy.array([index1,index2])

        return result

	
if __name__ == "__main__":
    test = ForceTest(args.potential,args.element,write=args.write)
    #raises BaseTest.main
    print test.main()
