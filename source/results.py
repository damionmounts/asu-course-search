from typing import List, Tuple

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from util import safe_click, wait_load


from source.table_row import extract_row_data

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
        general_studies: str = ''
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
            print(extract_row_data(tr))

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
