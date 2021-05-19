import re

from download_parse import download_site
import urllib
from urllib import parse


async def extract_faculty_info(course_info,session):
    try:
        faculty_url = course_info['faculty_url']
        faculty_page = await download_site(faculty_url,session)
        get_faculty_info(course_info,faculty_page)
    except Exception as e:
        course_info['faculty'] = []
        print(e)
    return course_info


def get_pic_url(container_obj):
    pic_url = ''
    try:
        pic_obj = container_obj.find('img')
        if pic_obj:
            pic_url = pic_obj.get('src')
            pic_url = parse.urljoin('https://www.insead.edu/', pic_url)
    except:
        pass
    return pic_url


def get_faculty_sub_url(container_obj):
    faculty_sub_url = ''
    try:
        sub_url_link = container_obj.find('a').get('href')
        faculty_sub_url = urllib.parse.urljoin('https://www.insead.edu/executive-education/', sub_url_link)
    except:
        pass
    return faculty_sub_url


def get_faculty_name_title(container_obj):
    name = ''
    title = ''
    try:
        name_title_obj = container_obj.find('div', attrs={'class': 'col-md-10 col-sm-9 col-xs-12 freehtml'})
        if name_title_obj:
            name = name_title_obj.find('h3').text.strip()
        if name_title_obj and name_title_obj.find('p') and name_title_obj.find('p').strong:
            title = name_title_obj.find('p').strong.text.strip()
            title = title
        elif name_title_obj and name_title_obj.find('h5'):
            title = name_title_obj.find('h5').text.strip()
            title = title
        if '(' in name:
            name = name.replace('(',' ').replace(')',' ')
        name = re.sub("\s+", " ", name)
    except:
        pass
    return {'name':name,'title':title}


def get_faculty_info(course_info,page_obj):
    faculty_list = []
    faculty_section = page_obj.find_all('div', attrs={'stripe-gray'})
    faculty_section += page_obj.find_all('div',attrs={'stripe-white'})
    # find all the containers
    container_objs = []
    for faculty_session in faculty_section:
        container_objs += faculty_session.find_all('div', attrs={'class': 'container'})

    for container_obj in container_objs:
        each_faculty = {'name':'',
                        'title':'',
                        'pic_url':''}
        # get name and title
        each_faculty['name'] = get_faculty_name_title(container_obj)['name'].strip()
        each_faculty['title'] = get_faculty_name_title(container_obj)['title'].strip()
        each_faculty['pic_url'] = get_pic_url(container_obj)
        each_faculty['faculty_sub_url'] = get_faculty_sub_url(container_obj)
        if len(each_faculty['name']) != 0:
            faculty_list.append(each_faculty)
    course_info['faculty'] = faculty_list
    return faculty_list

