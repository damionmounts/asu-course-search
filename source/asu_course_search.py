from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Optional, Union, Set, Dict
from source.controls import AbstractControl, InPersonOrOnline, OpenOrAll, \
                             Term, Subject, Number, Keyword, Session, Location


# Class to represent the entire asu-course-search program
class ASUCourseSearch:

    def __init__(self):

        # Create driver, set timeout, fetch course search page
        self.driver: WebDriver = \
            webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.get('https://webapp4.asu.edu/catalog/classlist')

        # Maps name of control to its instance
        self.controls: Dict[str, AbstractControl] = {
            'PersonOnline': InPersonOrOnline(self.driver),
            'Term': Term(self.driver),
            'Subject': Subject(self.driver),
            'Number': Number(self.driver),
            'Keyword': Keyword(self.driver),
            'Session': Session(self.driver),
            'Location': Location(self.driver),
            'OpenAll': OpenOrAll(self.driver)
        }

    # Quit program and close selenium instance
    def quit(self):
        self.driver.quit()

    # Returns the valid option names of all AbstractControls
    def checker(self) -> Set[str]:
        return set(self.controls.keys())

    # Gets the valid options of the AbstractControl named control
    def control_checker(self, control: str) -> Set[str]:
        pass

    # Sets the AbstractControl named control to value
    def control_setter(self, control: str,
                       value: Union[str, Set[str]]) -> None:
        pass

    # Returns the current value of the AbstractControl instance named control
    #   -Single selection controls return str or None
    #   -Multi-section controls return Set[str] (can be empty for no-selection)
    def control_getter(self, control: str) -> Optional[Union[str, Set[str]]]:
        pass
