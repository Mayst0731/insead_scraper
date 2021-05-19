import re

import bs4
import requests

from download_parse import download_site


async def get_tsinghua_detail(page,session):
    # overview page
    desc = ''
    video_url = ''
    video_title = ''
    faculties = []
    # experience page
    takeaways_url  = 'https://www.insead.edu/master-programmes/tiemba/experience'
    page = await download_site(takeaways_url,session)
    takeaways = get_tsinghua_takeaways(page)

    # tuition
    tuition_url = 'https://www.insead.edu/master-programmes/tiemba/financing'
    page = await download_site(tuition_url,session)
    price_info = get_tsinghua_price(page)

    info = {"desc":desc,
            "video_title":video_title,
            "video_url":video_url,
            "course_takeaways":takeaways,
            'university_school':'8888_EUR',
            'priority':0,
            "publish":100,
            'languages':"English",
            "course_faculties":faculties,
            "exec_ed_inquiry_cc_emails":""}
    info.update(price_info)
    return info


def get_tsinghua_price(page):
    currency = ''
    tuition = ''
    try:
        paras = page.find_all('p')
        for para in paras:
            if "US" in para.text:
                currency = 'USD'
                tuition = re.findall('(\d+)',para.text)[1:]
                tuition = int(''.join(tuition))
                break
    except Exception as e:
        print(e)
    return {'currency':currency,
            'tuition_number':tuition}


def get_tsinghua_takeaways(page):
    takeaways = ''
    try:
        takeaways_sessions = page.find_all('p')[:7]
        for takeaways_session in takeaways_sessions:
            takeaways += takeaways_session.text
        takeaways = takeaways.strip()
    except Exception as e:
        print(e)
    return takeaways

# cate_url = 'https://www.insead.edu/master-programmes/tiemba/experience'
# source = requests.get(cate_url).content
# page = bs4.BeautifulSoup(source,'lxml')
# info = get_tsinghua_takeawasy(page)
# print(info)