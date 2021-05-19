from pprint import pprint

from write_to_json import read_from_json, write_to_json


def final_detail(detail_list):
    new_detail_list = []
    for detail in detail_list:
        version_info_list = detail['version_detail']
        if len(version_info_list) == 0:
            overview = {"desc": detail["overview"],
                        "video_url": detail["video_url"],
                        "video_title": detail["video_title"]}
            new_detail = {"name": detail["course"],
                          "url": detail["url"],
                          "category": detail["category"],
                          "category_tags": "",
                          "active": True,
                          "course_takeaways": detail["course_takeaways"],
                          "video_title": detail["video_title"],
                          "video_url": detail["video_url"],
                          "desc": detail["overview"],
                          "overview": overview,
                          "who_attend_desc": detail["who_attend_desc"],
                          "university_school": "8888_EUR",
                          "credential": "",
                          "duration_consecutive": True,
                          "priority": 0,
                          "publish": 100,
                          "is_advanced": True,
                          "Repeatable": "Yes",
                          "who_attend_params": "{'working experience':'','background knowledge':''}",
                          "languages": detail['languages'],
                          "Repeatable": "Y",
                          "course_faculties": new_faculty,
                          "testimonials": detail["testimonials"],
                          "effective_date_start": "",
                          "effective_date_end": "",
                          "location": [
                              "Fontainebleau"
                          ],
                          "currency": "",
                          "tuition": 0,
                          "tuition_note": "",
                          "type": "",
                          "active": False,
                          "version": 1,
                          "exec_ed_inquiry_cc_email": detail["exec_ed_inquiry_cc_email"]}
            new_detail_list.append(new_detail)
        else:
            for version_info in version_info_list:
                locations = version_info['location']
                new_locations = final_location(locations)
                version_info['location'] = new_locations
                faculty = detail['faculty']
                new_faculty = final_faculty(faculty)
                overview = {"desc": detail["overview"],
                            "video_url": detail["video_url"],
                            "video_title": detail["video_title"]}
                part_detail = {"name": detail["course"],
                               "url": detail["url"],
                               "category": detail["category"],
                               "category_tags": [],
                               "active": True,
                               "audience_title_level": '',
                               "course_takeaways": detail["course_takeaways"],
                               "overview": overview,
                               "who_attend_desc": detail["who_attend_desc"],
                               "university_school": "8888_EUR",
                               "credential": "",
                               "duration_consecutive": "Yes",
                               "priority": 0,
                               "publish": 100,
                               "is_advanced": True,
                               "Repeatable": "Y",
                               "who_attend_params": "{'working experience':'','background knowledge':''}",
                               "languages": detail['languages'],
                               "course_faculties": new_faculty,
                               "testimonials": detail["testimonials"],
                               "exec_ed_inquiry_cc_email": detail["exec_ed_inquiry_cc_email"],
                               "desc": overview['desc']}
                new_detail = {**part_detail, **version_info}
                new_detail["tuition"] = int(new_detail["tuition"])
                new_detail_list.append(new_detail)
    new_detail_list = add_schedule(new_detail_list)
    new_detail_list = modify_credential_and_other_attrs(new_detail_list)
    return new_detail_list


def final_faculty(faculties):
    new_faculties = []
    for fac in faculties:
        new_faculties.append(fac["name"])
    return new_faculties


def final_location(locations):
    loc_set = set()
    for loc in locations:
        if loc == 'Live Virtual' or loc == 'Online' or loc == "Blended":
            new_loc = 'Fontainebleau'
            loc_set.add(new_loc)
        else:
            loc_set.add(loc)
    return list(loc_set)


def add_schedule(details):
    for detail in details:
        start_date = detail["effective_date_start"]
        end_date = detail["effective_date_end"]
        duration_num = detail.get("duration_months", '')
        if not duration_num:
            duration_num = detail.get("duration_weeks", '')
        if not duration_num:
            duration_num = detail.get("duration_days", '')
        if duration_num != '':
            duration_num = str(duration_num)
        detail["schedule"] = [[start_date, end_date, duration_num, 'formal']]
    return details


