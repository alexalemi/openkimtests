"""
The potential module.

Handles the loading of potentials from ASE, KIM, and LAMMPS

"""

import lammps
import kim

import os.path
import openkimtests
openkimtest_dir = os.path.dirname(openkimtests.__file__)
tmp_dir = os.path.join(openkimtest_dir,'tmp')

from logger import logger
logger = logger.getChild('potential')

class PackageDoesNotExist(Exception):
    """ Raised if a package cannot be loaded """

class UnknownPotential(Exception):
    """ Raised if a package cannot be loaded """

class UnsupportedAtom(Exception):
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


##################################################
# ASE STUFF ######################################
##################################################


def EMT_loader(name,element,slab=None,*args,**kwargs):
    """ Load an ASE EMT potential """
    child_logger = logger.getChild('EMT_loader')
    supported_elements = ['Ni','C','Pt','Ag','H',
                            'Al','O','N','Au','Pd','Cu']
    try:
        from ase.calculators.emt import EMT
        import ase
        ase.EMT.disabled = False
    except ImportError:
        child_logger.warning("ASE doesn't seem to exist")
        raise PackageDoesNotExist('ASE:EMT')
    try:
        calc = EMT(*args,**kwargs)
    except:
        child_logger.warning("Calculator creation threw exception")
        raise PotentialLoadFailed('ASE:EMT',*args,**kwargs)
    return calc

import scipy as sp

def ASAP_loader(name,element,slab=None,*args,**kwargs):
    """ Load ASAP potential """
    supported_elements = ['Ni','Cu','Pd','Ag','Pt','Au']
    child_logger = logger.getChild('ASAP_loader')
    try:
        import asap3
    except ImportError:
        child_logger.warning('ASAP package could not be loaded')
        raise PackageDoesNotExist('ASAP')
    try:
        if slab:
            size = min(sp.sum(slab.cell,0))
            boxes = sp.floor(10/size + 1)
            if boxes > 1:
                child_logger.warning('Cell Size too small for ASAP')

        calc = asap3.EMT(*args,**kwargs)
    except:
        child_logger.warning('An error occurred in the calculator creation')
        raise PotentialLoadFailed('ASAP',*args,**kwargs)
    return calc



supported_atoms = {'ASAP':set(['Ni','Cu','Pd','Ag','Pt','Au']),
                   'EMT': set(['Ni','C','Pt','Ag','H',
                               'Al','O','N','Au','Pd','Cu']) }

potentials = {'EMT':EMT_loader ,
              'ASAP': ASAP_loader }


##################################################
## KIM STUFF #####################################
##################################################


def KIM_loader(name,element,slab=None,*args,**kwargs):
    """ Load a KIM Potential """
    child_logger = logger.getChild('KIM_loader')

    #Make sure we have slab information
    if slab is None:
        child_logger.warning('KIM Potential needs slab information')
        raise PotentialLoadFailed('KIM',*args,**kwargs)

    subspec = slab.get_chemical_symbols()
    spec_mass = slab.get_masses()

    pair_style = "pair_KIM {name} {spec}".format(name=name,spec=subspec[0])
    mass_string = ["* {}".format(spec_mass[0])]

    parameters = { "pair_style" : pair_style, 
                        'pair_coeff' : ['* *'],
                         'mass': mass_string }

    default_args = {'tmp_dir':tmp_dir, 'parameters':parameters, 'specorder': subspec}
    default_args.update(kwargs)
    try:
        from kim import KIM
    except ImportError:
        child_logger.warning('Could not load kim module')
        raise PackageDoesNotExist('KIM')
    try:
        calc = KIM(*args,**default_args)
    except:
        child_logger.warning('Calculation creation threw exception')
        raise PotentialLoadFailed('KIM',*args,**kwargs)
    return calc



logger.info("Building available kim models")
kim_models = []

import os, glob

kim_dir = os.environ['KIM_DIR']

if 'KIM_MODELS_DIR' in os.environ:
    kim_models_dir = os.environ['KIM_MODELS_DIR']
else:
    kim_models_dir = os.path.join(kim_dir,'MODELs')

folders = glob.glob(os.path.join(kim_models_dir,'*'))

for folder in folders:
    basename = os.path.basename(folder)
    if basename.startswith('model'):
        kim_models.append(basename)


def kim_file_atoms(model):
    """ Given a KIM Model name, read the .kim file
    to get the supported atoms """
    kim_file = open(os.path.join(kim_models_dir,model,model+'.kim'))
    atoms = set()
    in_section = False
    for line in kim_file:
        if line.startswith('SUPPORTED_ATOM'):
            in_section = True
            continue
        if in_section:
            if line[:5].isupper():
                in_section = False
                break
            line = line.rstrip()
            if line:
                if not line.startswith('#'):
                    splits = line.split()
                    atoms.add(splits[0])
    return atoms


kim_supported_atoms={model:kim_file_atoms(model) for model in kim_models}

#add the kim models to the supported models

supported_atoms.update(kim_supported_atoms)
potentials.update({model:KIM_loader for model in kim_models})


#########################################################
# MISC STUFF ############################################
#########################################################

def GPAW_loader(name,element,slab=None,*args,**kwargs):
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


def LAMMPS_loader(name,element,slab=None,*args,**kwargs):
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


#########################################################
# LOADER ################################################
#########################################################


def load(name,element=None,slab=None,*args,**kwargs):
    """ Allow dictionary like access """
    logger.debug('Recieved a potential.load call')

    if name in potentials:
        logger.debug('potentialname: %s found',name)
        if element in supported_atoms[name]:
            logger.debug('element %r found',element)
            return potentials[name](name,element,slab,*args,**kwargs)
        else:
            logger.warning('Element %r not supported by potential %r', element, name)
            raise UnsupportedAtom(name,element)
    else:
        logger.warning('Potential %r not found',name)
        raise UnknownPotential(name)



    
