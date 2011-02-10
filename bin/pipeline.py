#! /usr/bin/env python


import glob, time, os, sys

#directory paths
testdirectory = "../tests/"
resultsdirectory = "../results/"
outputdirectory = "../outputs/"
verifydirectory = "../verify/"

#ase emt support
emtlist = ['Ni','C','Pt','Ag','H','Al','O','N','Au','Pd','Cu']
emtfcclist = ['Ni','Pt','Ag','Al','Au','Pd','Cu']
potentiallist = ['EMT']#,'GPAW']
potentiallist = ['EMT']

def runTest(test,potential,el,verbose=True):
    testname = test[len(testdirectory):-3]
    if verbose:
        print "=================================================="
        print "Running %s with %s for %s" % ( testname, potential, el)
    outputfilename = testname + '.' + potential + '.' + el + '.out'
    outputfilepath = outputdirectory + outputfilename
    resultfilename = testname + '.' + potential + '.' + el + '.xml'
    resultfilepath = resultsdirectory + resultfilename
    if verbose:
        print 
        print "File output... "
    start = time.time()
    if verbose:
        print "EXECUTING: "
        print 'python ' + test + ' ' + potential + ' ' + el + ' -w ' + '| tee ' + outputfilepath
    outflag = os.system('python ' + test + ' ' + potential + ' ' + el + ' -w ' + '| tee ' + outputfilepath)
    if outflag:
        os.system('rm ' + outputfilepath)
        print "Exception Occured"
        return -1
    end = time.time()
    if verbose:
        print 
        print "Test completed successfully in %f seconds" % (end-start)
        print "Results stored in %s" % resultfilename
    return 0 

def runTests(runAll = False):
    print 
    print "Test completed successfully in %f seconds" % (end-start)
    print "Results stored in %s" % resultfilename
    
def runTests(runAll = False, DFT = False):
    pipelinestart = time.time()
    if runAll:
        print "Running a full pipeline, all tests"
    if DFT:
        potentiallist.append('GPAW')
    lstTests = glob.glob(testdirectory + '*.py')
    lstTests.remove(testdirectory + 'BaseTest.py')
    lstTests.remove(testdirectory + 'NullTest.py')
    print lstTests
    print "Running pipeline... "
    print "There are a total of %d Tests" % (len(lstTests))
    for test in lstTests:
        testname = test[len(testdirectory):-3]
        for potential in potentiallist:
            for el in emtlist:
                if runAll:
                    runTest(test,potential,el)
                else:
                    resultfilename = testname + '.' + potential + '.' + el + '.xml'
                    resultfilepath = resultsdirectory + resultfilename
                    try:
                        fob = open(resultfilepath)
                        print "Test configuation for %s already exists..." % resultfilename
                    except IOError:
                        runTest(test,potential,el)  
    pipelinestop = time.time()
    
    print "Pipeline update finished, took %f seconds " % (pipelinestop-pipelinestart)              
            
            
if __name__ == '__main__':
    runAllFlag = False
    DFTFlag = False
    for opt in sys.argv:
        if opt == '--full':
            runAllFlag = True
        if opt == '--dft':
            DFTFlag = True
    runTests(runAll = runAllFlag, DFT = DFTFlag)
            
            
            
# Is there a way to do a   programtoexecute &> output.file 
# but also have it echo to the terminal
