#! /usr/bin/env python


import glob, time, os, sys


#get the paths
import os.path
import openkimtests
openkimtest_dir = os.path.dirname(openkimtests.__file__)

test_dir = os.path.join(openkimtest_dir,'kim_tests')

#import useful stuff
import openkimtests
from logger import logger
import db
from filetools import file_list
import potential as potential_module

import logging

logger = logger.getChild('pipeline')

def run_test(test,potential,element,verbose=True):
    """ Run a specific test """
    child_logger = logger.getChild('runtest')
    try:
        if verbose:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            child_logger.addHandler(ch)

        child_logger.info('\nAbout to run a test, test=%r,potential=%r,element=%r',
                            test,potential,element)
        start_time = time.time()
        
        child_logger.info('Attempting to load the test')
        try:
            testModule = __import__('openkimtests.kim_tests.'+test,None,None,fromlist=[test])
        except ImportError:
            child_logger.error('openkimtests.kim_tests.%r failed to import',test)
            raise
        
        testClass = testModule.__getattribute__(test)
        
        child_logger.info('Creating a test instance')
        testObject = testClass(potentialname=potential,element=element)

        #compute results, and create results file   
        results = testObject.main()
        
        child_logger.info('Computed results, obtained: %r\n', results)
    finally:
        #ensure we clear memory up a bit and detach handlers
        del testObject
        del testClass
        del testModule
        if verbose:
            child_logger.removeHandler(ch)



def test_timestamp(test):
    """ Get the modified time of the test """
    return os.path.getmtime(os.path.join(test_dir,test+'.py'))


def new_results_needed(potential,element,test):
    """ Do we need new test results """
    test_time = test_timestamp(test)
    results_time = db.results_timestamp(potential,element,test)
    return test_time > results_time
    
test_list = file_list(test_dir)

import traceback

def run_tests(verbose=True,update=False):
    """ Run all of the tests, where unless update is set,
        only compute the results if the test has been modified since
        the results. """
    child_logger = logger.getChild('run_tests')
    try:
        if verbose:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            child_logger.addHandler(ch)

        
        child_logger.info('\nLaunching all tests')
        start = time.time()
        for test in test_list:
            child_logger.info('\nRunning tests for test=%r',test)
            test_start =time.time()
            for potential,element_set in potential_module.supported_atoms.iteritems():
                child_logger.info('\nRunning potential=%r',potential)
                potential_start = time.time()
                for element in element_set:

                    
                    #figure out if we need to run the test
                    test_needed = True
                    if db.results_exist(potential=potential,
                                            element=element,
                                            test=test):
                        child_logger.info('Test %r,%r,%r exists',test,potential,element)
                        if new_results_needed(potential,element,test):
                            child_logger.info('New test needs computing')
                            test_needed = True
                        else:
                            test_needed = False
                    if update:
                        test_needed=True
                     
                        
                    if test_needed:
                        test_start = time.time()
                        child_logger.info('\nRunning element=%r',element)
                        try:
                            run_test(test=test,
                                    potential=potential,
                                    element=element,
                                    verbose=verbose)
                        except Exception as e:
                            child_logger.error('\nERROR on test=%r, potential=%r, element=%r, info:%r',
                                                test,potential,element,e)
                            child_logger.error('TRACEBACK: %s',traceback.format_exc())
            
                        child_logger.info('Element %r Run took %r seconds',element,time.time()-test_start)
                    else:
                        child_logger.info('Unessesary test %r,%r,%r',test,potential,element)
                child_logger.info('Potential %r run took %r seconds',potential,time.time()-potential_start)
            child_logger.info('Test %r run took %r seconds',test,time.time()-test_start)
        child_logger.info('Full Run took %r seconds',time.time()-start)            

    finally:
        child_logger.removeHandler(ch)
        



def request(potential,element,test,resultentry):
    """ Get the results from a potential, element, test pair
        if it doesn't exist, run it """

    if not db.results_exist(potential,element,test):
        run_test(test,potential,element)
    
    ans = db.request(potential,element,test,resultentry)

    return ans


        
if __name__ == "__main__":
    #run all tests
    run_tests()
