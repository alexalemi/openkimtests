

from _BaseTest import *

class MinimalTest(BaseTest):
	""" This example serves as a minimal example of a test """

	def results(self):
		""" This method computes the results as a dictionary """

		results = {'answer':42}

		return results

	def verify(self):
		""" This optional method can be used to do some more diagnostic stuff """

	
if __name__ == "__main__":
    test = MinimalTest(args.potential,args.element,verify=args.verify,write=args.write)
    #raises BaseTest.main
    print test.main()