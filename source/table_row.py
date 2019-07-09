from typing import Tuple, List, Dict

from bs4 import NavigableString, Comment


# Input: bs4 Tag <tr>
# Output: dict of all fields in the table-row entry
# Each section here is a <td> within the passed-in <tr>
def extract_row_data(tr) -> Dict:
    data = {}

    # Course
    x, y, z = course(tr)
    data['subject-code'] = x
    data['course-num'] = y
    data['entry-type'] = z

    # Title
    x, y, z = title(tr)
    data['title'] = x
    data['designation'] = y
    data['sub-type'] = z

    # Class#
    x = class_number(tr)
    data['class-num'] = x

    # Instructor
    x = instructor(tr)
    data['instructor'] = x

    # Days
    x = days(tr)
    data['days'] = x

    # Start
    x = start(tr)
    data['start'] = x

    # End
    x = end(tr)
    data['end'] = x

    # Location
    x = location(tr)
    data['location'] = x

    # Dates
    x, y = dates(tr)
    data['dates'] = x
    data['session-code'] = y

    # Units
    x = units(tr)
    data['units'] = x

    # Seats Open
    x, y, z = seats_open(tr)
    data['open_seats'] = x
    data['total_seats'] = y
    data['seat_status'] = z

    # GS
    x = general_studies(tr)
    data['general_studies'] = x

    return data


# Input: bs4 Tag <tr>
# Output: (subject code, course num, entry type)
def course(tr) -> Tuple[str, str, str]:
    td = tr.find('td', {'class': 'subjectNumberColumnValue'})  # Data cell
    course_span = td.find('span')  # Span containing text

    # No text is present -> SubEntry
    if not course_span:
        return '', '', 'Sub'

    # If text found, split code and number then indicate MainEntry
    text = course_span.text.strip()
    subject_code, course_num = text.split()
    return subject_code, course_num, 'Main'


# Input: bs4 Tag <tr>
# Output: (title, designation, sub-type)
def title(tr) -> Tuple[str, str, str]:
    td = tr.find('td', {'class': 'titleColumnValue'})  # Data cell

    # Optional fields defaulted to empty
    designation = ''
    subtype = ''

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

    return title, designation, subtype


# Input: bs4 Tag <tr>
# Output: class# (str)
def class_number(tr) -> str:
    td = tr.find('td', {'class': 'classNbrColumnValue'})  # Data cell
    course_number_link = td.find('a')
    return course_number_link.text.strip()


# Input: bs4 Tag <tr>
# Output: instructor string list
def instructor(tr) -> List[str]:
    td = tr.find('td', {'class': 'instructorListColumnValue'})  # Data cell

    # Get span and list of instructor spans contained inside
    list_span = td.find('span', recursive=False)
    list_items = list_span.find_all('span', recursive=False)

    instructors = []

    # Go through all instructor spans in list
    for index, item in enumerate(list_items):
        instructor = item.text.strip()

        # Remove commas on all but last instructor, add to list
        if index < len(list_items) - 1:
            instructor = instructor[:-1]
        instructors.append(instructor)

    return instructors


# Input: bs4 Tag <tr>
# Output: days as list of strings, each slot of the list refers to what session
#   of the course the day is for.
def days(tr) -> List[str]:
    td = tr.find('td', {'class': 'dayListColumnValue'})  # Data cell

    days = []

    # For all listed items, each string goes into a list slot
    for child in td.children:
        if type(child) == NavigableString:
            days.append(str(child).strip())

    return days


# Input: bs4 Tag <tr>
# Output: start times as list of strings, each slot of the list refers to what
#   session of the course the start time is for
def start(tr) -> List[str]:
    td = tr.find('td', {'class': 'startTimeDateColumnValue'})  # Data cell

    starts = []
    comment = False  # Used in tracking comment that messes up formatting

    # For all listed items, each string goes into a list slot
    for child in td.children:

        # If comment found, raise flag
        if type(child) == Comment:
            comment = True

        # If text found after comment, add to starts
        elif type(child) == NavigableString and comment:
            starts.append(str(child).strip())

    return starts


