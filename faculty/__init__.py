import asyncio
import json
from datetime import time
from pprint import pprint

from bs4 import BeautifulSoup

from download_parse import download_site


async def extract_all_faculty_info(detail_list,session):
    """
    :param detail_list:
    :param session:
    :return: faculty list with name,title,pdf_url,pic_url,intro_desc,university_school
    """
    faculties = []
    for detail in detail_list:
        ''' find faculty value list'''
        faculty_list = detail.get('faculty')
        for faculty in faculty_list:
            '''each faculty contains sub_url for desc and pdf_url, and extracted name,title and pic_url'''
            integrated_faculty = await integrate_faculty_attrs(faculty,session)
            faculties.append(integrated_faculty)
    for fac in faculties:
        del fac["faculty_sub_url"]
    return faculties


async def integrate_faculty_attrs(faculty,session):
    print(f'{faculty["name"]} is processing..., url is {faculty["faculty_sub_url"]}')
    if faculty['faculty_sub_url']:
        page = await download_site(str(faculty['faculty_sub_url']),session)
    faculty_personal_website = ''
    faculty_desc = ''
    try:
        faculty_personal_website = page.find('a',text="Personal Website").get('href')
        faculty_desc = page.find('div',attrs={"id":"faculty-biography"}).find('p').text
    except:
        pass
    finally:
        other_faculty_info = {'intro_desc':faculty_desc,
                              'pdf_url':faculty_personal_website,
                              'university_school': '8888_EUR'}
    faculty.update(other_faculty_info)
    return faculty

