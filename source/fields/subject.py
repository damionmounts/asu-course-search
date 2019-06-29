from bs4 import BeautifulSoup

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .abstract import AbstractField

from util import safe_click


# Models subject entry box control
class Subject(AbstractField):

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
            safe_click(self.driver, toggle_adv_search)
            if not adv_search.is_displayed():
                print("id='advanced-search' is not appearing. Could not init"
                      " valid option set for subject.")
                return

        # Click 'browse by subject' to open full subject list
        locator = (By.XPATH, "//div[@id='advanced-search']/div[3]/div/div/a")
        open_subject_list = WebDriverWait(self.driver, 10) \
            .until(ec.visibility_of_element_located(locator))
        safe_click(self.driver, open_subject_list)

        # Wait for visibility of full subject list
        locator = (By.ID, 'subjectList')
        WebDriverWait(self.driver, 10) \
            .until(ec.visibility_of_element_located(locator))

        # Explicitly click 'Show All' button of subject list
        xpath = "//div[@id='subjectList']/div[1]/a[24]"
        show_all = self.driver.find_element_by_xpath(xpath)
        safe_click(self.driver, show_all)

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
            safe_click(self.driver, self.header)

    # Return current field value
    def getter(self) -> str:
        return self.entry.get_attribute('value')
