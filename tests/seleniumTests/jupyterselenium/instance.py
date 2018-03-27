from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import os, time, sys, subprocess

from .runPixiedustNotebooks import createKernelSpecIfNeeded
from .runPixiedustNotebooks import __TEST_KERNEL_NAME__ 


#organizing inputs for expanding framework to be more modular
NOTEBOOKS_PATH = "path"
CELL_EXECUTION_WAIT_TIME = 30
DRIVER_TYPE = 'chrome'
KERNEL_NAME = __TEST_KERNEL_NAME__
SPARK = True
RUN_IN_BACKGROUND = True

class Instance():

    class NotebookFailedToStartException(Exception):
        pass

    class NoKernelSetException(Exception):
        pass

    class PythonErrorInNotebook(Exception):
        pass

    def __init__(self, nbFolderPath):
        self.tokenUrl = ""
        self.baseUrl = ""
        self.pid = 0
        self.driver = None
        self.jupyterProc = None
        self.nbFolderPath = nbFolderPath
        
        try:
            createKernelSpecIfNeeded(useSpark=SPARK)
            self.startJupyterNotebookInBackground()
            self.startDriverAndLoadJupyter()
        except Exception(): 
            self.killJupyterNotebook()
            raise Instance.NotebookFailedToStartException()

    def startJupyterNotebookInBackground(self):
        # the pid plus 1 is there because the shell, which is necessary, 
        # is the pid returned for the shell instance process,
        # but the child process (jupyter) is immediately created 
        # and that jupyter process pid is the shell process pid + 1
        JUPYTER_CMD = "jupyter notebook --no-browser  --notebook-dir=" + self.nbFolderPath + " > nohup.out 2>&1 &"
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
            with open("nohup.out", "r") as nohup:
                nohupTxt = nohup.read()
            self.parseOutTokenUrl(nohupTxt)
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
                self.tokenUrl = tokenUrl.strip()
                return
        
    def parseOutBaseUrl(self):
        end_i = self.tokenUrl.find("?")
        self.baseUrl = self.tokenUrl[:end_i - 1]

    def loadNotebookIntoDriver(self, nbPath):
        self.driver.get(self.baseUrl + nbPath)
        self.selectTestKernel()
        self.waitForJupyterKernalToLoad()
        self.runAllCells()
        self.waitForCellsToComplete()

    def selectTestKernel(self):
        try:
            #popup menu if no default kernel is set
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div/div[2]/form"))
            )  
            kernelForm = self.driver.find_element_by_xpath("/html/body/div[8]/div/div/div[2]/form/select")
            kernelForm.click()
            testKernel = self.driver.find_element_by_xpath("/html/body/div[8]/div/div/div[2]/form/select/option[@value='{0}']".format(KERNEL_NAME.lower()))
            testKernel.click()
            setKernelBtn = self.driver.find_element_by_xpath("/html/body/div[8]/div/div/div[3]/button[2]")
            setKernelBtn.click()
        except(NoSuchElementException, TimeoutException):
            try:
                kernelBtn = self.driver.find_element_by_xpath("//*[@id=\"menus\"]/div/div/ul/li[6]")
                kernelBtn.click()
                kernelSelector = self.driver.find_element_by_xpath("//*[@id=\"menu-change-kernel\"]")
                ActionChains(self.driver).move_to_element(kernelSelector).perform()
                setTestKernelBtn = self.driver.find_element_by_xpath("//*[@id=\"kernel-submenu-{0}\"]".format(KERNEL_NAME.lower()))
                setTestKernelBtn.click()
            except NoSuchElementException as e:
                print(e.msg)
                raise Instance.NoKernelSetException("No kernel was set!")

    def runAllCells(self):
        cellButton = self.driver.find_element_by_xpath("//*[@id=\"menus\"]/div/div/ul/li[5]")
        cellButton.click()
        self.driver.find_element_by_id("run_all_cells").click()
        self.waitForCellsToComplete()

    #selenium custom wait
    class wait_for_value_to_contain(object):
        def __init__(self, locator, val):
            self.locator = locator
            self.val = val

        def __call__(self, driver):
            element = driver.find_element(*self.locator)   # Finding the referenced element
            if self.val in element.text:
                return element
            else:
                return False
                
    def waitForJupyterKernalToLoad(self):
        kernelIndicator = self.driver.find_element_by_xpath("//*[@id=\"kernel_indicator_icon\"]")
        #kernel being idle means it is already loaded and you don't have to wait
        if(kernelIndicator.get_attribute("class") == "kernel_idle_icon"):
            return

        wait = WebDriverWait(self.driver, 10)
        kernalNotifierXpath= "//*[@id=\"notification_kernel\"]/span"
        kernalLoaded = wait.until(Instance.wait_for_value_to_contain(
                (By.XPATH, kernalNotifierXpath), "Kernel ready"))
        if(kernalLoaded == False):
            raise Instance.NoKernelSetException()
        
        #selenium custom wait

    class wait_for_python_error_or_cell_completion():
        def __init__(self, driver):
            numOfCodeCells = len(driver.find_elements_by_xpath("//*[@id='notebook-container']/div[contains(@class, 'code_cell')]"))
            numOfEmptyCodeCells = 0
            for cell_i in range(1, numOfCodeCells):
                xpathOfCellRunIndicator = "//*[@id='notebook-container']/div[{0}]/div[1]/div[1]".format(cell_i)
                emptyCellIndicatorText = driver.find_element_by_xpath(xpathOfCellRunIndicator).text
                if(emptyCellIndicatorText == "In [ ]:"):
                    numOfEmptyCodeCells += 1
            self.numOfNonEmptyCodeCells = numOfCodeCells - numOfEmptyCodeCells

        def __call__(self, driver):
            try:
                #see if all outputs exist, this  means all cells ran
                for i in range(1, self.numOfNonEmptyCodeCells):
                    xpathOfIthCellOutput = "//*[@id='notebook-container']/div[{0}]/div[2]/div[2]/div".format(i)
                    driver.find_element_by_xpath(xpathOfIthCellOutput)
            except NoSuchElementException:
                #check for error
                error = True
                try:
                    driver.find_element_by_xpath("//*[contains(@class, 'output_error')]")
                except NoSuchElementException:
                    error = False
                if(error == True ):
                    raise Instance.PythonErrorInNotebook
                else:
                    return False

            return True

    def waitForCellsToComplete(self):
        wait = WebDriverWait(self.driver, CELL_EXECUTION_WAIT_TIME)
        wait.until(Instance.wait_for_python_error_or_cell_completion(self.driver))

    def killJupyterNotebook(self):
        print("Killing jupyter server and shell...")
        os.system('kill ' + str(self.pid))
        self.jupyterProc.kill()


