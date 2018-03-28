import sys, os
import jupyterselenium
import unittest 
import time

import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException



__NOTEBOOK_NAME__ = "TestDisplay-Filter.ipynb"
__NOTEBOOK_FOLDER_PATH__ = "/Users/jacob.r.stafford@ibm.com/Desktop/pixiedust/tests"


#helper function for dragging and dropping
def drag_and_drop(driver, xpathSrc, xpathDest, wait=True, waitTime=3):
    if(wait):
        WebDriverWait(driver, waitTime).until(
            EC.element_to_be_clickable((By.XPATH, xpathSrc))
        )
    src = driver.find_element_by_xpath(xpathSrc)
    dest = driver.find_element_by_xpath(xpathDest)
    ActionChains(driver).drag_and_drop(src, dest).perform()

class BarGraphTest(jupyterselenium.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BarGraphTest, cls).setUpClass(__NOTEBOOK_NAME__, __NOTEBOOK_FOLDER_PATH__)

    def testBarGraphChoice(self):
        cell3 = self.notebook.getCell(3)

        changeGraphBtn = self.notebook.getElementInsideCell(cell3, "//*[@title='Chart']", wait=True)
        changeGraphBtn.click()

        barChartSpan = self.notebook.getElementInsideCell(cell3, "//*[contains(@id, 'barChart')]", wait=True)
        barChartSpan.click()

        #pop up that isn't contained in pixiedust
        xpathToOptionsDialog = "//*[contains(@class,'modal-dialog')]"
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, xpathToOptionsDialog))
            )
        except(TimeoutException):
            optionsBtn = self.notebook.getElementInsideCell(cell3,
                "//*[@pd_app='pixiedust.display.chart.options.defaultOptions.DefaultOptions']", wait=True
            )
            optionsBtn.click()
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, xpathToOptionsDialog))
            )
 
        xpathToKeysField = xpathToOptionsDialog + "//*[contains(@id,'keys-fields')]"
        xpathToAbbrItem = xpathToOptionsDialog + "//*[@data-field='abbr']"
        drag_and_drop(self.driver, xpathToAbbrItem, xpathToKeysField)

        xpathToValuesField = xpathToOptionsDialog + "//*[contains(@id,'values-fields')]"
        xpathToBronzeItem = xpathToOptionsDialog + "//*[@data-field='medals.bronze']"
        xpathToSilverItem = xpathToOptionsDialog + "//*[@data-field='medals.silver']"
        xpathToGoldItem = xpathToOptionsDialog + "//*[@data-field='medals.gold']"
        drag_and_drop(self.driver, xpathToBronzeItem, xpathToValuesField)
        drag_and_drop(self.driver, xpathToSilverItem, xpathToValuesField)
        drag_and_drop(self.driver, xpathToGoldItem, xpathToValuesField)

        xpathToOkayBtn= xpathToOptionsDialog + "//*[contains(@class,'btn-ok')]"
        okayBtn = self.driver.find_element_by_xpath(xpathToOkayBtn)
        okayBtn.click()

