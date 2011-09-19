"""
The potential module.

Handles the loading of potentials from ASE, KIM, and LAMMPS

"""

import lammps
import kim

import os.path
import openkimtest
openkimtest_dir = os.path.dirname(openkimtest.__file__)
tmp_dir = os.path.join(openkimtest_dir,'tmp')


class PackageDoesNotExist(Exception):
	""" Raised if a package cannot be loaded """

class PotentialLoadFailed(Exception):
	""" Raised if the calculator failed to initialize """
	def __init__(self,name,*args,**kwargs):
		""" Take args and kwargs """
		self.name = name
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		callstring = str(self.name) + '('
		for arg in self.args:
			callstring += str(arg) + ','
		for k,v in self.kwargs.iteritems():
			callstring += str(k) + '=' + str(v) + ','
		callstring = callstring[:-1] + ')'
		return callstring

def EMT_loader(*args,**kwargs):
	""" Load an ASE EMT potential """
	supported_elements = ['Ni','C','Pt','Ag','H',
							'Al','O','N','Au','Pd','Cu']
	try:
		from ase.calculators.emt import EMT
	except ImportError:
		raise PackageDoesNotExist('ASE:EMT')
	try:
		calc = EMT(*args,**kwargs)
	except:
		raise PotentialLoadFailed('ASE:EMT',*args,**kwargs)
	return calc

def ASAP_loader(*args,**kwargs):
	""" Load ASAP potential """
	supported_elements = ['Ni','Cu','Pd','Ag','Pt','Au']
	try:
		from asap3 import EMT
	except ImportError:
		raise PackageDoesNotExist('ASAP')
	try:
		calc = EMT(*args,**kwargs)
	except:
		raise PotentialLoadFailed('ASAP',*args,**kwargs)
	return calc

def GPAW_loader(*args,**kwargs):
	""" Load the GPAW calculator """
	try:
		from gpaw import GPAW
	except ImportError:
		raise PackageDoesNotExist('GPAW')
	try:
		calc = GPAW(*args,**kwargs)
	except:
		raise PotentialLoadFailed('GPAW',*args,**kwargs)
	return calc


def LAMMPS_loader(*args,**kwargs):
	""" Load LAMMPS calculator """
	default_args = {'tmp_dir':tmp_dir}
	default_args.update(kwargs)
	try:
		from lammps import LAMMPS
	except ImportError:
		raise PackageDoesNotExist('LAMMPS')
	try:
		calc = LAMMPS(*args,**default_args)
	except:
		raise PotentialLoadFailed('LAMMPS',*args,**kwargs)
	return calc

def KIM_loader(*args,**kwargs):
	""" Load a KIM Potential """
	default_args = {'tmp_dir':tmp_dir}
	default_args.update(kwargs)
	try:
		from kim import KIM
	except ImportError:
		raise PackageDoesNotExist('KIM')
	try:
		calc = KIM(*args,**default_args)
	except:
		raise PotentialLoadFailed('KIM',*args,**kwargs)
	return calc

def load(name,*args,**kwargs):
	""" Allow dictionary like access """
	name = name.lower()
	if (name == 'ase') or (name=='emt'):
		return EMT_loader(*args,**kwargs)
	if name == 'asap':
		return ASAP_loader(*args,**kwargs)
	if name == 'gpaw':
		return GPAW_loader(*args,**kwargs)
	if name == 'lammps':
		return LAMMPS_loader(*args,**kwargs)
	if name == 'kim':
		return KIM_loader(*args,**kwargs)


	
