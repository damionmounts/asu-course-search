import unittest

from bs4 import BeautifulSoup

from source.table_row import extract_row_data


def file_to_tag(file_loc: str):
    file = open(file_loc, 'r')
    html = file.read()
    file.close()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Expected Template, Paste this into {} and fill expected values for test
# 'subject-code': '',
# 'course-num': '',
# 'entry-type': '',
# 'title': '',
# 'designation': '',
# 'sub-type': '',
# 'class-num': '',
# 'instructor': [],
# 'days': [],
# 'start': [],
# 'end': [],
# 'location': [],
# 'dates': [],
# 'session-code': '',
# 'units': '',
# 'open_seats': '',
# 'total_seats': '',
# 'seat_status': '',
# 'general_studies': ''


class TestExtractRowData(unittest.TestCase):

    def test_001(self):
        tr = file_to_tag('./html/test_001.txt')
        actual = extract_row_data(tr)
        expected = {
            'subject-code': 'ENG',
            'course-num': '375',
            'entry-type': 'Main',
            'title': 'Topic: Virgin LTD/Richard Branson',
            'designation': '',
            'sub-type': '',
            'class-num': '75476',
            'instructor': ['Heldt'],
            'days': [''],
            'start': [''],
            'end': [''],
            'location': ['iCourse'],
            'dates': ['08/22 - 09/26'],
            'session-code': 'DYN',
            'units': '1',
            'open_seats': '28',
            'total_seats': '30',
            'seat_status': 'Reserved',
            'general_studies': ''
        }
        self.assertDictEqual(actual, expected)

    def test_002(self):
        tr = file_to_tag('./html/test_002.txt')
        actual = extract_row_data(tr)
        expected = {
            'subject-code': 'PHY',
            'course-num': '131',
            'entry-type': 'Main',
            'title': 'Univ Physics II: Elctrc/Magnet',
            'designation': '',
            'sub-type': '',
            'class-num': '72478',
            'instructor': ['McCartney'],
            'days': ['', 'M', 'F', 'W'],
            'start': ['12:00 AM', '', '', ''],
            'end': ['12:00 AM', '', '', ''],
            'location': ['Internet - Hybrid', 'Tempe - TBA', 'Tempe - TBA', 'Tempe - TBA'],
            'dates': ['08/22 - 12/06', '09/30 - 09/30', '10/18 - 10/18', '11/06 - 11/06'],
            'session-code': 'C',
            'units': '3',
            'open_seats': '46',
            'total_seats': '150',
            'seat_status': 'Reserved',
            'general_studies': 'SQ'
        }
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
