from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import os, time, sys, subprocess, unittest

from .runPixiedustNotebooks import createKernelSpecIfNeeded
from .runPixiedustNotebooks import __TEST_KERNEL_NAME__ 


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
        self.tokenUrl = ""
        self.baseUrl = ""
        self.pid = 0
        self.driver = None
        self.jupyterProc = None
        
        createKernelSpecIfNeeded()

        self.startJupyterNotebookInBackground()
        self.startDriverAndLoadJupyter()
        self.loadNotebookIntoDriver(getNotebookPaths()[0])
        self.selectTestKernel()
        time.sleep(5) #using sleep until wait functions implemented
        #self.waitForJupyterKernalToLoad()
        self.runAllCells()
        time.sleep(5) #using sleep until wait functions implemented
        #self.waitForCellsToRun()

    def startJupyterNotebookInBackground(self):
        # the pid plus 1 is there because the shell, which is necessary, 
        # is the pid returned for the shell instance process,
        # but the child process (jupyter) is immediately created 
        # and that jupyter process pid is the shell process pid + 1
        # P.S. make sure to understand nohup and & symbol if you aren't familiar with those
        #+  "--MappingKernelManager.default_kernel_name=" + __TEST_KERNEL_NAME__
        JUPYTER_CMD = "jupyter notebook --no-browser  --notebook-dir=" + NOTEBOOKS_PATH + " > nohup.out 2>&1 &"
        self.jupyterProc = subprocess.Popen(JUPYTER_CMD, shell=True)
        self.pid = self.jupyterProc.pid + 1
        # wait for jupyter notebook to initialize
        time.sleep(3)
        print("Running jupyter server on pid: " + str(self.pid))
        
    def startDriverAndLoadJupyter(self):
        self.getJupyterUrlFromNohup()
        self.driver = webdriver.Chrome()
        # have to open first with token to authenticate 
        self.driver.get(self.tokenUrl)
    
    def getJupyterUrlFromNohup(self):
        try:
            nohup = open("nohup.out", "r")
            nohupTxt = nohup.read()
            self.parseOutTokenUrl(nohupTxt)
            self.parseOutBaseUrl()
        except IOError:
            print("Error: Problem opening nohup.out file.")
        finally:
            nohup.close()
            os.system("rm nohup.out")

    def parseOutTokenUrl(self, nohup):
        nohup_split = nohup.splitlines()
        for line in nohup_split:
            line = line.strip()
            if "http" in line:
                begin_i= int(line.find("http"))
                tokenUrl = line[begin_i:]
                self.tokenUrl = tokenUrl.strip()
                return
        
    def parseOutBaseUrl(self):
        end_i = self.tokenUrl.find("?")
        self.baseUrl = self.tokenUrl[:end_i - 1]

    def loadNotebookIntoDriver(self, nbPath):
        self.driver.get(self.baseUrl + nbPath)
    
    def selectTestKernel(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div/div[2]/form"))
            )  
            kernelForm = self.driver.find_element_by_xpath("/html/body/div[8]/div/div/div[2]/form/select")
            kernelForm.click()
            testKernel = self.driver.find_element_by_xpath("/html/body/div[8]/div/div/div[2]/form/select/option[@value=pixiedusttravistest]")
            testKernel.click()
            setKernelBtn = self.driver.find_element_by_xpath("/html/body/div[8]/div/div/div[3]/button[2]")
            setKernelBtn.click()
        except Exception:
            kernelSetIndicator = self.driver.find_element_by_xpath("//*[@id=\"kernel_indicator\"]/span").text   
            if(kernelSetIndicator == "No Kernel"):
                raise NoKernelSetException("No kernel was set!")

    def runAllCells(self):
        cellButton = self.driver.find_element_by_xpath("//*[@id=\"menus\"]/div/div/ul/li[5]")
        cellButton.click()
        self.driver.find_element_by_id("run_all_cells").click()
        #self.waitForCellsToComplete()

    def waitForJupyterKernalToLoad(self):
        self.driver.find_element_by_xpath("//*[@id=\"kernel_indicator\"]")  
    
    def killJupyterNotebook(self):
        print("Killing jupyter server and shell...")
        os.system('kill ' + str(self.pid - 1))
        self.jupyterProc.kill()

class NoKernelSetException(Exception):
    pass

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
            cls.selectNotebook()
        except:
            cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        cls.jsi.killJupyterNotebook()
        cls.jsi.driver.close()
        cls.jsi.driver.quit()
        time.sleep(1)

    @classmethod
    def loadNotebook(cls):
        None

    @classmethod
    def selectNotebook(cls):
        moduleName = sys.modules[__name__]
    