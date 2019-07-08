import unittest

from bs4 import BeautifulSoup

from source.table_row import extract_row_data


def html_to_tag(html: str):
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
        html = """<tr class="grpOdd" id="informal"><td class="subjectNumberColumnValue nowrap "> <span>ENG 375 </span><!-- <br/>crseid=<span jwcid="@Insert" value="ognl:p.id.crseId"></span> <br/>crsoffrnbr=<span jwcid="@Insert" value="ognl:p.id.crseOfferNbr"></span> <br/>sessionCode=<span jwcid="@Insert" value="ognl:p.id.sessionCode"></span> <br/>associatedClass=<span jwcid="@Insert" value="ognl:p.associatedClass"></span><br/>componentPrimary=<span jwcid="@Insert" value="ognl:p.componentPrimary"></span> <br/>SsrCount=<span jwcid="@Insert" value="ognl:p.ssrCount"></span> --><!-- <div class="class-details"></div>--></td><td class="titleColumnValue"> <div class="class-results-drawer" url="/catalog/CourseDrawer.ext?sp=SENG&amp;sp=S375&amp;sp=SDTPHX&amp;sp=S2197&amp;sp=SINTRT&amp;sp=S120582&amp;sp=ZH4sIAAAAAAAAAFvzloG1uIhBJCuxLFEvN7EkQ88pM90lNTkzNzEn5Lho%2BM9GDX9mBiZPoKrkxJxUHwa2zLySsMScEgYxH5AefZAefaAez7yS1PTUIuuKIgYBsGE5iXnpen6luUmpRW1rpspyT3nQzcTAUFHAAAQYNkJ19%2FyZL7%2FS%2BrcsMwObJwNHUmaJc35pXoknAyeQ6ZOal16S4ckgnJZZVFzil59XlVqU71RZkgq0w5OBJye%2FPLW4JDi1xCkTqIGtODM9rzQ3moEzNzE9L7OkNCW1hIEp2qmikKGOgek%2FAvwDYaCLGEuLQPJrPov%2FYOMIeQBzKTOj2pWKCgCBw%2B28JQEAAA%3D%3D&amp;sp=SICOURSE"><i class="fa fa-caret-down drawer-caret" aria-hidden="true"></i><span>Topic: </span>Virgin LTD/Richard Branson </div></td><td class="classNbrColumnValue"><a role="link" class="course-details-link" href="https://webapp4.asu.edu:443/catalog/course?s=ENG&amp;n=375&amp;c=DTPHX&amp;t=2197&amp;f=INTRT&amp;r=75476&amp;=" url="https://webapp4.asu.edu:443/catalog/course?s=ENG&amp;n=375&amp;c=DTPHX&amp;t=2197&amp;f=INTRT&amp;r=75476&amp;=" id="Any_13">75476</a>&nbsp;</td><td class="instructorListColumnValue"><span><span id="For"><span><span><a id="DirectLink" title="Instructor|Charlene Heldt" class="nametip" href="/catalog/app?component=%24DirectLink&amp;page=ClassList&amp;service=direct&amp;session=T&amp;sp=S120582&amp;sp=ZH4sIAAAAAAAAAFvzloG1uIhBJCuxLFEvN7EkQ88pM90lNTkzNzEn5Lho%2BM9GDX9mBiZPoKrkxJxUHwa2zLySsMScEgYxH5AefZAefaAez7yS1PTUIuuKIgYBsGE5iXnpen6luUmpRW1rpspyT3nQzcTAUFHAAAQYNkJ19%2FyZL7%2FS%2BrcsMwObJwNHUmaJc35pXoknAyeQ6ZOal16S4ckgnJZZVFzil59XlVqU71RZkgq0w5OBJye%2FPLW4JDi1xCkTqIGtODM9rzQ3moEzNzE9L7OkNCW1hIEp2qmikKGOgek%2FAvwDYaCLGEuLQPJrPov%2FYOMIeQBzKSNLRQUANNRazCMBAAA%3D&amp;sp=S2197&amp;sp=SDYN&amp;sp=S3002&amp;sp=ZH4sIAAAAAAAAAFvzloG1uIhBJCuxLFEvN7EkQ88pM90lNTkzNzEn5Lho%2BM9GDX9mBiZPoKrkxJxUHwa2zLySsMScEgYxH5AefZAefaAez7yS1PTUIuuKIgYBsGE5iXnpen6luUmpRW1rpspyT3nQzcTAUFHAAAQYNkJ19%2FyZL7%2FS%2BrcsMwObJwNHUmaJc35pXoknAyeQ6ZOal16S4ckgnJZZVFzil59XlVqU71RZkgq0w5OBJye%2FPLW4JDi1xCkTqIGtODM9rzQ3moEzNzE9L7OkNCW1hIEp2qmikKGOgek%2FAvwDYaCLGEuLQPJrPov%2FYOMIeQBzKSNjRQUA3xaRyiMBAAA%3D&amp;sp=SCharlene&amp;sp=SHeldt" target="_blank"><span>Heldt</span></a></span></span></span></span></td><td class=" dayListColumnValue hide-column-for-online">&nbsp;</td><td class=" startTimeDateColumnValue hide-column-for-online"><!-- <span jwcid="@If" condition="ognl: p.getStartTimes().size()>1"><br/></span> -->&nbsp; </td><td class=" endTimeDateColumnValue hide-column-for-online">&nbsp;</td><td class="locationBuildingColumnValue nowrap"><span class="locationtip" title="iCourse|Online courses available to those who are enrolled as an on-campus student.">iCourse</span></td><td class="startDateColumnValue nowrap"><!-- <span jwcid="@If" condition="ognl:p.multipleMtgDates"><br/></span> --><span><a title="Deadlines: ENG 375 75476 (Dynamic Dated)" style="cursor: help;" class="deadlinetip" rel="/catalog/deadlinePage.ext?sp=S75476&amp;sp=S2197" href="#">08/22 - 09/26(DYN)</a>&nbsp;</span></td><td class="hoursColumnValue">1</td><td class="availableSeatsColumnValue"><div class="row"><div class="col-xs-3">28</div><div class="col-xs-3">of</div><div class="col-xs-3">30</div><div class="col-xs-3"><!-- p.countRows<span jwcid="@Insert" value="ognl:p.countRows"></span><br/>p.availableSeats<span jwcid="@Insert" value="ognl:p.availableSeats"></span><br/>p.hasActiveReservedSeats<span jwcid="@Insert" value="ognl:p.hasActiveReservedSeats"></span><br/> --><span raw="true"><span title="ENG 375 75476 (DYN)" style="cursor: help;" value="" class="rsrvtip" rel="/catalog/ReservedCapacity.ext?sp=S120582&amp;sp=S4&amp;sp=S2197&amp;sp=S3002&amp;sp=SUGRD&amp;sp=SDYN&amp;sp=S75476&amp;sp=S28&amp;sp=SE" id="Any_17"><i class="fa fa-exclamation-triangle green" aria-hidden="true" title="seats reserved"></i></span></span></div></div></td><td class="linksColumnValue"><!-- <span jwcid="@If" condition='ognl:p.showBooks' ><a jwcid="@Any" title="Book List" rel="ognl:getUrl()" class="booktip" style="cursor: pointer;">Book&nbsp;List</a><br/></span> --><span><a target="_blank" role="link" title="Syllabus" href="https://webapp4.asu.edu/bookstore/viewsyllabus/2197/75476" id="Any_18">Syllabus</a><br></span></td><td class="tooltipRqDesDescrColumnValue">&nbsp;&nbsp;</td><td style="padding-top:1px;" class="applyColumnValue"><span><div rendertag="true"><span><span><span><span><a role="link" class="btn btn-add-class" rendertag="true" href="https://weblogin.asu.edu/cgi-bin/login?callapp=https%3A%2F%2Fwebapp4.asu.edu%2Fcatalog%2FAddRedirect.ext%3Fsp%3DS2197%26sp%3DS75476%26init%3Dfalse" id="Any_21">Add</a></span></span></span></span></div></span></td></tr>"""
        tr = html_to_tag(html)
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
        print(actual)
        print(expected)
        self.maxDiff = None
        self.assertDictEqual(actual, expected)

    def test_002(self):
        html = """<tr class="grpOdd" id="informal"><td class="subjectNumberColumnValue nowrap "> <span>PHY 131 </span><!-- <br/>crseid=<span jwcid="@Insert" value="ognl:p.id.crseId"></span> <br/>crsoffrnbr=<span jwcid="@Insert" value="ognl:p.id.crseOfferNbr"></span> <br/>sessionCode=<span jwcid="@Insert" value="ognl:p.id.sessionCode"></span> <br/>associatedClass=<span jwcid="@Insert" value="ognl:p.associatedClass"></span><br/>componentPrimary=<span jwcid="@Insert" value="ognl:p.componentPrimary"></span> <br/>SsrCount=<span jwcid="@Insert" value="ognl:p.ssrCount"></span> --><!-- <div class="class-details"></div>--></td><td class="titleColumnValue"> <div class="class-results-drawer" url="/catalog/CourseDrawer.ext?sp=SPHY&amp;sp=S131&amp;sp=STEMPE&amp;sp=S2197&amp;sp=SINTRT&amp;sp=S101818&amp;sp=ZH4sIAAAAAAAAAFvzloG1uIhBJCuxLFEvN7EkQ88pM90lNTkzNzEn5Lho%2BM9GDX9mBiZPoKrkxJxUHwa2zLySsMScEgYxH5AefZAefaAez7yS1PTUIuuKIgYBsGE5iXnpen6luUmpRW1rpspyT3nQzcTAUFHAAAQYNkJ19%2FyZL7%2FS%2BrcsMwObJwNHUmaJc35pXoknAyeQ6ZOal16S4ckgnJZZVFzil59XlVqU71RZkgq0w5OBJye%2FPLW4JDi1xCkTqIGtODM9rzQ3moEzNzE9L7OkNCW1hIEp2qmikKGOgek%2FAvwDYaCLGEuLQPJrPov%2FYOMIeQBzKTOjtFxFBQBr8JQiJQEAAA%3D%3D&amp;sp=STEMPE"><i class="fa fa-caret-down drawer-caret" aria-hidden="true"></i>Univ Physics II: Elctrc/Magnet </div></td><td class="classNbrColumnValue"><a role="link" class="course-details-link" href="https://webapp4.asu.edu:443/catalog/course?s=PHY&amp;n=131&amp;c=TEMPE&amp;t=2197&amp;f=INTRT&amp;r=72478&amp;=" url="https://webapp4.asu.edu:443/catalog/course?s=PHY&amp;n=131&amp;c=TEMPE&amp;t=2197&amp;f=INTRT&amp;r=72478&amp;=" id="Any_13">72478</a>&nbsp;</td><td class="instructorListColumnValue"><span><span id="For"><span><span><a id="DirectLink" title="Instructor|Martha McCartney" class="nametip" href="/catalog/app?component=%24DirectLink&amp;page=ClassList&amp;service=direct&amp;session=T&amp;sp=S101818&amp;sp=ZH4sIAAAAAAAAAFvzloG1uIhBJCuxLFEvN7EkQ88pM90lNTkzNzEn5Lho%2BM9GDX9mBiZPoKrkxJxUHwa2zLySsMScEgYxH5AefZAefaAez7yS1PTUIuuKIgYBsGE5iXnpen6luUmpRW1rpspyT3nQzcTAUFHAAAQYNkJ19%2FyZL7%2FS%2BrcsMwObJwNHUmaJc35pXoknAyeQ6ZOal16S4ckgnJZZVFzil59XlVqU71RZkgq0w5OBJye%2FPLW4JDi1xCkTqIGtODM9rzQ3moEzNzE9L7OkNCW1hIEp2qmikKGOgek%2FAvwDYaCLGEuLQPJrPov%2FYOMIeQBzKSNjRQUA3xaRyiMBAAA%3D&amp;sp=S2197&amp;sp=SC&amp;sp=S1071&amp;sp=ZH4sIAAAAAAAAAFvzloG1uIhBJCuxLFEvN7EkQ88pM90lNTkzNzEn5Lho%2BM9GDX9mBiZPoKrkxJxUHwa2zLySsMScEgYxH5AefZAefaAez7yS1PTUIuuKIgYBsGE5iXnpen6luUmpRW1rpspyT3nQzcTAUFHAAAQYNkJ19%2FyZL7%2FS%2BrcsMwObJwNHUmaJc35pXoknAyeQ6ZOal16S4ckgnJZZVFzil59XlVqU71RZkgq0w5OBJye%2FPLW4JDi1xCkTqIGtODM9rzQ3moEzNzE9L7OkNCW1hIEp2qmikKGOgek%2FAvwDYaCLGEuLQPJrPov%2FYOMIeQBzKSNjRQUA3xaRyiMBAAA%3D&amp;sp=SMartha&amp;sp=SMcCartney" target="_blank"><span>McCartney</span></a></span></span></span></span></td><td class=" dayListColumnValue hide-column-for-online"> <br>M<br>F<br>W&nbsp;</td><td class=" startTimeDateColumnValue hide-column-for-online"><!-- <span jwcid="@If" condition="ognl: p.getStartTimes().size()>1"><br/></span> -->12:00 AM<br>&nbsp;<br>&nbsp;<br>&nbsp;&nbsp; </td><td class=" endTimeDateColumnValue hide-column-for-online">12:00 AM<br>&nbsp;<br>&nbsp;<br>&nbsp;&nbsp;</td><td class="locationBuildingColumnValue nowrap"><span class="locationtip" title="Hybrid classes|Hybrid classes have one or more in person meetings">Internet - Hybrid</span><br>Tempe - TBA<br>Tempe - TBA<br>Tempe - TBA</td><td class="startDateColumnValue nowrap"><!-- <span jwcid="@If" condition="ognl:p.multipleMtgDates"><br/></span> --><span><a title="Deadlines: PHY 131 72478 (Session C)" style="cursor: help;" class="deadlinetip" rel="/catalog/deadlinePage.ext?sp=S72478&amp;sp=S2197" href="#">08/22 - 12/06<br>09/30 - 09/30<br>10/18 - 10/18<br>11/06 - 11/06(C)</a>&nbsp;</span></td><td class="hoursColumnValue">3</td><td class="availableSeatsColumnValue"><div class="row"><div class="col-xs-3">46</div><div class="col-xs-3">of</div><div class="col-xs-3">150</div><div class="col-xs-3"><!-- p.countRows<span jwcid="@Insert" value="ognl:p.countRows"></span><br/>p.availableSeats<span jwcid="@Insert" value="ognl:p.availableSeats"></span><br/>p.hasActiveReservedSeats<span jwcid="@Insert" value="ognl:p.hasActiveReservedSeats"></span><br/> --><span raw="true"><span title="PHY 131 72478 (C)" style="cursor: help;" value="" class="rsrvtip" rel="/catalog/ReservedCapacity.ext?sp=S101818&amp;sp=S1&amp;sp=S2197&amp;sp=S1071&amp;sp=SUGRD&amp;sp=SC&amp;sp=S72478&amp;sp=S46&amp;sp=SE" id="Any_17"><i class="fa fa-exclamation-triangle green" aria-hidden="true" title="seats reserved"></i></span></span></div></div></td><td class="linksColumnValue"><!-- <span jwcid="@If" condition='ognl:p.showBooks' ><a jwcid="@Any" title="Book List" rel="ognl:getUrl()" class="booktip" style="cursor: pointer;">Book&nbsp;List</a><br/></span> --></td><td class="tooltipRqDesDescrColumnValue"><span class="gstip" href="General Studies|Natural Science - Quantitative">SQ</span>&nbsp;&nbsp;</td><td style="padding-top:1px;" class="applyColumnValue"><span><div rendertag="true"><span><span><span><span><a role="link" class="btn btn-add-class" rendertag="true" href="https://weblogin.asu.edu/cgi-bin/login?callapp=https%3A%2F%2Fwebapp4.asu.edu%2Fcatalog%2FAddRedirect.ext%3Fsp%3DS2197%26sp%3DS72478%26init%3Dfalse" id="Any_21">Add</a></span></span></span></span></div></span></td></tr>"""
        tr = html_to_tag(html)
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
        print(actual)
        print(expected)
        self.maxDiff = None
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
