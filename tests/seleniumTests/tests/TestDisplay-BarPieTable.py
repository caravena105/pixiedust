import sys, os
import jupyterselenium
import unittest 
import selenium

__NOTEBOOK_NAME__ = "TestDisplay-Filter.ipynb"
__NOTEBOOK_FOLDER_PATH__ = "/Users/jacob.r.stafford@ibm.com/Desktop/pixiedust/tests"

class BarPieTableTest(jupyterselenium.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BarPieTableTest, cls).setUpClass(__NOTEBOOK_NAME__, __NOTEBOOK_FOLDER_PATH__)

    def testTesting(self):
        assert("hi" == "hi")

    def testDriverExists(self):
        assert(self.driver != None)
        cell1Xpath = self.notebook.getNthCellOutputXpath(3)
        print(cell1Xpath + "/btn/")

    def testClickingOptions(self):
        None

if __name__ == '__main__':
    unittest.main()


#Load specfic notebook based on file name into