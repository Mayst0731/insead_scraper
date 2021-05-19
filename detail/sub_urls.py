import urllib


def add_related_urls_info_course_info(course_info,course_obj):
    testimonial_link = course_obj.find('a',text="Testimonials")
    try:
        faculty_link = course_obj.find('ul',attrs={'class':'level1'}).find('a',text='Faculty')
    except:
        faculty_link = None
    version_link = course_obj.find('a',text = 'Dates & Fees')
    if not version_link:
        version_link = course_obj.find('a', text='Dates and Fees')
    course_info['faculty_url'] = ''
    course_info['version_url'] = ''
    course_info['testimonials_url'] = ''
    if faculty_link is not None:
        course_info['faculty_url'] = urllib.parse.urljoin('https://www.insead.edu/executive-education/',
                                                          faculty_link.get('href'))
    if version_link is not None:
        course_info['version_url'] = urllib.parse.urljoin('https://www.insead.edu/executive-education/',
                                                          version_link.get('href'))
    if testimonial_link is not None:
        course_info['testimonials_url'] = urllib.parse.urljoin('https://www.insead.edu/executive-education/',
                                                           testimonial_link.get('href'))
    return course_info