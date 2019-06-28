from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from .abstract import AbstractControl


# Models term dropdown control
class Term(AbstractControl):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Term drop-down menu
        menu_element = self.driver.find_element_by_id('term')
        self.menu = Select(menu_element)

        # Get menu options and strip out previous term support
        options: List[WebElement] = self.menu.options
        self.valid_options = {opt.text.strip() for opt in options}
        self.valid_options.remove('Previous terms')

    # Set the term to value
    def setter(self, term: str) -> None:

        # If term not valid, alert and provide valid options
        if term not in self.valid_options:
            print('Could not pick invalid term [' + term + '].')
            print('Valid options are: ' + str(self.valid_options))
            return

        # If term needs to be changed, change it
        if self.getter() != term:
            self.menu.select_by_visible_text(term)

    # Return text of current selected term
    def getter(self) -> str:
        return self.menu.first_selected_option.text.strip()
