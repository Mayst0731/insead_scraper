from pprint import pprint

from download_parse import download_site
from detail.format_strings import *
import requests
import bs4
import aiohttp
import asyncio


async def extract_version_info(course_info, session):
    try:
        version_url = course_info['version_url']
        version_page = await download_site(version_url, session)
        course_info['version_detail'] = get_versions(version_page)
    except Exception as e:
        print(f'{course_info["url"]}\'s version has problem: {e}, version url {version_url}')
        course_info['version_detail'] = no_info_course_version_detail()
    return course_info


def no_info_course_version_detail():
    detail  = { 'effective_date_start': '',
            'effective_date_end': '',
            'duration_weeks': 0,
            'location': [],
            'currency': 'EUR',
            'tuition': 0,
            'tuition_note': '',
            'type': 'Onsite',
            'active': False,
            'version': 1}
    return [detail]


def get_versions(version_page_obj):
    all_versions = version_page_obj.find_all('div', attrs={'class': 'table-row'})
    single_location_set = set()
    multi_locations_set = list()
    all_version_info = []
    for each_version in all_versions:
        if is_first_module(each_version):
            continue
        body_info = each_version.tbody
        if is_single_module(body_info):
            location_str = single_module_location(body_info)
            if location_str in single_location_set:
                continue
            else:
                single_location_set.add(location_str)
                version_info = single_module_info(body_info)
                all_version_info.append(version_info)
        else:
            multi_locs = multi_module_location(body_info)
            if multi_locs in multi_locations_set:
                continue
            else:
                multi_locations_set.append(multi_locs)
                version_info = multi_module_info(body_info)
                all_version_info.append(version_info)
    real_versions = len(all_version_info)
    for info in all_version_info:
        info['version'] = real_versions
    return all_version_info


def is_first_module(each_version):
    title_text = each_version.find('div', attrs={"class": "table-row-header"}).a.text
    if '(1)' in title_text:
        return True
    return False


def is_single_module(body_info):
    modules = body_info.find_all('tr')
    if len(modules) == 1:
        return True
    else:
        return False


def single_module_info(body_info):
    date_obj = body_info.td
    length_obj = date_obj.nextSibling
    location_obj = length_obj.nextSibling
    tuition_fees_obj = location_obj.nextSibling
    date = date_obj.text
    length = length_obj.text
    location = location_obj.text.strip()
    tuition_fees = tuition_fees_obj.text
    currency = get_currency(tuition_fees)
    tuition = get_tuition(tuition_fees)
    effective_start_date = get_start_date(date)
    effective_end_date = get_end_date(date)
    duration_type = get_duration_type(length)
    duration_num = get_duration_num(length)
    duration_key = 'duration_' + duration_type
    type = ''
    type = get_single_module_course_type(location)
    if tuition_fees == 0:
        active = False
    else:
        active = True
    info = {'effective_date_start': effective_start_date,
            'effective_date_end': effective_end_date,
            duration_key: duration_num,
            'location': [location.strip()],
            'currency': currency,
            'tuition': tuition,
            'tuition_note': '',
            'type': type,
            'active': active}
    return info


def multi_module_info(body_info):
    start_and_end_date = multi_module_start_end_date(body_info)
    effective_start_date = start_and_end_date.get('effective_start_date','')
    effective_end_date = start_and_end_date.get('effective_end_date', '')
    # this one should be add in {**duration_info}, cuz cannot know the key
    duration_info = multi_module_duration(body_info)
    locations = multi_module_location(body_info)
    type = get_multi_module_course_type(locations)
    partial_version_info = {"active": True,
                            "effective_date_start": effective_start_date,
                            "effective_date_end": effective_end_date,
                            "location": locations,
                            "type": type}
    tuition_info = multi_module_price(body_info)
    version_info = {** partial_version_info, **duration_info,**tuition_info}
    if 'tuition_note' not in version_info:
        version_info['tuition_note'] = ''
    return version_info


def multi_module_start_end_date(body_info):
    modules = body_info.find_all('tr')
    start_date_with_module = modules[0].find('td')
    end_date_with_module = modules[-1].find('td')
    start_date_with_module.strong.extract()
    end_date_with_module.strong.extract()
    start_date = start_date_with_module.text
    end_date = end_date_with_module.text
    effective_start_date = get_start_date(start_date)
    effective_end_date = get_end_date(end_date)
    return {'effective_date_start':effective_start_date,
            'effective_date_end':effective_end_date}


def multi_module_duration(body_info):
    modules = body_info.find_all('tr')
    duration_num = 0
    duration_type = ''
    for module in modules:
        duration = module.find_all('td')[1].text
        duration_num += get_duration_num(duration)
        duration_type = get_duration_type(duration)
    duration_key = 'duration_' + duration_type
    return {
        duration_key:duration_num
    }


def multi_module_location(body_info):
    locations = set()
    modules = body_info.find_all('tr')
    for module in modules:
        location = module.find_all('td')[2].text.strip()
        locations.add(location)
    return list(locations)


def multi_module_price(body_info):
    tuition_fees = body_info.find('tr').find_all('td')[3].text
    currency = get_currency(tuition_fees)
    tuition = get_tuition(tuition_fees)
    return {'currency': currency,
            'tuition': tuition,
            'tuition_note': ''}


def single_module_location(body_info):
    location = body_info.find_all('td')[2].text.strip()
    return location


# test_urls = [
#     "https://www.insead.edu/executive-education/general-management/advanced-management-programme-dates-fees",
#     "https://www.insead.edu/executive-education/general-management/transition-general-management-dates-fees",
#     "https://www.insead.edu/executive-education/leadership/leading-change-age-digital-transformation-dates-fees",
#     "https://www.insead.edu/executive-education/leadership/strategic-decision-making-leaders-dates-fees",
#     "https://www.insead.edu/executive-education/leadership/leading-across-borders-cultures-dates-fees",
#     "https://www.insead.edu/executive-education/leadership/coaching-certificate-dates-fees",
#     "https://www.insead.edu/executive-education/leadership/integrating-performance-progress-dates-fees",
#     "https://www.insead.edu/executive-education/open-online-programmes/driving-digital-marketing-strategy-dates-fees",
#     "https://www.insead.edu/executive-education/marketing-sales/b2b-marketing-strategies-date-fees",
#     "https://www.insead.edu/executive-education/entrepreneurship-family-business/entrepreneurship-new-business-ventures/date-fees",
#     "https://www.insead.edu/executive-education/general-management/management-acceleration-programme-dates-fees",
#     "https://www.insead.edu/executive-education/general-management/leading-business-transformation-asia-dates-fees"
# ]
#
#
# async def worker(url, session):
#     dic = dict()
#     source = await session.request(method='GET', url=url)
#     page = await source.text()
#     version_page = bs4.BeautifulSoup(page, 'lxml')
#     version_info = get_versions(version_page)
#     if len(version_info) == 0:
#         version_info = no_info_course_version_detail()
#     dic[url] = version_info
#     return dic
#
#
# async def test(urls):
#     async with aiohttp.ClientSession() as session:
#         versions = await asyncio.gather(*(worker(url, session) for url in urls))
#         pprint(versions)
#         print(f'total {len(versions)} courses')
#
# asyncio.run(test(test_urls))
