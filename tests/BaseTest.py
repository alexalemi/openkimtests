#! /usr/bin/env python

"""This is the baseTest from which all tests inherit. 

The BaseTest handles initialization of the form
    BaseTest( potentialname, element symbol, TestDependencies List, others)
 """

#standard imports
import sys
import ase
import argparse

#import xml library
import xml.dom.minidom as mini


class BaseTest:
    """This is the Base Test from which all other Tests inherit."""
    
    def __init__(self,potentialname,element,TestDependencies=[],verified=False,verify=False,write=False,*args,**kwargs):
        self.potentialname = potentialname
        self.potential = self.getASEPotentialByName(potentialname)
        self.element = element
        self.verify = verify
        self.write = write
        
        self.TestDependencies = TestDependencies
        
    def XMLWriter(self,resultsdict):
        """This method packages the results dictionary into our standard XML 
        Format.  The layout is roughly as follows
        
        <test id='TestName'>
            <config>
                <potential> PotentialName </potential>
                <element> Element Symbol </element>
            </config>
            <results>
                <FirstResultKey> FirstResultValue </FirstResultKey>
                <SecondResultKey> SecondResultValue </SecondResultKey>
                ...
            </results>
        </test>
        """
    
        #create the XML document
        doc = mini.Document()
        
        #Create and append the main test node
        testnode = doc.createElement('test')
        testnode.setAttribute('id',str(self.__class__.__name__))
        doc.appendChild(testnode)
        
        #Set the configuration part
        confignode = doc.createElement('config')
        testnode.appendChild(confignode)
        
        #set and append the potential name and element nodes
        potentialnode = doc.createElement('potential')
        elementnode = doc.createElement('element')
        confignode.appendChild(potentialnode)
        confignode.appendChild(elementnode)
        
        potentialnode.appendChild(doc.createTextNode(str(self.potentialname)))
        elementnode.appendChild(doc.createTextNode(str(self.element)))
        
        #if there are test dependencies, add them
        if self.TestDependencies:
            testdependenciesnode = doc.createElement('testdependencies')
            confignode.appendChild(testdependenciesnode)
            confignode.appendChild(doc.createTextNode(str(self.TestDependencies)))
        
        #creates and appends the result node
        resultsnode = doc.createElement('results')
        testnode.appendChild(resultsnode)
        
        #for every key,value pair in the results dictionary, create and
        #append a new node.
        for key,value in resultsdict.iteritems():
            resultnode = doc.createElement(key)
            resultnode.appendChild(doc.createTextNode(str(value)))
            resultsnode.appendChild(resultnode)
        
        
        if self.write:
            resultfile = '../results/' + self.__class__.__name__ + '.' + self.potentialname + '.' + self.element + '.xml'
            outputfile = open(resultfile,'w')
            outputfile.write(doc.toprettyxml())
            outputfile.close()
            
        #return a pretty xml string.
        return doc.toprettyxml()
        

    def getASEPotentialByName(self,name):
        """A little helper method to call ASE potentials by name. 
        
        In the future, to be extended to include KIM potentials"""
        calculatorName = 'ase.calculators.' + name + '()'
        if name == "GPAW":
            from gpaw.aseinterface import GPAW
            return GPAW(h=0.2, kpts = (4,4,4), nbands = 15)
        if name == "ASAP":
            from asap3 import EMT
            return EMT()
        return eval(calculatorName)
        
    def TestResults(self):
        """The Test Results method, runs the test and packages the result in a dictionary"""
        raise LackingTestResults
        return {}

    def Verify(self):
        """Optional verify method, creates an easy to check visual verification of test results"""
        raise LackingVerify
        pass
        
    def main(self):
        """Main is called when the Test is run from the command line. currently runs tests
        and passes the dictionary of results to the XMLWriter Method"""
        if self.verify:
            self.Verify()
        return self.XMLWriter(self.TestResults())
        
        
#Parser specification

parser = argparse.ArgumentParser()
parser.add_argument('potential',nargs='?', help='The first argument is the potential')
parser.add_argument('element',nargs='?', help='The second argument is the element')
parser.add_argument('TestDependencies',nargs='*', help='Remaining nontagged arguments are test dependencies')
parser.add_argument('-v','--verify', action='store_true', help='runs the verify method')
parser.add_argument('-w','--write', action='store_true', help='writes the xml file to the results directory')

args = parser.parse_args()

