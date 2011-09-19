""" Unit Tests for the potential module """

from openkimtest.bin import potential
import unittest

import ase
from ase.structure import bulk

import logging

import os.path
import openkimtest
openkimtest_dir = os.path.dirname(openkimtest.__file__)
log_file = os.path.join(openkimtest_dir,'logs','tests.log')


logging.basicConfig(filename=log_file,level=logging.DEBUG)

def test_potential_loaders():
	""" Test that all of the potentials load """
	potentials = ['ASE','ASAP','EMT','GPAW','LAMMPS','KIM']

	for pot in potentials:
		assert potential.load(pot)


def test_lammps():
	""" Do a LAMMPS default run """	
	logging.info("\nInside test_lammps TEST")
	logging.info("Creating a slab of Cu")
	slab = bulk('Cu','fcc',cubic=True).repeat((5,5,5))

	logging.info("loading the LAMMPS calculator")
	slab.set_calculator(potential.load('LAMMPS'))

	logging.info("Getting the potential energy")
	energy = slab.get_potential_energy()
	logging.info("Obtained: {}".format(energy))
	logging.info("Leaving test_lammps TEST\n")

def test_asap():
	""" Do an ASAP default run """	
	logging.info("\nInside test_asap TEST")
	logging.info("Creating a slab of Cu")
	slab = bulk('Cu','fcc',cubic=True).repeat((5,5,5))

	logging.info("loading the ASAP calculator")
	slab.set_calculator(potential.load('ASAP'))

	logging.info("Getting the potential energy")
	energy = slab.get_potential_energy()
	logging.info("Obtained: {}".format(energy))
	logging.info("Leaving test_asap TEST\n")


def Qtest_gpaw():
	""" Do a GPAW default run """	
	logging.info("\nInside test_gpaw TEST")
	logging.info("Creating a slab of Cu")
	slab = bulk('Cu','fcc',cubic=True)

	logging.info("loading the GPAW calculator")
	slab.set_calculator(potential.load('GPAW'))

	logging.info("Getting the potential energy")
	energy = slab.get_potential_energy()
	logging.info("Obtained: {}".format(energy))
	logging.info("Leaving test_GPAW TEST\n")