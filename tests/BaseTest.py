"""This is the baseTest from which all tests inherit.  """

import sys
import ase


class BaseTest:
    """This is the Base Test from which all other Tests inherit."""
    
    def __init__(self,potentialname,element,TestDependencies=[],verified=False,*args,**kwargs):
        self.potentialname = potentialname
        self.potential = self.getASEPotentialByName(potentialname)
        self.element = element
        self.verified = verified
        
        self.TestDependencies = TestDependencies

    def getASEPotentialByName(self,name):
        calculatorName = 'ase.calculators.' + name + '()'
        return eval(calculatorName)
        
    def TestResults(self):
        """The Test Results method, runs the test and packages the result as an xml snippet"""
        pass

    def Verify(self):
        """Optional verify method, creates an easy to check visual verification of test results"""
        pass
        
    def main(self):
        if self.verified:
            self.Verify()
        return self.TestResults()
