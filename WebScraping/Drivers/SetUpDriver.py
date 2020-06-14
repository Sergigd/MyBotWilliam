from selenium import webdriver
from selenium.webdriver.edge import options as optionsEdge
import os


class Driver(object):
    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(os.curdir))
        # path_opera = os.path.join(root_dir, "Drivers", "operadriver.exe")
        path_edge = os.path.join(root_dir, "Drivers", "msedgedriver.exe")

        # self.webDriver = webdriver.Opera(executable_path=path_opera)
        options = optionsEdge
        options

        self.webDriver = webdriver.Edge()

    def getDriver(self):
        return self.webDriver

    def setURL(self, url):
        self.webDriver.get(url)

    def close(self):
        self.webDriver.close()


myDriver = Driver()
myDriver.setURL("https://www.python.org")
