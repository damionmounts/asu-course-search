from abc import ABC, abstractmethod
from typing import Set, Union, Optional
from selenium.webdriver.chrome.webdriver import WebDriver


# Models the base required methods of a control class
#   typing here is used for documentation purposes,
#   it is not enforceable with Python's design
class AbstractControl(ABC):

    # ToDo: Determine how to structure resource passing
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
    def getter(self) -> str:
        pass


class InPersonOrOnline(AbstractControl):
    pass


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
