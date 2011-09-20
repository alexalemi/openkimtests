#! /usr/bin/env python

"""This is the baseTest from which all tests inherit. 

The BaseTest handles initialization of the form
    BaseTest( potentialname, element symbol, TestDependencies List, others)
 """

#standard imports
import argparse

from openkimtests.bin.logger import logger

import openkimtests.bin.pipeline as pipeline
import openkimtests.bin.db as db

import ase

logger = logger.getChild('Test')

from openkimtests.bin import potential


#helpful rename
request = pipeline.request

class LackingResults(Exception):
    """ The LackingResults exception, raised if the test doesn't have a results method """

class LackingVerify(Exception):
    """ The LackingVerify method, to be raised if the test doesn't override the verify method """

class BaseTest:
    """This is the Base Test from which all other Tests inherit."""
    
    def __init__(self,potentialname,element,verified=False,verify=False,write=False,*args,**kwargs):
        #store how it was called
        self.potentialname = potentialname.encode('ascii')
        self.element = element.encode('ascii')
        self.verify = verify
        self.write = write
        self.args = args
        self.kwargs = kwargs
        
        #place where atomic configurations are stored
        self.slab = None

        self.dependencies = []

        self.result_names = []

        self.logger = logger.getChild(self.__class__.__name__)

    @property
    def calculator(self):
        """ Generate a calculator for the potential, given a slab """
        self.logger.debug('Recieved a calculator access call')
        return potential.load(self.potentialname,self.element,
                            self.slab)

    def write_results(self,results_dict):
        """ Write the results_dict to the database """

    def request(self,request):
        """ Request some previous results """

        
    def results(self):
        """ Must be overridden by the other tests, calculates the results """
        raise LackingResults

    def verify(self):
        """Optional verify method, creates an easy to check visual verification of test results"""
        raise LackingVerify
        
    def main(self):
        """Main is called when the Test is run from the command line. currently runs tests
        and passes the dictionary of results to the XMLWriter Method"""
        self.logger.debug('Recieved a main method call')
        if self.verify:
            self.verify()

        results = self.results()
        db.writer(potential=self.potentialname,
                    element=self.element,
                    test=self.__class__.__name__,
                    results=results,
                    write=True)

        return results        
        
#Parser specification

parser = argparse.ArgumentParser()
parser.add_argument('potential',nargs='?', help='The first argument is the potential')
parser.add_argument('element',nargs='?', help='The second argument is the element')
parser.add_argument('optionalargs',nargs='*', help='Remaining nontagged arguments')
parser.add_argument('-v','--verify', action='store_true', help='runs the verify method')
parser.add_argument('-w','--write', action='store_true', help='writes the xml file to the results directory')

args = parser.parse_args()


logger.debug('Test called with arguments %r',args)

#make this stuff into in logging statement.
