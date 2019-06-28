from typing import Dict, Tuple, Optional, Set

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .abstract import AbstractControl

from util import move_and_click, wait_load


# Models a radio-group control element defined by the options argument
class RadioGroup(AbstractControl):

    # options is used to add radios to the set upon creation. Example Below:
    # options = {
    #   'open': (By.ID, 'searchTypeOpen'),
    #   'all': (By.ID, 'searchTypeAllClass')
    # }
    def __init__(self, driver: WebDriver, options: Dict[str, Tuple[str, str]]):
        super().__init__(driver)

        # Pull valid option set from options dict
        self.valid_options = set(options.keys())

        # Create mapper for valid option to according radio element
        self.option_to_radio: Dict[str, WebElement] = {}
        for option in self.valid_options:
            radio_element = self.driver.find_element(*options[option])
            self.option_to_radio[option] = radio_element

    # Set option to value
    def setter(self, value: str) -> None:

        # If value is invalid, warn and state valid options
        if value not in self.valid_options:
            print('Could not pick radio named [' + value + '].')
            print('Valid options are: ' + str(self.valid_options))
            return

        # If value is valid and selection must change, change it
        if self.getter() != value:
            radio_element = self.option_to_radio[value]
            move_and_click(self.driver, radio_element)
            wait_load(self.driver)

    # Return name of selected radio, or None if neither are selected
    def getter(self) -> Optional[str]:

        # Go through radios and return the name of the checked radio
        for option in self.valid_options:
            if self.option_to_radio[option].get_attribute('checked'):
                return option

        # If no radio was checked, return None
        return None


# Models in-person/online radio group
class PersonOnline(RadioGroup):

    def __init__(self, driver: WebDriver):

        options = {
            'person': (By.ID, 'radio-campus'),
            'online': (By.ID, 'radio-online')
        }
        super().__init__(driver, options)


# Models open/all radio group
class OpenAll(RadioGroup):

    def __init__(self, driver: WebDriver):

        options = {
            'open': (By.ID, 'searchTypeOpen'),
            'all': (By.ID, 'searchTypeAllClass')
        }
        super().__init__(driver, options)
