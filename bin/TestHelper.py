import sys
import ase

def getASEPotentialByName(name):
    calculatorName = 'ase.calculators.' + name + '()'
    return eval(calculatorName)