# Input: bs4 Tag <tr>
# Output: end times as list of strings, each slot of the list refers to what
#   session of the course the end time is for
def end(tr) -> List[str]:
    td = tr.find('td', {'class': 'endTimeDateColumnValue'})  # Data cell

    ends = []

    # For all listed items, each string goes into a list slot
    for child in td.children:
        if type(child) == NavigableString:
            ends.append(str(child).strip())

    return ends


# Input: bs4 Tag <tr>
# Output: locations as list of strings, each slot of the list refers to what
#   session of the course the location is for
def location(tr) -> List[str]:
    td = tr.find('td', {'class': 'locationBuildingColumnValue'})  # Data cell

    locations = []

    for item in td.children:
        # Either spacing in page or potential location string
        if type(item) == NavigableString:
            text = str(item).strip()
            if text:
                locations.append(text)

        # Tag, either formatting <br> or location in <span> or <a>
        else:
            tag_name = item.name
            if tag_name == 'a':
                locations.append(item.text.strip())
            elif tag_name == 'span':
                # Corrects for blank spans used for cohort_message formatting
                span_text = item.text.strip()
                if span_text:
                    locations.append(span_text)

    return locations


# Input: bs4 Tag <tr>
# Output: date ranges as list of strings, each slot of the list being a
#   'session' of the class. Session code string 'A'/'B'/'C'/'DYN'
def dates(tr) -> Tuple[List[str], str]:
    td = tr.find('td', {'class': 'startDateColumnValue'})  # Data cell
    dates_link = td.find('a', {'class': 'deadlinetip'})  # Link of dates list

    dates = []

    # Take all date strings in the link and put the in the dates list
    for child in dates_link:
        if type(child) == NavigableString:
            dates.append(str(child).strip())

    # Session code is on the last string
    # ['08/22 - 12/06', '09/30 - 09/30' , '10/18 - 10/18', '11/06 - 11/06(C)']
    left_paren = dates[-1].find('(')  # 13
    session = dates[-1][left_paren + 1:-1]  # session = C
    dates[-1] = dates[-1][:left_paren]  # dates[-1] = '11/06 - 11/06'

    return dates, session


# Input: bs4 Tag <tr>
# Output: string 'X' or 'X-Y'
def units(tr):
    td = tr.find('td', {'class': 'hoursColumnValue'})  # Data cell
    return td.text.strip()


# Input: bs4 Tag <tr>
# Output: (open seats, total seats, status)
def seats_open(tr) -> Tuple[str, str, str]:
    td = tr.find('td', {'class': 'availableSeatsColumnValue'})  # Data cell

    # Get columns making up format [X][of][Y][STATUS]
    seats_row = td.find('div', {'class': 'row'}, recursive=False)
    columns = seats_row.find_all('div', {'class': 'col-xs-3'}, recursive=False)

    # Get open seats and total seats
    open_seats = columns[0].text.strip()
    total_seats = columns[2].text.strip()

    # Get classes of status icon
    icon = columns[3].find('i', {'class': 'fa'})
    icon_classes = icon.attrs['class']

    # Circle -> Open
    if 'fa-circle' in icon_classes:
        status = 'Open'

    # !Triangle -> Reserved
    elif 'fa-exclamation-triangle' in icon_classes:
        status = 'Reserved'

    # X -> None
    elif 'fa-times' in icon_classes:
        status = 'None'

    # If icon couldn't be found -> unknown status '?'
    else:
        status = '?'

    return open_seats, total_seats, status


# Given <tr>, return string of possible general studies codes
def general_studies(tr):
    td = tr.find('td', {'class': 'tooltipRqDesDescrColumnValue'})  # Data cell
    return td.text.strip()
