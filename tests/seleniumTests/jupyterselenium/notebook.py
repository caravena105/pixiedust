from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class Notebook():

    def __init__(self, driver):
        self.cells = []
        self.parseHtmlIntoCells(driver)

    class Cell():
        def __init__(self, xpath, cellNum):
            self.xpath = xpath
            self.cellNum = cellNum

    def getNthCellOutputXpath(self, cellNum):
        return self.cells[cellNum].xpath

    def parseHtmlIntoCells(self, driver):
        for cellNum in range(1, self.getNumberOfCells(driver)):
            xpath = "//*[@id=\"notebook-container\"]/div[{0}]*/div[2]".format(cellNum)
            driver.find_element_by_xpath(xpath)
            self.cells.append(Notebook.Cell(xpath, cellNum))
 
    def getNumberOfCells(self, driver):
        cells = driver.find_elements_by_xpath("//*[@id=\"notebook-container\"]/div")
        return len(cells)
