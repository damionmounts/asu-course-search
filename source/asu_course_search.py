from abc import ABC, abstractmethod
from typing import Set, Union, Optional
from selenium.webdriver.chrome.webdriver import WebDriver
from source.util import move_and_click


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


class InPersonOrOnline(AbstractControl):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Connect to radio elements on page
        radio_person = self.driver.find_element_by_id('radio-campus')
        radio_online = self.driver.find_element_by_id('radio-online')

        # Hardcoded options as this is a simple radio set
        self.valid_options = {'person', 'online'}

        # Option mapping
        self.option_to_radio = {
            'person': radio_person,
            'online': radio_online
        }

    # Return hardcoded option set
    def checker(self) -> Set[str]:
        return self.valid_options

    # Set option if not already set
    def setter(self, value: str) -> None:
        if self.getter() != value:
            radio_element = self.option_to_radio[value]
            move_and_click(self.driver, radio_element)

    # Return name of selected radio, or None if neither are selected
    def getter(self) -> Optional[str]:
        person = self.option_to_radio['person'].get_attribute('checked')
        online = self.option_to_radio['online'].get_attribute('checked')
        if person:
            return 'person'
        else:
            if online:
                return 'online'
            else:
                return None


class Term(AbstractControl):
    pass


class Subject(AbstractControl):
    pass

class Number(AbstractControl):
    pass


class Keyword(AbstractControl):
    pass


class Session(AbstractControl):
    pass


class Location(AbstractControl):
    pass


class OpenOrAll(AbstractControl):
    pass
