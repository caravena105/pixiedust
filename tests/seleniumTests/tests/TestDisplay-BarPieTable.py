import sys, os
import jupyterselenium
import unittest 
import selenium

__NOTEBOOK_NAME__ = "TestDisplay-BarPieTable.ipynb"

class BarPieTableTest(jupyterselenium.Test):

    @classmethod
    def setUpClass(cls):
        super(BarPieTableTest, cls).setUpClass(__NOTEBOOK_NAME__)
        
    def testTesting(self):
        assert("hi" == "hi")

    def testDriverExists(self):
        assert(self.driver != None)

if __name__ == '__main__':
    unittest.main()


#Load specfic notebook based on file name into