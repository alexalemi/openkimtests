#! /usr/bin/env python

from _BaseTest import *


#request method available, as
# 	request(potential,element,test,resultentry)
#logger available

class MinimalTest(BaseTest):
	""" This example serves as a minimal example of a test
			Notes:
				* Place slab in self.slab
				* calculator available at self.calculator """

	def results(self):
		""" This method computes the results as a dictionary """

		results = {'answer':42}

		return results

	
if __name__ == "__main__":
    test = MinimalTest(args.potential,args.element,verify=args.verify,write=args.write)
    #raises BaseTest.main
    print test.main()