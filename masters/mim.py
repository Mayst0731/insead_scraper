from pprint import pprint
from urllib import parse

import bs4
import requests

from download_parse import download_site


def get_mim_course_detail(page):
    video_url = ''
    video_title = ''
    takeaways = ''
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

    return {"video_url":video_url,
            "video_title":video_title,
            "languages":"English",
            "university_school": "8888_EUR",
            "credential": "Masters",
            "duration_consecutive": "Yes",
            "priority": 0,
            "publish": 100,
            "is_advanced": True,
            "Repeatable": "Y",
            "course_takeaways":takeaways,
            "currency":'',
            "tuition_number":0,
            "tuition_note":'',
            'exec_ed_inquiry_cc_emails':'',
            'course_faculties':[],
            'testimonials':[],
            'university_school':'8888_EUR'}





# url = 'https://www.insead.edu/master-programmes/mim'
# source = requests.get(url).content
# page = bs4.BeautifulSoup(source,'lxml')
# info = get_mim_course_detail(page)
# pprint(info)