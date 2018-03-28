from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Notebook():

    def __init__(self, driver):
        self.cells = []
        self.driver = driver
        self.parseHtmlIntoCells()

    class Cell():
        def __init__(self, xpath, cellNum):
            self.xpath = xpath
            self.cellNum = cellNum

    def getCell(self, cellNum):
        return self.cells[cellNum - 1]
    
    def getNthCellOutputXpath(self, cellNum):
        return self.cells[cellNum - 1].xpath

    def parseHtmlIntoCells(self):
        for cellNum in range(1, self.getNumberOfCells()):
            xpath = "//*[@id=\"notebook-container\"]/div[{0}]/div[2]".format(cellNum)
            self.driver.find_element_by_xpath(xpath)
            self.cells.append(Notebook.Cell(xpath, cellNum))
 
    def getNumberOfCells(self):
        cells = self.driver.find_elements_by_xpath("//*[@id=\"notebook-container\"]/div")
        return len(cells)

    def getElementInsideCell(self, cell, xpath, wait=False, waitTime=3):
        elemXpath = cell.xpath + xpath
        if(wait):
            WebDriverWait(self.driver, waitTime).until(
                EC.element_to_be_clickable((By.XPATH, elemXpath))
            )
        return self.driver.find_element_by_xpath(elemXpath)