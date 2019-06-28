from selenium import webdriver
from source.controls import Session
import time

# Create driver, set wait, load page
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://webapp4.asu.edu/catalog/classlist')

# Testing Zone
###############################################################################

###############################################################################

# Allow extra time to look at page
time.sleep(5)

# Exit Selenium
driver.quit()
