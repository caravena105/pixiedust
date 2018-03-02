from ..JupyterSelenium import JupyterSelenium
import unittest 
import selenium

class BarPieTableTest(JupyterSelenium.Test):

    def testSomething(self):
      print(self.jsi.driver)
      self.jsi.driver.get_element_by_xpath("//*[@id=\"menus\"]/div/div/ul/li[1]")

      self.jsi.driver.get_element_by_xpath(self.notebook.cell[0].xpath + "/ul")

      assert("hi" == "hi")
      

if __name__ == '__main__':
    unittest.main()