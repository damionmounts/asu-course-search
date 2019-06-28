from selenium import webdriver
from source.controls import Number
import time

# Create driver, set wait, load page
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://webapp4.asu.edu/catalog/classlist')

# Testing Zone
###############################################################################

n = Number(driver)

print('Valid options:', n.checker())
print('Current value:', n.getter())

n.setter('123')
n.setter('Yes')
n.setter('stringy')
print(n.getter())

while True:
    n.setter(str(int(n.getter()) + 1))

###############################################################################

# Allow extra time to look at page
time.sleep(5)

# Exit Selenium
driver.quit()
