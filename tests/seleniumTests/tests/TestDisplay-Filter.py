import sys, os
import jupyterselenium
import unittest 
import time

import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


__NOTEBOOK_NAME__ = "TestDisplay-Filter.ipynb"
__NOTEBOOK_FOLDER_PATH__ = "/Users/jacob.r.stafford@ibm.com/Desktop/pixiedust/tests"

class OptionsMenuTest(jupyterselenium.TestCase):

    @classmethod
    def setUpClass(cls):
        super(OptionsMenuTest, cls).setUpClass(__NOTEBOOK_NAME__, __NOTEBOOK_FOLDER_PATH__)

    def testChartTitleChange(self):
        assert(self.driver != None)
        cell3 = self.notebook.getCell(3)
        
        optionsBtn = self.notebook.getElementInsideCell(cell3,
             "//*[@pd_app='pixiedust.display.chart.renderers.table.tableOptions.TableOptions']", wait=True)
        optionsBtn.click()

        xpathToOptionsDialog = "//*[contains(@class,'modal-dialog')]"
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpathToOptionsDialog))
        )  

        xpathToTitleInput =  xpathToOptionsDialog + "//*[contains(@name,'title')]"

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpathToTitleInput))
        )  

        titleForm = self.driver.find_element_by_xpath(xpathToTitleInput)
        titleForm.clear()
        titleForm.send_keys("Selenium changed the title!")

        xpathToOkayBtn= xpathToOptionsDialog + "//*[contains(@class,'btn-ok')]"
        okayBtn = self.driver.find_element_by_xpath(xpathToOkayBtn)
        okayBtn.click()

        title = self.notebook.getElementInsideCell(cell3, "//div[@class='pd_save']", wait=True)
        self.assertEqual("Selenium changed the title!", title.text)

    def testRowNumberChange(self):
        None
    
    def testAddingField(self):
        None

    def testRemovingField(self):
        None





if __name__ == '__main__':
    unittest.main()


#Load specfic notebook based on file name into