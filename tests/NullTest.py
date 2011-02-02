#! /usr/bin/env python

#import BaseTest and ase
from BaseTest import *

#import bin scripts, and sys for argv
import sys

#Test specific imports go here

class NullTest(BaseTest):
    """NullTest does nothing, but serves as an example test.
    
        It inherits its functionality from BaseTest, and serves as a template for future
    tests.  

    Simply copy NullTest.py, and rename the file, and class name, and rewrite TestResults
    """
    
    def __init__(self,potentialname,energy,TestDependencies=[],*args,**kwargs):
        #Passes the initialization arguments to the BaseTest initialization
        BaseTest.__init__(self,potentialname,energy,TestDependencies,*args,**kwargs)


    def TestResults(self):
        """Required module, the TestResults Module returns a dictionary of result. 
        
        of the form { 'NameOfValue' : value, 'NameOfSecondValue' : secondvalue }
        
        This is where your test code goes.  Feel free to write other methods if necessary.
        """

        return {}


    def Verify(self):
        """ Optional verify script to be used to generate a visual output for
        
        quick check that everything is going alright"""
        pass
            
        
#The following ensures that the test can be called from the command line
if __name__ == '__main__':
    test = NullTest(sys.argv[1],sys.argv[2],sys.argv[3:])
    #Uses BaseTest.main to ensure proper execution.
    print test.main()
    
        
