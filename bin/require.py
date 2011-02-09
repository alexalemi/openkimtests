#! /usr/bin/env python


import glob, time, os, sys
import argparse

#directory paths
testdirectory = "../tests/"
resultsdirectory = "../results/"
outputdirectory = "../outputs/"

parser = argparse.ArgumentParser()
parser.add_argument('potential',nargs='?', help='The first argument is the potential')
parser.add_argument('element',nargs='?', help='The second argument is the element')
parser.add_argument('test',nargs='?', help='Require the result of this test')

args = parser.parse_args()

potential = args.potential
element = args.element
testname = args.test

resultfilename = testname + '.' + potential + '.' + element + '.xml'
resultfilepath = resultsdirectory + resultfilename
err = 0
try:
    fob = open(resultfilepath)
    #print "Test configuation for %s already exists..." % resultfilename
except IOError:
    import pipeline
    err = pipeline.runTest(testdirectory+testname+'.py',potential,element,verbose=False)  

if err == 0:
    file = open(resultfilepath, 'r')
    print "".join(file.readlines())
    file.close()
import sys
sys.exit(err)

