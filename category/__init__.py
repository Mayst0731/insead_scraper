from download_parse import download_site
import urllib


async def extract_categories(url,session):
    print('hello cate')
    category_page = await download_site(url,session)
    all_categories = []
    open_programms = category_page.find('ul',attrs={"class":"level1"}).find('li',attrs={"class":"active"}).find(
        'ul',attrs={"class":"level2"}).find_all('li',recursive=False)
    for program in open_programms[:-1]:
        cate_name = program.a.text
        cate_relative_link = program.a.get('href')
        cate_link = urllib.parse.urljoin('https://www.insead.edu/executive-education/', cate_relative_link)
        category = package_category(cate_link,url,cate_name)
        all_categories.append(category)
    level1_lis = category_page.find('ul',attrs={"class":"level1"}).find_all('li',recursive=False)
    special_programms = ['Certificates','Coaching']
    for li in level1_lis:
        title = li.a.text
        if title == special_programms[0]:
            cate_link = get_certificate_cate_link(li)
            category = package_category(cate_link,url,title)
            all_categories.append(category)
        if title == special_programms[1]:
            cate_link = get_coaching_cate_link(li)
            category = package_category(cate_link,url,title)
            all_categories.append(category)
    return all_categories


def package_category(url,parent_url,category):
    cate_info = {
        'category': category,
        'url': url,
        'parent_url': parent_url
    }
    return cate_info


def get_certificate_cate_link(li):
    cert_link_tag = li.find('div',attrs={"class":"submenu"}).find('ul',attrs={"class":"level2"}).find_all("li",
    recursive=False)[-2]
    cert_relative_link = cert_link_tag.a.get('href')
    cate_url = urllib.parse.urljoin('https://www.insead.edu/executive-education/', cert_relative_link)
    return cate_url


def get_coaching_cate_link(li):
    coach_link_tag = li.find('div',attrs={"class":"submenu"}).find('ul',attrs={"class":"level2"}).find_all("li",
    recursive=False)[-3]
    coach_relative_link = coach_link_tag.a.get('href')
    cate_url = urllib.parse.urljoin('https://www.insead.edu/executive-education/', coach_relative_link)
    return cate_url