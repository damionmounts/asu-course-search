from selenium import webdriver
from source.asu_course_search import InPersonOrOnline
import time

# Create driver, set wait, load page
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://webapp4.asu.edu/catalog/classlist')

radio = InPersonOrOnline(driver)

print('Valid options:', radio.checker())

print('Currently selected:', radio.getter())

for i in range(4):
    print('\nLoop #', i)
    for option in radio.checker():
        time.sleep(2)
        print('Setting option', option)
        radio.setter(option)
        print('Option is now', radio.getter())

driver.quit()