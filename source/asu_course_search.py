from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from typing import Optional, Union, Set, Dict

from controls.keyword import Keyword
from controls.number import Number
from controls.split_multi_selection import Session, Location
from controls.abstract import AbstractControl
from controls.radio_group import PersonOnline, OpenAll
from controls.term import Term
from controls.subject import Subject


# Class to represent the entire asu-course-search program
class ASUCourseSearch:

    def __init__(self):

        # Create driver, set timeout, fetch course search page
        self.__driver: WebDriver = \
            webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
        self.__driver.implicitly_wait(10)
        self.__driver.get('https://webapp4.asu.edu/catalog/classlist')

        # Maps name of control to its instance
        self.__controls: Dict[str, AbstractControl] = {
            'PersonOnline': PersonOnline(self.__driver),
            'Term': Term(self.__driver),
            'Subject': Subject(self.__driver),
            'Number': Number(self.__driver),
            'Keyword': Keyword(self.__driver),
            'Session': Session(self.__driver),
            'Location': Location(self.__driver),
            'OpenAll': OpenAll(self.__driver)
        }

    # Quit program and close selenium instance
    def quit(self):
        self.__driver.quit()

    # Returns the valid option names of all AbstractControls
    def checker(self) -> Set[str]:
        return set(self.__controls.keys())

    # Gets the valid options of the AbstractControl named control
    def control_checker(self, control: str) -> Union[str, Set[str]]:
        return self.__controls[control].valid_options

    # Sets the AbstractControl named control to val
    def control_setter(self, control: str, val: Union[str, Set[str]]) -> None:
        self.__controls[control].setter(val)

    # Returns the current value of the AbstractControl instance named control
    #   -Single selection controls return str or None
    #   -Multi-section controls return Set[str] (can be empty for no-selection)
    def control_getter(self, control: str) -> Optional[Union[str, Set[str]]]:
        return self.__controls[control].getter()
