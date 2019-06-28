from abc import ABC, abstractmethod
from typing import Set, Union, Optional, Dict, Tuple, List

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Entry is the subject box, header is used to click-off after entry
        self.entry = self.driver.find_element_by_id('subjectEntry')
        self.header = self.driver.find_element_by_id('class-header')

        # Toggle used to open advanced search to get a full list of subjects
        toggle_adv_search = self.driver \
            .find_element_by_class_name('toggle-advanced-search')
        adv_search = self.driver.find_element_by_id('advanced-search')

        # Attempt to open advanced search menu and return on failure
        if not adv_search.is_displayed():
            move_and_click(self.driver, toggle_adv_search)
            if not adv_search.is_displayed():
                print("id='advanced-search' is not appearing. Could not init"
                      " valid option set for subject.")
                return

        # Click 'browse by subject' to open full subject list
        locator = (By.XPATH, "//div[@id='advanced-search']/div[3]/div/div/a")
        open_subject_list = WebDriverWait(self.driver, 10) \
            .until(EC.visibility_of_element_located(locator))
        move_and_click(self.driver, open_subject_list)

        # Wait for visibility of full subject list
        locator = (By.ID, 'subjectList')
        full_sub_list = WebDriverWait(self.driver, 10) \
            .until(EC.visibility_of_element_located(locator))

        # Explicitly click 'Show All' button of subject list
        xpath = "//div[@id='subjectList']/div[1]/a[24]"
        show_all = self.driver.find_element_by_xpath(xpath)
        move_and_click(self.driver, show_all)

        # Use BeautifulSoup to get the visible text of the listed subjects
        subject_list = self.driver.find_element_by_id('list')
        sub_list_html = subject_list.get_attribute('innerHTML')
        soup = BeautifulSoup(sub_list_html, 'html.parser')
        sub_list_entries = soup.find_all('span')

        # ToDo: Possibly dictionary to group codes -> subject names
        self.valid_options = set()  # Valid option codes 'ENG', 'CSE', ..
        self.subject_list = set()  # Full names 'FIN Finance', 'FRE French'

        for entry in sub_list_entries:
            text = entry.text.strip()
            subject_code = text.split(' ', 1)[0]
            self.valid_options.add(subject_code)
            self.subject_list.add(text)

    # Return valid options set of strings
    def checker(self) -> Set[str]:
        return self.valid_options

    # Set field to value
    def setter(self, value: str) -> None:

        # If value is invalid, warn and print valid options
        if value not in self.valid_options:
            print('Could not set invalid subject [' + value + '].')
            print('Valid options are: ' + str(self.valid_options))
            return

        # If box contents need to be changed, change them
        if self.getter() != value:
            self.entry.clear()
            self.entry.send_keys(value)
            move_and_click(self.driver, self.header)

    # Return current field value
    def getter(self) -> str:
        return self.entry.get_attribute('value')


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

    # Return set of valid option strings
    def checker(self) -> Set[str]:
        return self.valid_options

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


class Session(SplitMultiSelection):

    def __init__(self, driver: WebDriver):
        button = (By.ID, 'session-button')
        dropdown = (
            By.XPATH,
            "//form[@id='advancedForm']/div[2]/div[2]/div[4]/div[2]/div/div/div/div/ul/li"
        )
        super().__init__(driver, button, dropdown)


# Visually hidden when person/online = 'online'
class Location(SplitMultiSelection):

    def __init__(self, driver: WebDriver):
        button = (By.ID, 'location-button')
        dropdown = (
            By.XPATH,
            "//form[@id='advancedForm']/div[2]/div[2]/div[4]/div[3]/div/div/div/div/ul/li"
        )
        super().__init__(driver, button, dropdown)
