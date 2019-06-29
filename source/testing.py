from asu_course_search import ASUCourseSearch
import time

start = time.time()

s = ASUCourseSearch()

s.set_field('PersonOnline', 'person')
s.set_field('Term', 'Fall 2019')
s.set_field('Subject', 'ENG')
s.set_field('OpenAll', 'all')

s.searcher.search()
pages = s.searcher.get_page_numbers()
pages.remove(1)

for page in pages:
    s.searcher.click_page_number(str(page))

s.quit()

finish = time.time()

print('Whole operation took ' + str(finish - start) + 's.')