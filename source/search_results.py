from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver

from util import move_and_click, wait_load


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
                move_and_click(self.driver, btn_link)
                break
        if found:
            wait_load(self.driver)
        else:
            print('Page ' + page_num + ' not found!')

    # Clicks the search button and waits on loading banner
    def search(self) -> None:
        move_and_click(self.driver, self.search_btn)
        wait_load(self.driver)


# Represents a single class listing in the search results page
class Course:
    pass