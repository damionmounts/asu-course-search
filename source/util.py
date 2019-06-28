from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


# Move to and then click element, prevents trying to click off-screen
def move_and_click(driver: WebDriver, element: WebElement) -> None:
    ActionChains(driver).move_to_element(element).click(element).perform()


# Wait for loading banner to disappear
def wait_load(driver: WebDriver) -> None:
    WebDriverWait(driver, 10).until(
        ec.invisibility_of_element_located((By.ID, 'loading-alert')))


# Checks if str is a valid int
def is_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False
