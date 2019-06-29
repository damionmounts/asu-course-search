from selenium.webdriver.chrome.webdriver import WebDriver

from .abstract import AbstractField

from util import is_int


# Models number entry box control
class Number(AbstractField):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # WebElement of input box
        self.entry = self.driver.find_element_by_id('catNbr')
        self.valid_options = "Any Numeric Digit String Or '' Is Valid"

    # Set the number box to value
    def setter(self, value: str) -> None:
        if value:  # If value isn't blank, (clearing field)
            if not is_int(value):  # If it isn't a string either
                print('Could not set number box to [' + value + '].')
                print(self.valid_options)
                return

        # Change value
        self.entry.clear()
        self.entry.send_keys(value)

    # Return current value of the box
    def getter(self) -> str:
        return self.entry.get_attribute('value')
