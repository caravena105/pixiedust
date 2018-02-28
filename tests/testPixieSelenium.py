
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import sys
sys.path.append(os.path.abspath("."))
import runPixiedustNotebooks as runPixie
import subprocess

class JupyterSeleniumInstance():

    def __init__(self):
        self.url = ""
        self.pid = 0

    def startJupyterNotebookInBackground(self):
        # the pid plus 1 is there because the shell, which is necessary, 
        # is the pid returned for the shell instance process,
        # but the child process (jupyter) is immediately created 
        # and there is the shell process pid + 1
        # lookup nohup and & symbol if you aren't familiar with those
        self.pid = subprocess.Popen("nohup jupyter notebook --no-browser &", shell=True).pid + 1
        #wait for jupyter notebook to initialize
        print("Running jupyter server on pid:" + str(self.pid))
        time.sleep(3)

    def killJupyterNotebook(self):
        os.system('kill ' + str(self.pid))

    def getJupyterUrlFromNohup(self):
        try:
            nohup = open("nohup.out", "r").read()
            return self.parseOutUrl(nohup)
        except IOError:
            print("Error: Problem opening nohup.out file.")
        finally:
            os.system("rm nohup.out")

    def parseOutUrl(self, nohup):
        nohup_split = nohup.splitlines()
        for line in nohup_split:
            line = line.strip()
            if "http" in line:
                begin_i= int(line.find("http"))
                url = line[begin_i:]
                print("Jupyter url:" + url)
                self.url = url.strip()

#not tested fully, but it should load in the pixiedust kernal
#if it doesn't exist
runPixie.createKernelSpecIfNeeded()

try:
    jsi = JupyterSeleniumInstance()
    jsi.startJupyterNotebookInBackground()
    jsi.getJupyterUrlFromNohup()
    driver = webdriver.Chrome()
    driver.get(jsi.url)
finally:
    time.sleep(10)
    jsi.killJupyterNotebook()



