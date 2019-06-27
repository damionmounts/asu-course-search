from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def move_and_click(driver: WebDriver, element: WebElement):
    ActionChains(driver).move_to_element(element).click(element).perform()