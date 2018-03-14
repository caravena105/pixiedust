import unittest 
from jupyterselenium.instance import Instance
from jupyterselenium.notebook import Notebook
from selenium import webdriver

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls, nbName, nbFolderPath):
        cls.jsi = Instance(nbFolderPath) #jsi = jupyter selenium instance
        cls.driver = cls.jsi.driver
        cls.loadNotebook(nbName, cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.jsi.killJupyterNotebook()
        cls.driver.close()
        cls.driver.quit()

    @classmethod
    def loadNotebook(cls, nbName, driver):
        nbPath =  "/notebooks/" + nbName
        cls.jsi.loadNotebookIntoDriver(nbPath)
        cls.notebook = Notebook(driver)
        