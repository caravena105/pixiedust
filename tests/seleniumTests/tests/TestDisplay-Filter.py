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
        cell3Xpath = self.notebook.getNthCellOutputXpath(3)
        pixiedustXpath = cell3Xpath + "//div[contains(@class,'pixiedust-output-wrapper')]"

        xpathToOptionsBtn = pixiedustXpath + "//*[@pd_app='pixiedust.display.chart.renderers.table.tableOptions.TableOptions']"
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpathToOptionsBtn))
        )  

        optionsBtn = self.driver.find_element_by_xpath(xpathToOptionsBtn)
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

        xpathToTitle = pixiedustXpath + "//div[@class='pd_save']"
        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element((By.XPATH, xpathToTitle), "Selenium changed the title!")
        ) 
        title = self.driver.find_element_by_xpath(xpathToTitle)

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