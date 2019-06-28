from typing import Tuple, Set

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .abstract import AbstractControl

from util import move_and_click, wait_load


# Models a multi-selection drop-down list that is a button and a ul
class SplitMultiSelection(AbstractControl):

    # button and dropdown are locator tuples of the components
    # Example: button = (By.ID, 'session-button')
    def __init__(self, driver: WebDriver, button_loc: Tuple[str, str],
                 dropdown_loc: Tuple[str, str]):
        super().__init__(driver)

        # Find button and dropdown elements
        self.button = self.driver.find_element(*button_loc)
        self.dropdown = self.driver.find_elements(*dropdown_loc)

        # Set valid options to blank set so items can be added
        self.valid_options = set()

        # Open menu
        move_and_click(self.driver, self.button)

        # Get text of all entries for options set
        for item in self.dropdown:
            span_item = item.find_element_by_tag_name('span')
            text = span_item.text.strip()
            self.valid_options.add(text)

        # Close menu
        move_and_click(self.driver, self.button)

    # Return string set of current selections
    def setter(self, value: Set[str]) -> None:

        # If any selection of the selection-set is invalid, alert and return
        invalids = value - self.valid_options
        if len(invalids) != 0:
            print('These selections are invalid:', invalids)
            print('Valid options are:', self.valid_options)
            print('Nothing will be set until the entire input is correct.')
            return

        # Open menu
        move_and_click(self.driver, self.button)

        # Go through options and change if necessary
        for item in self.dropdown:
            text = item.find_element_by_tag_name('span').text.strip()
            input_ = item.find_element_by_tag_name('input')

            # Ensure input is set
            if text in value:
                if not input_.get_attribute('checked'):
                    move_and_click(self.driver, input_)
                    wait_load(self.driver)

            # Ensure input is not set
            else:
                if input_.get_attribute('checked'):
                    move_and_click(self.driver, input_)
                    wait_load(self.driver)

        # Close menu
        move_and_click(self.driver, self.button)

    def getter(self) -> Set[str]:

        # Start with empty string set
        current_selection: Set[str] = set()

        # Open menu
        move_and_click(self.driver, self.button)

        # Run through all input items
        for item in self.dropdown:
            input_ = item.find_element_by_tag_name('input')
            if input_.get_attribute('checked'):
                text = item.find_element_by_tag_name('span').text.strip()
                current_selection.add(text)

        # Close menu
        move_and_click(self.driver, self.button)

        # Return selection
        return current_selection


# Models session dropdown
class Session(SplitMultiSelection):

    def __init__(self, driver: WebDriver):
        button = (By.ID, 'session-button')
        dropdown = (By.XPATH, "//form[@id='advancedForm']/div[2]/div[2]/div[4]"
                              "/div[2]/div/div/div/div/ul/li")
        super().__init__(driver, button, dropdown)


# Models location dropdown
# Visually hidden when person/online = 'online'
class Location(SplitMultiSelection):

    def __init__(self, driver: WebDriver):
        button = (By.ID, 'location-button')
        dropdown = (By.XPATH, "//form[@id='advancedForm']/div[2]/div[2]/div[4]"
                              "/div[3]/div/div/div/div/ul/li")
        super().__init__(driver, button, dropdown)
