def filter_out_masters_category_list(url):
    new_cates = []
    cate = {"category":'Master Programmes',
            "url":url,
            "parent_url":url}
    new_cates.append(cate)
    return new_cates


def filter_out_masters_course_list(details):
    new_courses = []
    for detail in details:
        course = {'name':detail['name'],
                  'url':detail['url'],
                  'category_name':detail['category'],
                  'category_url':detail['category_url']}
        new_courses.append(course)
    return new_courses


def filter_out_masters_detail_list(details):
    for detail in details:
        del detail["category_url"]
        del detail["parent_url"]
    return details