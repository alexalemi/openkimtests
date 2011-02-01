"""This is the baseTest from which all tests inherit. 

For the XML
Basic structure of output
<Test id='testname'>
    <config>
        <potential> potentialname </potential>
        <element> elementsymbol </element>
        <dependencies> dependency list (optional) </dependencies>
    </config>
    <results>
        <propertyname> value </propertyname>
        <propertyname2> value </propertyname>
    </results>
</Test>
 """

import sys
import ase

import xml.dom.minidom as mini


class BaseTest:
    """This is the Base Test from which all other Tests inherit."""
    
    def __init__(self,potentialname,element,TestDependencies=[],verified=False,*args,**kwargs):
        self.potentialname = potentialname
        self.potential = self.getASEPotentialByName(potentialname)
        self.element = element
        self.verified = verified
        
        self.TestDependencies = TestDependencies
        
    def XMLWriter(self,resultsdict):
    
        #create the XML document
        doc = mini.Document()
        
        testnode = doc.createElement('test')
        testnode.setAttribute('id',str(self.__class__.__name__))
        doc.appendChild(testnode)
        
        #Set the configuration part
        confignode = doc.createElement('config')
        testnode.appendChild(confignode)
        
        potentialnode = doc.createElement('potential')
        elementnode = doc.createElement('element')
        confignode.appendChild(potentialnode)
        confignode.appendChild(elementnode)
        
        potentialnode.appendChild(doc.createTextNode(str(self.potentialname)))
        elementnode.appendChild(doc.createTextNode(str(self.element)))
        
        if self.TestDependencies:
            testdependenciesnode = doc.createElement('testdependencies')
            confignode.appendChild(testdependenciesnode)
            confignode.appendChild(doc.createTextNode(str(self.TestDependencies)))
        
        resultsnode = doc.createElement('results')
        testnode.appendChild(resultsnode)
        
        for key,value in resultsdict.iteritems():
            resultnode = doc.createElement(key)
            resultnode.appendChild(doc.createTextNode(str(value)))
            resultsnode.appendChild(resultnode)
        
        return doc.toprettyxml()
        

    def getASEPotentialByName(self,name):
        calculatorName = 'ase.calculators.' + name + '()'
        return eval(calculatorName)
        
    def TestResults(self):
        """The Test Results method, runs the test and packages the result as an xml snippet"""
        return {}

    def Verify(self):
        """Optional verify method, creates an easy to check visual verification of test results"""
        pass
        
    def main(self):
        if self.verified:
            self.Verify()
        return self.XMLWriter(self.TestResults())
