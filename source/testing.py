from selenium import webdriver
from source.controls import Subject
import time

# Create driver, set wait, load page
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://webapp4.asu.edu/catalog/classlist')

# Testing Zone
###############################################################################

# Subject instance to test
s = Subject(driver)

# Get options, print amount, print each
options = s.checker()
amt_opts = len(options)
print('There are', amt_opts, 'options available.')
for ind, opt in enumerate(options):
    print('Option', ind, 'is', opt)

# Spacing before test
print()

# Try all valid options and ensure they are being set
for opt in options:
    s.setter(opt)
    if s.getter() == opt:
        print(opt, 'passed.')
    else:
        print(opt, 'FAILED!')

# Spacing before next test
print()

# Try invalid options and ensure field never changed
invalids = ['YEET', 'woke', 'IAmNotValid']

before = s.getter()

for inv in invalids:
    print('Setting', inv)
    s.setter(inv)

if before == s.getter():
    print('No invalid accepted, pass.')
else:
    print('Field changed during attempted invalid setting, FAIL!')

###############################################################################

# Allow extra time to look at page
time.sleep(5)

# Exit Selenium
driver.quit()
