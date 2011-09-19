"""
The Database module.

Handles the abstraction of reading and writing the results of the tests.

I will start by using XML
"""


def get_by_potential(potential, cands = None):
    """ Get all of the results by potential name """

def get_by_element(element, cands=None):
    """ Get all of the results by element """

def get_by_test(test, cands=None):
    """ Get all of the results by test name """


def request(potential,element,test):
    """ Get the results from a potential, element, test pair """


###############
# Legacy ######
###############

def getContent(node):
    rc = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE:
            rc.append(child.data)
    return ''.join(rc)

def XMLReader(xmltext):
    """This method unpacks results to a dictionary"""
    from xml.parsers.expat import ExpatError
    try:
        doc = mini.parseString(xmltext)
    except ExpatError:
        assert False
    configs = {}
    results = {}
    testnode = doc.documentElement
    try:
        confignode = testnode.getElementsByTagName('config')[0]
        for child in confignode.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                configs[child.tagName] = getContent(child)

        resultnode = testnode.getElementsByTagName('results')[0]
        for child in resultnode.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                results[child.tagName] = getContent(child)
    except IndexError:
        assert False
    return configs, results

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
            outputfile.write(doc.toxml())
            outputfile.close()
            
        #return a pretty xml string.
        return doc.toxml()
        
