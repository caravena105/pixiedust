from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import time
import sys
sys.path.append(os.path.abspath(".."))
import runPixiedustNotebooks as runPixie
import subprocess
import unittest


def getNotebookFolderPath():
    notebookFolderPath = os.getcwd()
    notebookFolderPath = os.path.abspath(os.path.join(notebookFolderPath, ".."))
    return notebookFolderPath

NOTEBOOKS_PATH = getNotebookFolderPath()

def getNotebookPaths():
    files = os.listdir(getNotebookFolderPath())
    notebooks = filter(lambda file: ".ipynb" in file, files)
    notebooks = filter(lambda file: not ".ipynb_checkpoints" in file, notebooks)
    return list(map(lambda notebook: "/notebooks/" + notebook, notebooks))

class Instance():

    def __init__(self):
        runPixie.createKernelSpecIfNeeded()
        self.tokenUrl = ""
        self.baseUrl = ""
        self.pid = 0
        self.driver = None
        #self.checkIfJupyterNotebookIsAlreadyRunning() if so get this instance jupyter notebook list
        self.startJupyterNotebookInBackground()
        self.getJupyterUrlFromNohup()
        self.loadJupyterIntoDriver()
        self.loadNotebookIntoDriver(getNotebookPaths()[0])
        #self.waitForJupyterKernalToLoad()
        self.runAllCells()
        #self.waitForCellsToRun()

    def startJupyterNotebookInBackground(self):
        # the pid plus 1 is there because the shell, which is necessary, 
        # is the pid returned for the shell instance process,
        # but the child process (jupyter) is immediately created 
        # and that jupyter process pid is the shell process pid + 1
        # P.S. make sure to understand nohup and & symbol if you aren't familiar with those
        JUPYTER_CMD = "nohup jupyter notebook --no-browser  --notebook-dir=" + NOTEBOOKS_PATH + "&"
        self.pid = subprocess.Popen(JUPYTER_CMD, shell=True).pid + 1
        # wait for jupyter notebook to initialize
        time.sleep(3)
        print("Running jupyter server on pid: " + str(self.pid))

    def killJupyterNotebook(self):
        print("Killing jupyter server!")
        os.system('kill ' + str(self.pid))

    def getJupyterUrlFromNohup(self):
        try:
            nohup = open("nohup.out", "r").read()
            self.parseOutTokenUrl(nohup)
            self.parseOutBaseUrl()
        except IOError:
            print("Error: Problem opening nohup.out file.")
        finally:
            os.system("rm nohup.out")

    def parseOutTokenUrl(self, nohup):
        nohup_split = nohup.splitlines()
        for line in nohup_split:
            line = line.strip()
            if "http" in line:
                begin_i= int(line.find("http"))
                tokenUrl = line[begin_i:]
                print("Jupyter tokenUrl:" + tokenUrl)
                self.tokenUrl = tokenUrl.strip()

    def parseOutBaseUrl(self):
        end_i = self.tokenUrl.find("?")
        self.baseUrl = self.tokenUrl[:end_i - 1]
        
    def loadJupyterIntoDriver(self):
        self.driver = webdriver.Chrome()
        # have to open first with token to authenticate 
        self.driver.get(self.tokenUrl)

    def loadNotebookIntoDriver(self, nbPath):
        self.driver.get(self.baseUrl + nbPath)

    def runAllCells(self):
        cellButton = self.driver.find_element_by_xpath("//*[@id=\"menus\"]/div/div/ul/li[5]")
        cellButton.click()
        self.driver.find_element_by_id("run_all_cells").click()
        #self.waitForCellsToComplete()

    def waitForJupyterKernalToLoad(self):
        self.driver.find_element_by_xpath("//*[@id=\"kernel_indicator\"]")  

class Notebook():
    def __init__(self):
        self.cells = []

class Cell():
    #Just holds xpath location of cell in jsi driver
    def __init__(self, driver):
        self.xpath = ""
        self.cellNumber = 0 #cell input prompt.input_prompt bdi 

    def getXPath(self, driver):
        self.xpath = "" 

    def __setXPath__(self):
        self.outputHtml = "" #output_wrapper output

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.jsi = Instance() #jsi = jupyter selenium instance
            cls.jn = Notebook() # jn = jupyter notebook
        except:
            cls.jsi.killJupyterNotebook()
            cls.jsi.driver.close()

    @classmethod
    def tearDownClass(cls):
        cls.jsi.killJupyterNotebook()
        cls.jsi.driver.close()

i = Instance()
time.sleep(5)
i.killJupyterNotebook()
i.driver.close()
