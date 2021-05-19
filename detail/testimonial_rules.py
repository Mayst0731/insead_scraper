
from download_parse import download_site
import re


def truncate_statement_length(statement):
    truncated = statement
    if "." in statement:
        pattern = "([^\.]+)"
        truncated = re.match(pattern,statement).group()
    return truncated


async def extract_testimonial_info(course_info,session):
    testimonials_url = course_info['testimonials_url']
    if testimonials_url == '':
        course_info['testimonials'] = []
        return course_info
    testimonials_page = await download_site(testimonials_url,session)
    get_testimonial_info(course_info,testimonials_page)
    return course_info


def get_testimonial_info(course_info,testimonial_page_obj):
    # get all the person objs
    person_objs = testimonial_page_obj.find_all('div', attrs={"class": "item active"})
    persons = []
    for person_obj in person_objs:
        person = {
        'publish': 'public',
        'name': '',
        'title': '',
        'company': '',
        'testimonial_statement': '',
        'picture_url': '',
        'visual_url':'',
        "active":True,
        "publish": 100
        }
        # name,title, company
        name_title_com = get_name_title_com(person_obj)
        person['name'] = name_title_com['name']
        person['title'] = name_title_com['title'].strip()
        person['company'] = name_title_com['company'].strip()
        # person['name'], person['title'], person['company'] = distribute_name_title_company(person['name'], person['title'], person['company'])
        # quote
        person['testimonial_statement'] = get_testi_quote(person_obj).strip()
        # picture_url
        person['picture_url'] = get_pic_url(person_obj)
        persons.append(person)
    course_info['testimonials'] = persons


def distribute_name_title_company(name,title,company):
    if ',' in name:
        idx = name.index(',')
        company = f'{title}, {company}'
        name,title = name[:idx], name[idx+1:]
    return [name, title, company]






def get_name_title_com(person_obj):
    name,title,company = 'Anonymous','',''
    statement_obj = person_obj.blockquote
    needed_obj = statement_obj.next_sibling

    if no_information(needed_obj):
        return {'name':name,'title': title,'company': company}

    if no_strong_but_name(needed_obj):
        info = no_comma_in_name_info(needed_obj)
        name, title, company = info['name'], info['title'], info['company']
        return info
    if needed_obj.strong:
        name_obj = needed_obj.strong
        name_text = name_obj.text
        if ',' in name_text:
            info =  comma_in_name_info(needed_obj)
            name,title,company = info['name'],info['title'],info['company']
        else:
            info = no_comma_in_name_info(needed_obj)
            name, title, company = info['name'], info['title'], info['company']
    if '\xa0' in name:
        name = name.replace('\xa0',' ')
    if name.startswith('Dr.'):
        name = name[3:].strip()
    if '\xa0' in title:
        title = title.replace('\xa0', ' ')
    if '\xa0' in company:
        company = company.replace('\xa0', ' ')
    return {'name':name,'title': title,'company': company}


def comma_in_name_info(needed_obj):
    name,title,company = 'Anonymous','',''
    if needed_obj.strong:
        name_obj = needed_obj.strong
        text = name_obj.text
        text_lst = text.split(',')
        name = text_lst[0]
        title = ','.join(text_lst[1:])
        needed_obj.strong.extract()
    company = needed_obj.text
    return {'name':name,'title': title,'company': company}


def no_strong_but_name(needed_obj):
    info_text = needed_obj.text
    if ',' in info_text:
        return True
    else:
        return False


def no_strong_but_name_info(needed_obj):
    name, title, company = 'Anonymous', '', ''
    info_text = needed_obj.text
    if ',' in info_text:
        lst = ','.split(info_text)
        name = lst[0]
        title= ' '.join(lst[1:])
    return {'name':name,'title': title,'company': company}


def no_comma_in_name_info(needed_obj):
    name, title, company = 'Anonymous', '', ''
    if needed_obj.strong:
        name_obj = needed_obj.strong
        name = name_obj.text
        needed_obj.strong.extract()
    other_text = needed_obj.text
    if ',' in other_text:
        text_lst = other_text.split(',')
        title = text_lst[0]
        company = ','.join(text_lst[1:])
    elif ',' not in other_text:
        title = other_text
        company = ''
    return {'name':name,'title': title,'company': company}


def no_information(needed_obj):
    if not needed_obj:
        return True
    children = needed_obj.children
    first_child = [ch for ch in children if ch][0]
    if first_child.name == 'a':
        return True
    return False


def get_testi_quote(person_obj):
    statement = ''
    if person_obj:
        statement_obj = person_obj.blockquote
        statement = statement_obj.text
        statement = truncate_statement_length(statement) + '.'
    return statement


def get_pic_url(person_obj):
    url = ''
    picture_obj = None
    if person_obj:
        statement_obj = person_obj.blockquote
        if statement_obj and statement_obj.parent and statement_obj.parent.previousSibling:
            picture_obj = statement_obj.parent.previousSibling.img
        if picture_obj:
            url = 'https://www.insead.edu/' + picture_obj['src']
    return url










