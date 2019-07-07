from typing import List, Tuple

from bs4 import BeautifulSoup, NavigableString
from selenium.webdriver.chrome.webdriver import WebDriver

from util import safe_click, wait_load


# Given <tr>, return course text
def tr_course(tr):
    td = tr.find('td', {'class': 'subjectNumberColumnValue'})
    course_text_span = td.find('span')
    if not course_text_span:
        return '<SubEntry>'
    return course_text_span.text.strip()


# Given <tr>, return Title - Designation - Subtype
def tr_title(tr):
    td = tr.find('td', {'class': 'titleColumnValue'})

    # Title | Designation | Sub-type
    title = '-'
    designation = '-'
    subtype = '-'

    # Get title from [div class-results-drawer] or [a course-details-link]
    title_div = td.find('div', {'class': 'class-results-drawer'})
    if title_div:
        title = ' '.join(title_div.text.split())
    else:
        title_a = td.find('a', {'class': 'course-details-link'})
        title = title_a.text.strip()

    # Get designation if present
    designation_container = td.find('span', {'class': 'lab-designation'})
    if designation_container:
        comptip = designation_container.find('span', {'class': 'comptip'})
        designation = comptip.text.strip()

    # Get subtype if present
    cohort_message = td.find('div', {'id': 'cohortMessage'})
    if cohort_message:
        subtype = cohort_message.find(text=True, recursive=False).strip()

    return title + ' | ' + designation + ' | ' + subtype


# Given <tr>, return class number
def tr_class_number(tr):
    td = tr.find('td', {'class': 'classNbrColumnValue'})
    course_number_link = td.find('a')
    return course_number_link.text.strip()


# Given <tr>, return list of instructors
def tr_instructors(tr):
    td = tr.find('td', {'class': 'instructorListColumnValue'})
    list_span = td.find('span', recursive=False)
    list_items = list_span.find_all('span', recursive=False)

    instructors = []

    # Go through all instructor spans in list
    for index, item in enumerate(list_items):
        instructor = item.text.strip()

        # Remove commas on all but last instructor
        if index < len(list_items) - 1:
            instructor = instructor[:-1]

        instructors.append(instructor)

    return instructors


# Given <tr>, return list of days (top-down for each session listed)
def tr_days(tr):
    td = tr.find('td', {'class': 'dayListColumnValue'})
    br_s = td.find_all('br')

    # If there are no linebreaks, return the single line as session 0 in list
    if not br_s:
        return [td.text.strip()]

    days = []

    # If there are br's, return a list where each line is an element
    for child in td.children:
        if type(child) == NavigableString:
            days.append(str(child).strip())

    return days


# Given <tr>, return list of start times (top-down for each session in list)
def tr_starts(tr):
    td = tr.find('td', {'class': 'startTimeDateColumnValue'})
    br_s = td.find_all('br')

    # If there are no linebreaks, return the single line as session 0 in list
    if not br_s:
        return [td.text.strip()]

    starts = []

    # If there are br's, return a list where each line is an element
    for child in td.children:
        if type(child) == NavigableString:
            starts.append(str(child).strip())

    # Extra entry is added because of page formatting, remove it
    del starts[0]
    return starts


# Given <tr>, return list of end times (top-down for each session in list)
def tr_ends(tr):
    td = tr.find('td', {'class': 'endTimeDateColumnValue'})
    br_s = td.find_all('br')

    # If there are no linebreaks, return the single line as session 0 in list
    if not br_s:
        return [td.text.strip()]

    ends = []

    # If there are br's, return a list where each line is an element
    for child in td.children:
        if type(child) == NavigableString:
            ends.append(str(child).strip())

    # Extra entry is added because of page formatting, remove it
    # del ends[0]
    return ends


class MainEntry:

    def __init__(self):
        course: str = ''
        title: str = ''
        designation: str = ''
        class_number: str = ''
        instructor: List[str] = []
        sessions: List[Session] = []
        units: str = ''
        seats_open: List[int] = []
        general_studies: str
        sub_entries: List[Tuple[str, SubEntry]] = []


class Session:

    def __init__(self):
        days: str = ''
        start_time: str = ''
        end_time: str = ''
        location: str = ''
        dates: str = ''


class SubEntry:

    def __init__(self):
        title: str = ''
        designation: str = ''
        class_number: str = ''
        instructor: str = ''
        session: Session = Session()
        units: str = ''
        seats_open: List[int] = []
        general_studies: str = ''


class Results:

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

    def diag_print_trs(self, tr_list):
        for tr in tr_list:
            print('---------------------------------------------------------')
            print('Course: ' + tr_course(tr))
            print('Title: ' + tr_title(tr))
            print('Class#: ' + tr_class_number(tr))
            print('Instructor(s): ' + str(tr_instructors(tr)))
            print('Days: ' + str(tr_days(tr)))
            print('Start(s): ' + str(tr_starts(tr)))
            print('End(s): ' + str(tr_ends(tr)))

    # Returns a list of Course(s) by going through all search result pages
    def get_search_results(self):

        amt_results = self.get_number_of_results()
        if amt_results == 0:
            return

        table_xpath = "//table[@id='CatalogList']/tbody"
        table_body = self.driver.find_element_by_xpath(table_xpath)
        html = table_body.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        entries = soup.find_all('tr')
        self.diag_print_trs(entries)

        page_nums = self.get_page_numbers()
        page_nums.remove(1)

        for page in page_nums:
            self.click_page_number(str(page))
            table_xpath = "//table[@id='CatalogList']/tbody"
            table_body = self.driver.find_element_by_xpath(table_xpath)
            html = table_body.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            entries = soup.find_all('tr')
            self.diag_print_trs(entries)
