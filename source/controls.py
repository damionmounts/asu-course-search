from abc import ABC, abstractmethod
from typing import Set, Union, Optional, Dict, Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from source.util import move_and_click
from source.util import wait_load
from source.util import is_int


# Models the base required methods of a control class
#   typing here is used for documentation purposes,
#   it is not enforceable with Python's design
class AbstractControl(ABC):

    # Input: reference(s) to shared application resources
    # Output: -
    @abstractmethod
    def __init__(self, driver: WebDriver):

        # Reference to the Selenium web driver instance
        self.driver = driver

        # Holds the set of valid option strings
        self.valid_options: Optional[Set[str]] = None

    # Input: -
    # Output: set of valid option strings
    @abstractmethod
    def checker(self) -> Set[str]:
        pass

    # Input: string or set of strings that are the choice
    #   -str: for controls that can only hold 1 value
    #   -Set[str]: for controls that allow multi-selection
    # Output: -
    @abstractmethod
    def setter(self, value: Union[str, Set[str]]) -> None:
        pass

    # Input: -
    # Output: string that is the current value on the page
    @abstractmethod
    def getter(self) -> Optional[Union[str, Set[str]]]:
        pass


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

    # Return valid options for radio set
    def checker(self) -> Set[str]:
        return self.valid_options

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
class RGPersonOnline(RadioGroup):

    def __init__(self, driver: WebDriver):

        options = {
            'person': (By.ID, 'radio-campus'),
            'online': (By.ID, 'radio-online')
        }
        super().__init__(driver, options)


# Models open/all radio group
class RGOpenAll(RadioGroup):

    def __init__(self, driver: WebDriver):

        options = {
            'open': (By.ID, 'searchTypeOpen'),
            'all': (By.ID, 'searchTypeAllClass')
        }
        super().__init__(driver, options)


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

    # Returns string set of valid term options
    def checker(self) -> Set[str]:
        return self.valid_options

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


class Subject(AbstractControl):
    pass


# Models number entry box control
class Number(AbstractControl):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # WebElement of input box
        self.entry = self.driver.find_element_by_id('catNbr')

        # ToDo: Look into changing valid_option / verification design.
        #   However, ensure that a consistent interface is maintained.
        self.valid_options = {'Numeric Digit Strings Are Valid Options'}

    # Return a set containing a single string explaining valid options
    def checker(self) -> Set[str]:
        return self.valid_options

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


# Models the keyword entry box
class Keyword(AbstractControl):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self.entry = self.driver.find_element_by_id('keyword')
        self.valid_options = {'Literally Anything is Valid Here'}

    # Returns valid options set of a single string
    def checker(self) -> Set[str]:
        return self.valid_options

    # Sets entry box's value
    def setter(self, value: str) -> None:

        # If value has to be changed, change it
        if self.getter() != value:
            self.entry.clear()
            self.entry.send_keys(value)

    # Returns current value of entry box
    def getter(self) -> str:
        return self.entry.get_attribute('value')


class Session(AbstractControl):
    pass


# Visually hidden when person/online = 'online'
class Location(AbstractControl):
    pass
