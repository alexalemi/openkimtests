#! /usr/bin/env python

#import BaseTest and ase
from BaseTest import *

#import bin scripts, and sys for argv
import sys

#Test specific imports go here

class NullTest(BaseTest):
    """NullTest does nothing, but serves as an example test."""
    
    def __init__(self,potentialname,energy,TestDependencies=[],*args,**kwargs):
        BaseTest.__init__(self,potentialname,energy,TestDependencies,*args,**kwargs)
        #self.potential = self.getASEPotentialByName(potentialname)


    def TestResults(self):
        """Required module, the TestResults Module returns a dictionary of result. 
        
        of the form { 'NameOfValue' : value, 'NameOfSecondValue' : secondvalue }
        """

        return {}


    def Verify(self):
        """ Optional verify script to be used to generate a visual output for
        
        quick check that everything is going alright"""
        pass
            
        
        
if __name__ == '__main__':
    test = NullTest(sys.argv[1],sys.argv[2],sys.argv[3:])
    print test.main()
    
        
