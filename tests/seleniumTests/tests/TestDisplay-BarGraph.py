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

def openOptionsDialog(driver, notebook, cell):
    #pop up that isn't contained in pixiedust
    xpathToOptionsDialog = "//*[contains(@class,'modal-dialog')]"
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, xpathToOptionsDialog))
        )
    except(TimeoutException):
        optionsBtn = notebook.getElementInsideCell(cell,
            "//*[@pd_app='pixiedust.display.chart.options.defaultOptions.DefaultOptions']", wait=True
        )
        optionsBtn.click()
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, xpathToOptionsDialog))
        )

def getElementInOptionsDialog(driver, xpathToElem, wait=True):
    xpathToOptionsDialog = "//*[contains(@class,'modal-dialog')]"
    xpath = xpathToOptionsDialog + xpathToElem
    if(wait):
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    return driver.find_element_by_xpath(xpath)


class BarGraphTest(jupyterselenium.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BarGraphTest, cls).setUpClass(__NOTEBOOK_NAME__, __NOTEBOOK_FOLDER_PATH__)
        cls.sortTestMethodsUsing = None

    def test1OpenBarGraphOptionsMenu(self):
        cell3 = self.notebook.getCell(3)

        changeGraphBtn = self.notebook.getElementInsideCell(cell3, "//*[@title='Chart']", wait=True)
        changeGraphBtn.click()

        barChartSpan = self.notebook.getElementInsideCell(cell3, "//*[contains(@id, 'barChart')]", wait=True)
        barChartSpan.click()
 
        openOptionsDialog(self.driver, self.notebook, cell3)

        keyField = getElementInOptionsDialog(self.driver, "//*[contains(@id,'keys-fields')]")
        abbrItem = getElementInOptionsDialog(self.driver, "//*[@data-field='abbr']")
        ActionChains(self.driver).drag_and_drop(abbrItem, keyField).perform()

    def test2DragValuesToValueLocation(self):
        valuesField = getElementInOptionsDialog( self.driver, "//*[contains(@id,'values-fields')]")
        bronzeItem = getElementInOptionsDialog( self.driver, "//*[@data-field='medals.bronze']")
        silverItem = getElementInOptionsDialog( self.driver, "//*[@data-field='medals.silver']")
        goldItem = getElementInOptionsDialog( self.driver, "//*[@data-field='medals.gold']")
        ActionChains(self.driver).drag_and_drop(bronzeItem, valuesField).perform()
        ActionChains(self.driver).drag_and_drop(silverItem, valuesField).perform()
        ActionChains(self.driver).drag_and_drop(goldItem, valuesField).perform()

    def test3ClickOk(self):
        okayBtn= getElementInOptionsDialog(self.driver, "//*[contains(@class,'btn-ok')]")
        okayBtn.click()

