"""
The Database module.

Handles the abstraction of reading and writing the results of the tests.

I will start by using XML
"""

import os.path
import openkimtests
openkimtest_dir = os.path.dirname(openkimtests.__file__)

results_dir = os.path.join(openkimtest_dir,'results')

from logger import logger

logger = logger.getChild('db')


logger.debug('Initializing Database')


import xml.dom.minidom as mini
import simplejson
import xml.etree.ElementTree as etree
import scipy as sp

def XMLReader(filename=None,test=None,potential=None,element=None,full=False):
    """This method unpacks results to a dictionary,
        using json for the serialization"""
    child_logger = logger.getChild('XMLReader')
    child_logger.debug('XMLReader called...')

    #if given a filename, load the file
    if filename:
        tree = etree.parse(os.path.join(results_dir,filename))
    else:
        #otherwise, try to find the file
        filename = test + '.' + potential + '.' + element + '.xml'
        tree = etree.parse(os.path.join(results_dir,filename))

    root = tree.getroot()

    #get test name
    test = root.attrib['id']

    #get contrib
    config_node = root.find('config')
    config = {}
    for node in config_node.getchildren():
        config[node.tag] = node.text
    
    #get results
    results_node = root.find('results')
    results = {}

    #read each of the results nodes
    for node in results_node:

        value = simplejson.loads(node.text)
        #if a scipy array, cast it as such
        if node.attrib == 'ndarray':
            value = sp.array(value)
        results[node.tag] = value

    if full:
        # return full results
        return test, config, results

    return results



def XMLWriter(potential,element,test,results,write=False):
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

    child_logger = logger.getChild('XMLWriter')
    child_logger.debug('XMLWriter called.')

    #create the XML document
    doc = mini.Document()
    
    #Create and append the main test node
    testnode = doc.createElement('test')
    testnode.setAttribute('id',test)
    doc.appendChild(testnode)
    
    #Set the configuration part
    confignode = doc.createElement('config')
    testnode.appendChild(confignode)
    
    #set and append the potential name and element nodes
    potentialnode = doc.createElement('potential')
    elementnode = doc.createElement('element')
    confignode.appendChild(potentialnode)
    confignode.appendChild(elementnode)
    
    potentialnode.appendChild(doc.createTextNode(potential))
    elementnode.appendChild(doc.createTextNode(element))
    
    
    #creates and appends the result node
    resultsnode = doc.createElement('results')
    testnode.appendChild(resultsnode)
    
    #for every key,value pair in the results dictionary, create and
    #append a new node.
    for key,value in results.iteritems():
        resultnode = doc.createElement(key)

        typename = type(value).__name__
        resultnode.setAttribute('type',typename)

        #try to simplejson it
        try:
            jsoned = simplejson.dumps(value)
        except TypeError:
            #if we have a scipy array, cast as list
            if typename == 'ndarray':
                jsoned = simplejson.dumps(value.tolist())
            else:
                raise

        resultnode.appendChild(doc.createTextNode(jsoned))
        resultsnode.appendChild(resultnode)
    
    
    if write:
        resultfile = '../results/' + test + '.' + potential + '.' + element + '.xml'
        outputfile = open(resultfile,'w')
        outputfile.write(doc.toprettyxml())
        outputfile.close()
        
    #return a pretty xml string.
    return doc.toprettyxml()

reader = XMLReader
writer = XMLWriter

def get_by_potential(potential, cands = None):
    """ Get all of the results by potential name """

def get_by_element(element, cands=None):
    """ Get all of the results by element """

def get_by_test(test, cands=None):
    """ Get all of the results by test name """



def results_exist(potential,element,test):
    """ See if results exist """
    filename = test + '.' + potential + '.' + element + '.xml'
    return os.path.isfile(os.path.join(results_dir,filename))

import time

def results_timestamp(potential,element,test):
    """ Get the creation time of a results file """
    filename = test + '.' + potential + '.' + element + '.xml'
    return os.path.getmtime(os.path.join(results_dir,filename))

def request(potential,element,test,resultentry):
    """ Get the results from a potential, element, test pair """
    try:
        results = reader(potential=potential,
                        element=element,
                        test=test)
    except IOError:
        #result doesn't appear to exist
        filename = test + '.' + potential + '.' + element + '.xml'
        logger.warning("Request %r doesn't exist",
                                filename)
    return results[resultentry]

