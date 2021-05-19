import re
from pprint import pprint

import bs4
import requests

from download_parse import download_site


async def get_mba_course_detail(cate_info,page,previous_faculties,session):
    video_url = ''
    video_title = ''
    takeaways = ''
    currency = ''
    tuition = ''
    try:
        video_link = page.find('a',attrs={"class":"ytp-title-link yt-uix-sessionlink"})
        video_title = video_link.text
        video_url = video_link.get('href')
    except:
        pass

    try:
        takeaways_sessions = page.find('div',attrs={"class":"equal-box equal-responsive"}).find_all('p')
        for takeaways_session in takeaways_sessions:
            takeaways += takeaways_session.text
        takeaways = takeaways.strip()
    except:
        pass

    try:
        tuition_sessions = page.find_all('div')
        for tuition_session in tuition_sessions:
            if '$' in tuition_session.text and ',' in tuition_session.text:
                tuition_info = tuition_session.text
                currency = 'USD'
                tuition =''.join(re.findall('(\d+)',tuition_info))
                tuition = int(tuition)
    except:
        pass
    fac_url = cate_info['url'] + '/faculty-profiles'
    fac_page = await download_site(fac_url, session)
    faculties = get_mba_faculties(previous_faculties, fac_page)
    return {"video_url":video_url,
            "video_title":video_title,
            "testimonials":[],
            "languages":"English",
            "university_school": "8888_EUR",
            "credential": "MBA",
            "duration_consecutive": "Yes",
            "priority": 0,
            "publish": 100,
            "is_advanced": True,
            "Repeatable": "Y",
            "course_takeaways":takeaways,
            "currency":currency,
            "tuition_number":tuition,
            "tuition_note":'',
            'exec_ed_inquiry_cc_emails':'',
            'course_faculties':faculties,
            'university_school':'8888_EUR'}


def get_mba_faculties(previous_fauculties,page):
    previous_fauculties_name = []
    needed_faculties = []
    for fac in previous_fauculties:
        previous_fauculties_name.append(fac["name"])
    fac_sessions = page.find_all('div',attrs={"align":"center"})
    for fac in fac_sessions:
        name = ''
        try:
            name = fac.h4.text.strip()
        except:
            pass
        if name and name in previous_fauculties_name:
            needed_faculties.append(name)
    return needed_faculties



# url = 'https://www.insead.edu/master-programmes/mba'
# source = requests.get(url).content
# page = bs4.BeautifulSoup(source,'lxml')
# info = get_mba_course_detail(page)
# # pprint(info)
