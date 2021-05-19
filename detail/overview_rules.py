import bs4
import requests
from langdetect import detect


def extract_overview_info(course_info,overview_page):
    # (1) course_takeaways
    course_takeaways = get_course_takeaways(course_info,overview_page)

    # (2) course video_url
    course_video_url = get_video_url(overview_page)

    # (3) course description: course_detail['desc']
    overview = get_description(overview_page)

    # (4) get who_attend_desc course_detail['who_attend_desc'] = ''
    course_who_attend = get_who_attend(overview_page)

    # (5) get language
    course_language = get_language(course_info)

    # (6) contact

    exec_ed_inquiry_cc_email = get_contact_info(course_info)
    new_attrs = {
        'course_takeaways': course_takeaways,
        'video_title':"",
        'video_url': course_video_url,
        'overview': overview,
        'who_attend_desc': course_who_attend,
        'university_school': '8888_EUR',
        'priority': 'non-sponsor',
        'publish': 'public',
        'is_advanced': True,
        'repeatable': 'Yes',
        "who_attend_params": '{\"working experience\":\"\",\"background knowledge\":\"\"}',
        'languages': course_language,
        "exec_ed_inquiry_cc_email":exec_ed_inquiry_cc_email
    }
    course_info.update(new_attrs)


def France_coursetake_aways():
    takeaways = "*Développer votre aptitude à penser stratégiquement et à " \
                 "établir une vision d’ensemble, de façon à harmoniser les ressources " \
                 "et les capacités d’une organisation en fonction de son environnement extérieur changeant" + "*Apprendre une démarche axée sur la valeur pour naviguer dans les décisions commerciales et assurer un avantage concurrentiel durable"+"*Comprendre l’impact des choix du management sur la position fnancière de l’entreprise afn d’élaborer un plan d’exécution stratégique qui garantisse une meilleure performance fnancière."
    return takeaways


def get_course_takeaways(course_info,overview_page):
    course_takeaways = ""
    try:
        h4_obj = overview_page.find('h4', text="How you benefit")

        if h4_obj:
            ul_obj = h4_obj.findNext('ul')
            if ul_obj:
                li_objs = ul_obj.find_all('li')
                for li_obj in li_objs:
                    course_takeaways += "*" + li_obj.text + "\n"
        if course_info['url'] == "https://www.insead.edu/executive-education/open-online-programmes/strategie-affaires" \
                                 "-performance-financiere":
            course_takeaways = France_coursetake_aways()
    except:
        pass
    return course_takeaways


def get_video_url(overview_page):
    video_url = ''
    try:
        banner_obj = overview_page.find('div', attrs={'class': 'hero-banner no-margin'})
        # set the video url suffix to be a blank string first
        video_url_suffix = ''

        if banner_obj.a:
            video_url_suffix = banner_obj.a['href']

        if len(video_url_suffix) == 0:
            video_url = ''
        else:
            video_url = 'https://www.insead.edu' + video_url_suffix
    except Exception:
        pass
    return video_url


def get_description(overview_page):
    desc = ''
    try:
        right_obj = overview_page.find('div', attrs={'class': "col-md-9 col-sm-7 col-xs-12 freehtml"})
        desc_title_obj = right_obj.find('h3')
        if desc_title_obj:
            desc_obj = desc_title_obj.nextSibling
            while desc_obj.name == 'p':
                desc += desc_obj.text
                desc_obj = desc_obj.nextSibling
    except Exception as e:
        pass
    return desc


def get_who_attend(overview_page):
    who_attend_desc = ''
    attend_title_obj = overview_page.find('h4', text='Participant profile')
    if attend_title_obj:
        attend_desc_obj = attend_title_obj.find_next("p")
        while attend_desc_obj:
            who_attend_desc += attend_desc_obj.text
            attend_desc_obj = attend_desc_obj.find_next("p")
    if overview_page.find('h4', text='Participant profile') and overview_page.find('h4', text='Participant '
                                                                                              'profile').find_next(
        'ul'):
        who_attend_desc += overview_page.find('h4', text='Participant profile').find_next('ul').text
    return who_attend_desc


def get_language(course_info):
    lang = detect(course_info['course'])
    return lang


def get_contact_info(course_info):
    exec_ed_inquiry_cc_email = ''
    try:
        exec_ed_inquiry_cc_email = course_info.find('a',text="Send an email").get('href')
    except:
        pass
    return exec_ed_inquiry_cc_email


















