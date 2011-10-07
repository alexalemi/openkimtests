#! /usr/bin/env python

#import BaseTest and ase
from _BaseTest import *

#Test specific imports
import scipy as sp
import pylab as py
from ase.structure import bulk
import numdifftools as ndt
from ase import units

class BCCElasticConstants(BaseTest):
    """Determine the cubic elastic constants by numerically determining the Hessian"""

    def __init__(self,*args,**kwargs):
	super(BCCElasticConstants,self).__init__(*args,**kwargs)
	self.o_slab = self.create_slab()

    def create_slab(self):
	# Request the BCCLattice constant
	a = request(self.potentialname, self.element, 'BCCLattice', 'BCCLatticeConstant' )

	slab = bulk(self.element,a=a,crystalstructure='bcc',cubic=True)
	if self.potentialname == 'ASAP':
	    slab = slab.repeat((8,8,8))

	return slab

    def voigt_to_matrix(self,voigt_vec):
	"""Convert a voigt notation vector to a matrix """
	matrix = sp.zeros((3,3))
	matrix[0,0] = voigt_vec[0]
	matrix[1,1] = voigt_vec[1]
	matrix[2,2] = voigt_vec[2]
	matrix[ [ [1,2], [2,1] ] ] = voigt_vec[3]
	matrix[ [ [0,2], [2,0] ] ] = voigt_vec[4]
	matrix[ [ [0,1], [1,0] ] ] = voigt_vec[5]

	return matrix

    def strain(self,strain_vec):
	""" Apply a strain according to the strain_vec """
	self.slab = self.o_slab.copy()
	strain_mat = self.voigt_to_matrix(strain_vec)

	old_cell = self.slab.cell
	new_cell = old_cell + sp.dot( strain_mat, old_cell)

	self.slab.set_cell(new_cell,scale_atoms=True)
	
	self.slab.set_calculator(self.calculator)

	energy = self.slab.get_potential_energy()
	volume = self.slab.get_volume()
	
	return energy/volume/units.GPa	
 
    def results(self):
	""" Return the cubic elastic constants """
	func = self.strain
	hess = ndt.Hessian(func)
	elastic_constants = hess(sp.zeros(6))
	error_estimate = hess.error_estimate
	
	C11 = 1./3 * ( elastic_constants[0,0]
		+ elastic_constants[1,1] 
		+ elastic_constants[2,2])
	C11sig = 1./3 *sp.sqrt( error_estimate[0,0]**2 
			+ error_estimate[1,1]**2 
			+ error_estimate[2,2]**2 )

	C12 = 1./6 * ( elastic_constants[1,0]
			+ elastic_constants[2,0]
			+ elastic_constants[2,1]
			+ elastic_constants[0,1]
			+ elastic_constants[0,2]
			+ elastic_constants[1,2] )
	C12sig = 1./6 * sp.sqrt( error_estimate[1,0]**2
			+ error_estimate[2,0]**2
			+ error_estimate[2,1]**2
			+ error_estimate[0,1]**2
			+ error_estimate[0,2]**2
			+ error_estimate[1,2]**2 )

	C44 = 1./3 * ( elastic_constants[3,3]
			+ elastic_constants[4,4]
			+ elastic_constants[5,5] )
	C44sig = 1./3 * sp.sqrt( error_estimate[3,3]**2 
			+ error_estimate[4,4]**2
			+ error_estimate[5,5]**2 )

	B = 1./3 * ( C11 + 2 * C12 )
	Bsig = sp.sqrt( ( 1./3 * C11sig )**2 + ( 2./3 * C12sig )**2 )

    	excess = 1./24 * (elastic_constants[3,0]
			+elastic_constants[3,1]
			+elastic_constants[3,2]
			+elastic_constants[4,0]
			+elastic_constants[4,1]
			+elastic_constants[4,2]
			+elastic_constants[4,3]
			+elastic_constants[5,0]
			+elastic_constants[5,1]
			+elastic_constants[5,2]
			+elastic_constants[5,3]
			+elastic_constants[5,4]
			+elastic_constants[0,3]
			+elastic_constants[1,3]
			+elastic_constants[2,3]
			+elastic_constants[0,4]
			+elastic_constants[1,4]
			+elastic_constants[2,4]
			+elastic_constants[3,4]
			+elastic_constants[0,5]
			+elastic_constants[1,5]
			+elastic_constants[2,5]
			+elastic_constants[3,5]
			+elastic_constants[4,5])
	excess_sig = 1./24 * sp.sqrt( error_estimate[3,0]**2
			+ error_estimate[3,1]**2
			+ error_estimate[3,2]**2
			+ error_estimate[4,0]**2
			+ error_estimate[4,1]**2
			+ error_estimate[4,2]**2
			+ error_estimate[4,3]**2
			+ error_estimate[5,0]**2
			+ error_estimate[5,1]**2
			+ error_estimate[5,2]**2
			+ error_estimate[5,3]**2
			+ error_estimate[5,4]**2
			+ error_estimate[0,3]**2
			+ error_estimate[1,3]**2
			+ error_estimate[2,3]**2
			+ error_estimate[0,4]**2
			+ error_estimate[1,4]**2
			+ error_estimate[2,4]**2
			+ error_estimate[3,4]**2
			+ error_estimate[0,5]**2
			+ error_estimate[1,5]**2
			+ error_estimate[2,5]**2
			+ error_estimate[3,5]**2
			+ error_estimate[4,5]**2 )

	results_dict = { 'C11': C11, 
			 'C11_sig' : C11sig,
			 'C12' : C12,
			 'C12_sig' : C12sig,
			 'C44': C44,
			 'C44_sig' : C44sig,
			 'B' : B,
			 'B_sig' : Bsig,
			 'excess': excess,
			 'excess_sig' : excess_sig,
			 'units' : 'GPa' }

	return results_dict


#required for command line execution
if __name__ == '__main__':
    test = BCCElasticConstants(args.potential,args.element,write=args.write)
    #raises BaseTest.main
    print test.main()
    
        
