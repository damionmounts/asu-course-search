from selenium.webdriver.chrome.webdriver import WebDriver

from .abstract import AbstractField


# Models the keyword entry box
class Keyword(AbstractField):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self.entry = self.driver.find_element_by_id('keyword')
        self.valid_options = 'Any Search String Is Valid'

    # Sets entry box's value
    def setter(self, value: str) -> None:

        # If value has to be changed, change it
        if self.getter() != value:
            self.entry.clear()
            self.entry.send_keys(value)

    # Returns current value of entry box
    def getter(self) -> str:
        return self.entry.get_attribute('value')