def modify_credential_and_other_attrs(details):
    for detail in details:
        detail["tuition_number"] = detail["tuition"]
        del detail["tuition"]
        del detail["is_advanced"]
        detail["is_advanced_management_program"] = False
        detail["location"] = locations_map(detail["location"])
        detail["duration_desc"] = ""
        detail["languages"] = languages_map(detail["languages"])
        if "Certificates" in detail["category"]:
            detail["credential"] = 'Certificate'
        if detail["type"] == '':
            detail["type"] = "Onsite"
        if "audience_title_level" not in detail:
            detail["audience_title_level"] = ''
    return details


def languages_map(language):
    lang_dict = {"en": "English",
                 "ro": "Romanian",
                 "da": "Danish",
                 "nl": "Dutch",
                 "fr": "French",
                 "de": "German",
                 "no": "Norwegian",
                 "id": "Indonesian"}
    return lang_dict.get(language, 'English')


def locations_map(locations):
    location_dict = {"Fontainebleau": "Fontainebleau, ----, France",
                     "Singapore": "Singapore, ----, Singapore",
                     "San Francisco": "San Francisco, CA, United States",
                     "Beijing": "China, ----, Beijing"}
    if len(locations) == 0:
        new_locations = ["Fontainebleau, ----, France"]
        return new_locations
    new_locations = []
    for location in locations:
        new_loc = location_dict.get(location)
        new_locations.append(new_loc)
    return new_locations


def modify_course_keys(courses):
    new_courses = []
    for course in courses:
        new_course = {"name": course["course"],
                      "url": course["url"],
                      "category_name": course["category"],
                      "category_url": course["category_url"]}
        new_courses.append(new_course)
    return new_courses


def delete_repeat_faculties_for_faculty_list(faculties):
    new_faculties = []
    faculty_set = set()
    for fac in faculties:
        if fac["name"] not in faculty_set:
            faculty_set.add(fac["name"])
            new_faculties.append(fac)
        else:
            continue
    return new_faculties


def modifying_testi_title_length():
    details = read_from_json('./final_files/detail_8888_EUR_XW_0226.json')
    occupations = ["Director", "Consultant", "President", "CEO", "Manager", "Head", "Owner", "Lead", "Officer"]
    for detail in details:
        all_testis = detail.get("testimonials", [])
        for testi in all_testis:
            if len(testi["title"]) > 20:
                for occ in occupations:
                    if occ in testi["title"]:
                        testi["title"] = occ
                        break
        for testi in all_testis:
            if len(testi["title"]) > 20:
                testi["company"] = testi["title"]
                testi["title"] = ""
            if len(testi["title"]) > 20:
                print("title: ", testi["title"])
            if len(testi["company"]) > 20:
                print("company: ", testi["company"])
    write_to_json(details, './final_files/detail_8888_EUR_XW_0226.json')


def modify_duration_consecutive():
    details = read_from_json('./final_files/detail_8888_EUR_XW_0226.json')
    for detail in details:
        detail["duration_consecutive"] = detail.get("duration_consecutive", 'Yes')
        if detail["duration_consecutive"] != "Yes" or detail["duration_consecutive"] != "":
            detail["duration_consecutive"] = "Yes"
        if detail["duration_consecutive"] == "Yes":
            detail["duration_consecutive"] = True
    write_to_json(details, './final_files/detail_8888_EUR_XW_0226.json')


def modify_course_type():
    details = read_from_json('./final_files/detail_8888_EUR_XW_0226.json')
    type_map = {'Blended - Onsite & Self-paced': 'blended-os',
                'Blended - Onsite & Virtual': 'blended-ov',
                'Online - Self-paced': 'online-selfpaced',
                'Online - Virtual': 'online-virtual',
                'Onsite': 'onsite'}
    for detail in details:
        course_type = detail.get("type", '')
        if "Live Virtual" in course_type:
            detail["type"] = detail["type"].replace("Live Virtual", 'Virtual')
        detail["type"] = type_map.get(detail["type"],'onsite')
    write_to_json(details, './final_files/detail_8888_EUR_XW_0226.json')




