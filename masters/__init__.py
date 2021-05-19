from pprint import pprint

import bs4
import requests

from detail.format_strings import get_duration_type, get_duration_num
from download_parse import download_site
from masters.mba import get_mba_course_detail
from masters.mim import get_mim_course_detail
from masters.tsinghua_sem import get_tsinghua_detail


async def extract_masters_detail(url,cate_url,parent_url,previous_faculties,session):
    page = await download_site(url,session)
    masters_details = []
    course_sessions = page.find_all('div',attrs={"class":"col-md-6 col-sm-6 col-xs-12 columns mbot5 tealium-programme-cta programme-250-box"})
    for course_session in course_sessions:
        cate_detail = extract_one_master_cate_detail(course_session,cate_url,parent_url)
        course_url = cate_detail['url']
        page = await download_site(course_url,session)
        if 'Tsinghua' in cate_detail['name']:
            other_info = await get_tsinghua_detail(page,session)
        elif 'Master in Management' in cate_detail['name']:
            other_info = get_mim_course_detail(page)
        else:
            other_info = await get_mba_course_detail(cate_detail,page,previous_faculties,session)
        info = {**cate_detail,**other_info}
        overview = {'desc':info['desc'],
                    'video_url':info['video_url'],
                    'video_title':info['video_title']}
        info['overview'] = overview
        info["type"] = course_type(info["type"])
        del info['video_url']
        del info['video_title']
        if 'is_advanced' in info:
            del info["is_advanced"]
        masters_details.append(info)
    return masters_details

def course_type(type):
    type_dict = {"Modular / Part-time":"Onsite",
                 "Full-time":"Onsite"}
    return type_dict.get(type)

def extract_one_master_cate_detail(course_session,cate_url,parent_url):
    name = ''
    url = ''
    type = ''
    duration_info = ''
    location = ''
    desc = ''
    who_attend_params = {
        "working experience": "",
        "background knowledge": ""}
    try:
        name = course_session.find('h3').a.text
    except:
        pass
    try:
        url = course_session.find('h3').a.get('href')
    except:
        pass
    try:
        type = course_session.find('ul').find_all('li')[0].text
    except:
        pass
    try:
        location = course_session.find('ul').find_all('li')[3].text
    except:
        pass
    try:
        duration_info = course_session.find('ul').find_all('li')[2].text
    except:
        pass
    try:
        desc = course_session.find('div',attrs={"class":"s_texte"}).p.text
    except:
        pass
    try:
        lis = course_session.find('ul').find_all('li')
        for li in lis:
            if 'Work Experience' in li.text:
                experience = li.text
                if '\xa0' in experience:
                    experience = experience.replace('\xa0',' ')
                who_attend_params['working experience'] = experience
    except:
        pass
    if duration_info:
        duration_type = get_duration_type(duration_info)
        duration_type = 'duration_'+duration_type
        duration_num = get_duration_num(duration_info)
    schedule = [[
        "",
        "",
        f"{duration_num}",
        "normal"]]
    if 'Executive MBA' in name:
        credential = 'EMBA'
    elif 'MBA' in name:
        credential = 'MBA'
    else:
        credential = 'Masters'
    location = deal_with_locations(location)
    info = {"name":name,
            "url":url,
            "category":["Master Programmes"],
            "category_url":[cate_url],
            "parent_url":parent_url,
            "location":location,
            "type":type,
            "desc":desc,
            "who_attend_params":who_attend_params,
            duration_type:duration_num,
            "version":1,
            "credential":credential,
            "category_tags": "",
            "is_advanced_management_program": False,
            "tuition_note":"",
            "Repeatable":"Y",
            "effective_date_start":'',
            "effective_date_end":"",
            "duration_desc":"",
            "duration_consecutive":True,
            "who_attend_desc":'',
            "exec_ed_inquiry_cc_emails":"",
            "active":True,
            "audience_title_level": "",
            "schedule":schedule}
    return info


def deal_with_locations(location):
    location_list = []
    location_dict = {"Fontainebleau": "Fontainebleau, ----, France",
                     "Singapore": "Singapore, ----, Singapore",
                     "San Francisco": "San Francisco, CA, United States",
                     "Beijing": "Beijing, ----, China",
                     "France":"Fontainebleau, ----, France",
                     "Abu Dhabi":"Abu Dhabi, ----, United Arab Emirates",
                     "China":"Beijing, ----, China",
                     "USA":"San Francisco, CA, United States"}
    for loc in location_dict.keys():
        if loc in location:
            location_list.append(location_dict[loc])
    return location_list



# parent_url = 'https://www.insead.edu/'
# cate_url = 'https://www.insead.edu/master-programmes'
#
# source = requests.get(cate_url).content
# page = bs4.BeautifulSoup(source,'lxml')
# details = extract_masters_detail(page,cate_url,parent_url)
# pprint(details)