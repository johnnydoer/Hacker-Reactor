from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class Tests():
    def __init__(self, driver):
        if driver == "Mozilla":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
    def closeBrowser(self):
        self.driver.close()

    def loginTest(self):
        driver = self.driver
        driver.find_element_by_id("id_emailid").send_keys("")
        driver.find_element_by_id("").send_keys("")
        driver.find_element_by_id("").click()