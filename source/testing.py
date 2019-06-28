from selenium import webdriver
from source.controls import Keyword
import time

# Create driver, set wait, load page
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://webapp4.asu.edu/catalog/classlist')

# Testing Zone
###############################################################################

k = Keyword(driver)

print('Options:', k.checker())
print('Default Value:', k.getter())

test_list = ['this', 'is', 'some', 'text', '234', '342rr3f', '0reg0']

for text in test_list:
    time.sleep(1)
    k.setter(text)
    if k.getter() == text:
        print(text, 'passed!')
    else:
        print(text, 'failed!')

###############################################################################

# Allow extra time to look at page
time.sleep(5)

# Exit Selenium
driver.quit()
