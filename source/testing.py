from selenium import webdriver
from source.controls import Term
import time

# Create driver, set wait, load page
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://webapp4.asu.edu/catalog/classlist')

# Testing Zone
###############################################################################

t = Term(driver)
print(t.checker())
print(t.getter())


for term in t.checker():
    time.sleep(3)
    print('------------------------------')
    print('Setting term = ' + term)
    t.setter(term)
    print('Term = ' + t.getter())

###############################################################################

# Allow extra time to look at page
time.sleep(5)

# Exit Selenium
driver.quit()
