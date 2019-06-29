from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from typing import Optional, Union, Set, Dict

from fields.keyword import Keyword
from fields.number import Number
from fields.split_multi_selection import Session, Location
from fields.abstract import AbstractField
from fields.radio_group import PersonOnline, OpenAll
from fields.term import Term
from fields.subject import Subject
from search_results import SearchResults


# Class to represent the entire asu-course-search program
class ASUCourseSearch:

    def __init__(self):

        # Create driver, set timeout, fetch course search page
        self.driver: WebDriver = \
            webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.get('https://webapp4.asu.edu/catalog/classlist')

        # ToDo: Just make these attributes to allow simplified access
        # Maps name of control to its instance
        self.fields: Dict[str, AbstractField] = {
            'PersonOnline': PersonOnline(self.driver),
            'Term': Term(self.driver),
            'Subject': Subject(self.driver),
            'Number': Number(self.driver),
            'Keyword': Keyword(self.driver),
            'Session': Session(self.driver),
            'Location': Location(self.driver),
            'OpenAll': OpenAll(self.driver)
        }

        self.searcher = SearchResults(self.driver)

    # Quit program and close selenium instance
    def quit(self):
        self.driver.quit()

    # Returns the names of all AbstractFields
    def field_names(self) -> Set[str]:
        return set(self.fields.keys())

    # Gets the valid options of the AbstractField named field
    #   Returns None upon getting an invalid field name
    def field_options(self, field: str) -> Optional[Union[str, Set[str]]]:
        try:
            return self.fields[field].valid_options
        except KeyError:
            print('[' + field + '] is not a valid field name.')
            print('Valid field names:', self.field_names())
            return None

    # Sets the AbstractField named field to value
    def set_field(self, field: str, value: Union[str, Set[str]]) -> None:
        try:
            self.fields[field].setter(value)
        except KeyError:
            print('[' + field + '] is not a valid field name.')
            print('Valid field names:', self.field_names())
            return None

    # ToDo: None is a normal result from this method, employ logging or a form
    #   of explicit error return here.
    # Returns the current value of the AbstractField instance named field
    #   -Single selection fields return str or None
    #   -Multi-section fields return Set[str] (can be empty for no-selection)
    def get_field(self, field: str) -> Optional[Union[str, Set[str]]]:
        try:
            return self.fields[field].getter()
        except KeyError:
            print('[' + field + '] is not a valid field name.')
            print('Valid field names:', self.field_names())
            return None
