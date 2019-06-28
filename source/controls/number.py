from selenium.webdriver.chrome.webdriver import WebDriver

from .abstract import AbstractControl

from util import is_int


# Models number entry box control
class Number(AbstractControl):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # WebElement of input box
        self.entry = self.driver.find_element_by_id('catNbr')
        self.valid_options = 'Any Numeric Digit String Is Valid'

    # Set the number box to value
    def setter(self, value: str) -> None:

        # If the value given isn't a numeric string, alert and explain
        if not is_int(value):
            print('Could not set number box to [' + value + '].')
            print(self.valid_options)
            return

        # If value needs to be changed, change it
        if self.getter() != value:
            self.entry.clear()
            self.entry.send_keys(value)

    # Return current value of the box
    def getter(self) -> str:
        return self.entry.get_attribute('value')
