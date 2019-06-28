from abc import ABC, abstractmethod

from typing import Optional, Set, Union

from selenium.webdriver.chrome.webdriver import WebDriver


# Models the base required methods of a control class
#   typing here is used for documentation purposes,
#   it is not enforceable with Python's design
class AbstractField(ABC):

    # Input: reference(s) to shared application resources
    # Output: -
    @abstractmethod
    def __init__(self, driver: WebDriver):

        # Reference to the Selenium web driver instance
        self.driver = driver

        # Valid options variable of any type depending on input style.
        #   None by default as options haven't been checked.
        self.valid_options = None

    # Input: string or set of strings that are the choice
    #   -str: for fields that can only hold 1 value
    #   -Set[str]: for fields that allow multi-selection
    # Output: -
    @abstractmethod
    def setter(self, value: Union[str, Set[str]]) -> None:
        pass

    # Input: -
    # Output: string that is the current value on the page
    @abstractmethod
    def getter(self) -> Optional[Union[str, Set[str]]]:
        pass
