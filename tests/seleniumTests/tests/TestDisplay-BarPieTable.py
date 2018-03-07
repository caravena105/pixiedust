import sys, os
import jupyterselenium
import unittest 
import selenium


class BarPieTableTest(jupyterselenium.Test):
    
    def testSomething(self):
      assert("hi" == "hi")

    def testSomethingElse(self):
        assert(self.jsi.driver != None)
      

if __name__ == '__main__':
    unittest.main()
