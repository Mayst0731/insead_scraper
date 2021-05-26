from download_parse import download_site
import urllib
import pprint

# coroutines = []
#     for detail in partial_detail:
#         coroutines.append(course_page_detail(detail, session))
#     final_details = await asyncio.gather(*coroutines)


async def extract_courses(category_list,session):
    print('hello course')
    course_list = []

    for category in category_list:
       category_page = await download_site(category['url'], session)
       one_page_courses = extract_one_page_courses(category_page)
       for course in one_page_courses:
           course_info = package_course(category,course)
           course_list.append(course_info)
    cleaned_courses = combine_categories_for_course(course_list)
    pprint.pprint(cleaned_courses)
    print(len(cleaned_courses))
    return cleaned_courses


def extract_one_page_courses(category_page):
    courses = []
    course_divs = category_page.find_all('div',attrs={"class":"body body-programme body-programme-icon"})
    for course_div in course_divs:
        course_name = course_div.find('h3').a.text
        course_relative_link = course_div.find('h3').a.get('href')
        course_link = urllib.parse.urljoin('https://www.insead.edu/executive-education/', course_relative_link)
        course = {'course':course_name,
                  'url':course_link}
        courses.append(course)
    return courses


# package all the course information
def package_course(category,course):
    course_info = {}
    course_info['course'] = course['course']
    course_info['url'] = course['url']
    course_info['category'] = [category['category']]
    course_info['category_url'] = [category['url']]
    return course_info


def combine_categories_for_course(course_list):
    processing_course_mapping = dict()
    for course in course_list:
        course_url = course.get('url')
        if course_url not in processing_course_mapping:
            processing_course_mapping[course_url] = course
        else:
            processing_course_mapping[course_url]['category'] += course['category']
            processing_course_mapping[course_url]['category_url'] += course['category_url']

    after_processing_course_info = []
    for course_info in processing_course_mapping.values():
        after_processing_course_info.append(course_info)
    return after_processing_course_info