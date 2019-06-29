from typing import List

from asu_course_search import ASUCourseSearch
from search_results import Course

import time

start = time.time()
s = ASUCourseSearch()
s.set_field('Subject', 'CSE')
s.set_field('OpenAll', 'all')
s.searcher.search()
results: List[Course] = s.searcher.get_search_results()
s.quit()
finish = time.time()

for result in results:
    print(str(result) + '\n')

print(finish - start)