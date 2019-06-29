from typing import List

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from util import safe_click, wait_load


# Represents a single class listing in the search results page
class Course:

    # Creates Course object from BeautifulSoup Tag tr from results
    def __init__(self, tr):
        self.data = {
            'course': '',  # sub-entries have no course text
            'title': '',
            'class_num': '',
            'instructor': '',
            'days': '',
            'start': '',
            'end': '',
            'location': '',
            'dates': '',
            'units': '',
            'seats_open': '',
            'general_studies': '',
            'sub_entries': None  # None for sub-entry, [..] for actual entry
        }
        field_locations = {
            'course': 'subjectNumberColumnValue',
            'title': 'titleColumnValue',
            'class_num': 'classNbrColumnValue',
            'instructor': 'instructorListColumnValue',
            'days': 'dayListColumnValue',
            'start': 'startTimeDateColumnValue',
            'end': 'endTimeDateColumnValue',
            'location': 'locationBuildingColumnValue',
            'dates': 'startDateColumnValue',
            'units': 'hoursColumnValue',
            'seats_open': 'availableSeatsColumnValue',
            'general_studies': 'tooltipRqDesDescrColumnValue'
        }

        # For all fields, locate that portion of the tr
        for field, location in field_locations.items():
            td_item = tr.find('td', {'class': location})

            # Special override for title
            # Title can be contained in <a> or <div> if no <a> in that order
            if field == 'title':
                a = td_item.find('a', recursive=False)
                if a:
                    text = a.text
                else:
                    div = td_item.find('div', recursive=False)
                    text = div.text
            else:
                text = td_item.text

            # Split the string apart to get rid of \t\n and then rejoin
            self.data[field] = ' '.join(text.split())

    # Sub entries have no course text
    def is_sub_entry(self):
        return not self.data['course']

    # Nicely formatted printing for courses and sub-courses
    # {------------------------------[  (course)
    #       ------------------------,   (sub)
    #       ------------------------]}  (sub)
    def __str__(self):

        # Subs are printed normally as they are just dicts
        if self.is_sub_entry():
            return str(self.data)

        # Entries need to have their sub_entries list managed
        else:

            # Print like a normal dict for all keys before 'sub_entries'
            string = '{'
            for k, v in self.data.items():
                if k != 'sub_entries':
                    string += k + ': ' + v + ', '

                # Sub-entries management
                else:
                    string += k + ': ['

                    # In case of list, print all items with comma and newline.
                    # Last item is printed plain so closings can be added.
                    if self.data['sub_entries']:
                        last_ind = len(self.data['sub_entries']) - 1
                        string += '\n'
                        for ind, sub in enumerate(self.data['sub_entries']):
                            if ind != last_ind:
                                string += '\t' + str(sub) + ',\n'
                            else:
                                string += '\t' + str(sub)

            # Add closings for list and dict
            string += ']}'
            return string


# ToDo: Application needs some state management and communication past just
#   being a conglomeration of methods. Data should be communicated about if
#   locations is being hidden by InPersonal/Online and if the search button
#   has already been clicked. Also if fields have changed after a search,
#   the search button hasn't been clicked, and the results are being read.
# Provides facilities related to searching and results parsing
class SearchResults:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.search_btn = self.driver.find_element_by_id('go_and_search')

    # Returns number of class entries that exist
    def get_number_of_results(self) -> int:
        xpath = "//div[@id='classResults']/div[3]/div"
        result_status = self.driver.find_element_by_xpath(xpath)
        text = result_status.text.strip()  # 'Showing 1 to 100 of 817'
        amount = text.split(' ')[-1]  # '817'
        return int(amount)  # 817

    # Returns list of all available page numbers
    def get_page_numbers(self) -> List[int]:
        amt_results = self.get_number_of_results()
        if amt_results > 0:
            page_nav = self.driver.find_element_by_class_name('pagination')
            nav_btns = page_nav.find_elements_by_tag_name('li')
            nav_btns = [btn.find_element_by_tag_name('a') for btn in nav_btns]
            nav_btns = [btn for btn in nav_btns if btn.get_attribute('page')]
            return [int(btn.text.strip()) for btn in nav_btns]
        else:
            return []

    # Clicks the given page number
    def click_page_number(self, page_num: str) -> None:
        page_nav = self.driver.find_element_by_class_name('pagination')
        nav_btns = page_nav.find_elements_by_tag_name('li')
        found = False
        for btn in nav_btns:
            btn_link = btn.find_element_by_tag_name('a')
            if btn_link.get_attribute('page') == page_num:
                found = True
                safe_click(self.driver, btn_link)
                break
        if found:
            wait_load(self.driver)
        else:
            print('Page ' + page_num + ' not found!')

    # Clicks the search button and waits on loading banner
    def search(self) -> None:
        safe_click(self.driver, self.search_btn)
        wait_load(self.driver)

    # Extend a list of Course(s) by a list of table rows
    def course_list_extend_trs(self, courses, trs):
        for tr in trs:
            course = Course(tr)

            # Sub-entries added to last full course entry
            if course.is_sub_entry():
                courses[-1].data['sub_entries'].append(course)

            # Full course entry has list for subs and is added to course list
            else:
                course.data['sub_entries'] = []
                courses.append(course)

    # Returns a list of Course(s) by going through all search result pages
    def get_search_results(self) -> List[Course]:
        course_list = []

        amt_results = self.get_number_of_results()
        if amt_results == 0:
            return course_list

        table_xpath = "//table[@id='CatalogList']/tbody"
        table_body = self.driver.find_element_by_xpath(table_xpath)
        html = table_body.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        entries = soup.find_all('tr')
        self.course_list_extend_trs(course_list, entries)

        page_nums = self.get_page_numbers()
        page_nums.remove(1)

        for page in page_nums:
            self.click_page_number(str(page))
            table_xpath = "//table[@id='CatalogList']/tbody"
            table_body = self.driver.find_element_by_xpath(table_xpath)
            html = table_body.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            entries = soup.find_all('tr')
            self.course_list_extend_trs(course_list, entries)

        return course_list
