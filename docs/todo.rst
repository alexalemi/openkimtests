=======
ToDo
=======

Thing's I need to do
 * Fix naming convention in BaseTest
 	goto lowercase names for functions
 * Write KIM and LAMMPS calculators
 * Handle errors intelligently
 * Rewrite pipeline
 * abstract database calls
 * implement logging
 * write a generalized potential loader
 * write a command line interface (cmd)



Current Focus
 * need to fill out BaseTest again
 * need to load the potential
 * need to allow requests
 * need to fill out database stuff
 * switch results to be "TEST.ELEMENT.POTENTIAL.XML" to ease lookups
 * write some docs


For Potential Drivers
	Need to supply a list of potentials
	need to for each of the potentials supply a list of supported atoms
	each of these needs to be able to supply a calculator.  


pipeline

	run every test over every potential over every element it supports


	for test in tests:
		for potential in potentials:
			for element in supported_elements:
				compute results
