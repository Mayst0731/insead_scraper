from detail.faculty_rules import extract_faculty_info
from detail.overview_rules import extract_overview_info
from detail.sub_urls import add_related_urls_info_course_info
from detail.testimonial_rules import extract_testimonial_info
from detail.version_rules import extract_version_info
from download_parse import download_site
import urllib
import pprint


async def extract_details(course_list,session):
    detail_list = []
    count = 0
    for course in course_list:
        print(f'{count}. {course["course"]} is processing...')
        detail = {}
        overview_page = await download_site(course['url'],session)
        get_sub_links = add_related_urls_info_course_info(course,overview_page)
        course_overview_info = extract_overview_info(course,overview_page)
        course_faculty_info = await extract_faculty_info(course,session)
        course_testimonial_info = await extract_testimonial_info(course,session)
        course_version_info = await extract_version_info(course,session)
        detail_list.append(course)
        count += 1
    return detail_list









