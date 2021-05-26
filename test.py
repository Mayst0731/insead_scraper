from pprint import pprint
import urllib
import bs4

from download_parse import download_site
from write_to_json import read_from_json, write_to_json
import requests


def change_master_program_parent_url():
    cates = read_from_json('./final_files/category_8888_EUR_XW_0524.json')
    for cate in cates:
        if cate["category"] == "Master Programmes":
            cate["parent_url"] = "https://www.insead.edu/"
    write_to_json(cates, './final_files/category_8888_EUR_XW_0524.json')


def add_virtual_cates():
    parent_url = "https://www.insead.edu/executive-education"
    source = requests.get(parent_url)
    page = source.content
    page = bs4.BeautifulSoup(page,'html.parser')
    li = page.find('ul',attrs={"class":"level1"}).find_all('li',recursive=False)[-3]
    name = li.a.text
    url = li.a.get('href')
    url = urllib.parse.urljoin("https://www.insead.edu/executive-education/",url)

    virtual_cate = {"category":name,
                    "parent_url":parent_url,
                    "url":url}
    pprint(virtual_cate)
    return virtual_cate


def add_online_cates():
    parent_url = "https://www.insead.edu/executive-education"
    source = requests.get(parent_url)
    page = source.content
    page = bs4.BeautifulSoup(page, 'html.parser')
    li = page.find('ul', attrs={"class": "level1"}).find_all('li', recursive=False)[-4]

    name = li.a.text
    url = li.a.get('href')
    url = urllib.parse.urljoin("https://www.insead.edu/executive-education/", url)

    online_cate = {"category": name,
                   "parent_url": parent_url,
                   "url": url}
    pprint(online_cate)
    return online_cate


def rewrite_cates():
    cates = read_from_json('./final_files/category_8888_EUR_XW_0524.json')
    virtual_cate = add_virtual_cates()
    online_cate = add_online_cates()
    cates.append(virtual_cate)
    cates.append(online_cate)
    write_to_json(cates, './final_files/category_8888_EUR_XW_0524.json')


def get_online_courses():
    online_courses = {}
    url = "https://www.insead.edu/executive-education/online-programmes"
    source = requests.get(url)
    page = source.content
    page = bs4.BeautifulSoup(page, 'html.parser')
    course_block = page.find_all("div",attrs={"class":"row equal-box"})[1]
    titles = course_block.find_all("h3")
    for title in titles:
        name = title.find('a').text
        url = title.a.get('href')
        online_courses[name] = url
    return online_courses


def get_virtual_cates():
    virtual_cates = []
    parent_url = "https://www.insead.edu/executive-education"
    source = requests.get(parent_url)
    page = source.content
    page = bs4.BeautifulSoup(page, 'html.parser')
    li = page.find('ul', attrs={"class": "level1"}).find_all('li', recursive=False)[-3]
    sub_cates = li.ul.find_all('li',recursive=False)
    for sub_cate in sub_cates:
        name = sub_cate.a.text
        virtual_cates.append(name)
    return virtual_cates


def add_virtual_online_cates_to_courses():
    details = read_from_json('./final_files/detail_8888_EUR_XW_0524.json')
    online_courses = get_online_courses()
    virtual_cates = get_virtual_cates()

    for detail in details:
        if detail["name"] in online_courses:
            detail["category"].append('Online Programmes')
        for cate in detail["category"]:
            if cate in virtual_cates:
                detail["category"].append("Live Virtual Programmes")
                break
    write_to_json(details, './final_files/detail_8888_EUR_XW_0524.json')


def modify_certificate_main():
    cates = read_from_json('./final_files/category_8888_EUR_XW_0524.json')
    for cate in cates:
        if cate["category"] == "Certificates":
            cate["url"] = "https://www.insead.edu/executive-education/certificates"
    write_to_json(cates, './final_files/category_8888_EUR_XW_0524.json')












