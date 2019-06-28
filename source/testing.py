from asu_course_search import ASUCourseSearch

asu = ASUCourseSearch()  # Start session

controls = asu.checker()  # Get all valid control item names

# Print all valid inputs for each control item
for control in controls:
    options = asu.control_checker(control)
    print(control, ":", options)

asu.quit()  # Quit session