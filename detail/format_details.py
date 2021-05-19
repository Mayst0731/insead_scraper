import copy


def delete_useless_urls(course):
    useless_urls = ["faculty_url","version_url","testimonials_url"]
    for useless_url in useless_urls:
        del course[useless_url]
    if len(course['faculty']) != 0:
        for fac in course['faculty']:
            del fac['faculty_sub_url']
    return course


def version_info_dispatch(course):
    course_list = []
    # get out the 'version_info' attr
    version_info_list = course['version_info']
    # delete 'version_info' attr
    del course['version_info']
    # count a course's versions and add each version into the course
    versions = len(version_info_list)
    if versions > 0:
        for version_info in version_info_list:
            new_course = copy.deepcopy(course)
            new_course.update(version_info)
            course_list.append(new_course)
    return course_list


def delete_ascii_string(course):
    for value in course.values():
        value.strip().replace()

    return


def format_course_detail(courses_info):
    new_courses_info = []
    for course in courses_info:
        new_course = delete_useless_urls(course)
        new_courses_list_with_version_info = version_info_dispatch(new_course)
        new_courses_info += new_courses_list_with_version_info
    return new_courses_info