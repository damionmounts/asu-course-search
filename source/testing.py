from typing import List

from asu_course_search import ASUCourseSearch

import time

start = time.time()
s = ASUCourseSearch()
s.set_field('Subject', 'PHY')
s.set_field('OpenAll', 'all')
s.results.search()
s.results.get_search_results()
finish = time.time()

s.quit()

print('')
print('Completed in ' + str(finish - start) + 's.')