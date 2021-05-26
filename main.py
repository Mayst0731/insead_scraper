from category import extract_categories
from course import *
import time
import aiohttp
import asyncio


from detail import extract_details
from faculty import  extract_all_faculty_info
from final_arragement import final_detail, modify_course_keys, delete_repeat_faculties_for_faculty_list, \
    delete_none_location
from masters import extract_masters_detail
from masters.filter_out_json_list import *
from test import change_master_program_parent_url, rewrite_cates, add_virtual_online_cates_to_courses, \
    modify_certificate_main
from write_to_json import write_to_json


async def start_crawl(base_url):
    session = aiohttp.ClientSession()

    category_list = await extract_categories(base_url, session)
    course_list = await extract_courses(category_list,session)
    detail_list = await extract_details(course_list,session)

    write_to_json(detail_list, './detail/outputfiles/comprehensive_details.json')

    faculty_list = await extract_all_faculty_info(detail_list,session)
    cleaned_faculties = delete_repeat_faculties_for_faculty_list(faculty_list)
    write_to_json(cleaned_faculties, './final_files/faculty_8888_EUR_XW_0524.json')

    url = 'https://www.insead.edu/master-programmes'
    info = await extract_masters_detail(url, url, url, cleaned_faculties, session)
    category_list += filter_out_masters_category_list(url)
    write_to_json(category_list, './final_files/category_8888_EUR_XW_0524.json')

    modified_course_list = modify_course_keys(course_list)
    modified_course_list += filter_out_masters_course_list(info)
    write_to_json(modified_course_list, './final_files/course_8888_EUR_XW_0524.json')

    comprehensive_detail = final_detail(detail_list)
    comprehensive_detail += filter_out_masters_detail_list(info)
    write_to_json(comprehensive_detail, './final_files/detail_8888_EUR_XW_0524.json')
    delete_none_location()
    change_master_program_parent_url()
    rewrite_cates()
    add_virtual_online_cates_to_courses()
    add_virtual_online_cates_to_courses()
    modify_certificate_main()
    await session.close()
    return

if __name__ == '__main__':
    start_time = time.time()
    BASE_URL = "https://www.insead.edu/executive-education/open-programmes"
    asyncio.run(start_crawl(BASE_URL))
    duration = time.time() - start_time
    minutes = duration//60
    print(f"Crawled {duration} seconds, {minutes} mins")

