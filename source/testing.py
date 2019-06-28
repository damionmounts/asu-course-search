import time

from asu_course_search import ASUCourseSearch

a = ASUCourseSearch()

# Search for all English classes
a.set_field('Subject', 'ENG')
a.set_field('Number', '')
a.set_field('OpenAll', 'all')
a.searcher.search()

# Get all page nums besides the first, (already on page 1)
pages = a.searcher.get_page_numbers()
pages.remove(1)

# Click through each page
for page in pages:
    a.searcher.click_page_number(str(page))
    time.sleep(2)

a.quit()