import re


def month_dict(month_str):
    months_check = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12',
        }
    return months_check[month_str]


def get_currency(price):
    if 'S' or '$' in price:
        currency = 'USD'
    if '€' in price:
        currency = 'EUR'
    return currency


def get_tuition(price):
    tuition = ''
    tuition += ''.join(re.findall('\d+', price))
    return tuition


def get_start_date(str):
    try:
        if 'Module' in str:
            str = str[9:]
        if '-' in str:
            str = str[:str.index('-')]

        date_split = str.split()
        date = date_split[-1] + '-' + month_dict(date_split[1]) + '-' + date_split[0]
    except:
        date = ''
    return date


def get_end_date(str):
    date = ''
    try:
        if 'Module' in str:
            str = str[9:]
        if '-' in str:
            all = str.split('-')
            end_date = all[-1]
            date_split = end_date.split()
            date = date_split[-1] + '-' + month_dict(date_split[1]) + '-' + date_split[0]
    except:
        pass
    return date


def get_duration_type(length):
    length = str(length)
    if 'days' in length or 'Days' in length:
        type = 'days'
    if 'weeks' in length or 'Weeks' in length:
        type = 'weeks'
    if 'months' in length:
        type = 'months'
    return type


def get_duration_num(length):
    res = list(map(int, re.findall('\d+', length)))
    if 'months' in length and ('days' or 'weeks') in length:
        return res[0]

    if 'half' in length:
        duration_num = sum(res) + 0.5
    elif ',' in length:
        duration_num = sum(res[:1] + res[2:])
    else:
        duration_num = sum(res)
    return duration_num


def get_single_module_course_type(location):
    type = {
        'Blended': 'Blended - Onsite & Virtual',
        'Online': 'Online - Self-paced',
        'Live Virtual' : 'Online - Virtual',
    }

    if location in type:
        return type[location]
    else:
        return 'Onsite'


def get_multi_module_course_type(locations):
    if len(locations) == 1:
        course_type = get_single_module_course_type(locations[0])
        return course_type
    types = []
    type_dic = {
        'Online': 'self-paced',
        'Live Virtual': 'virtual',
    }
    types = ''
    if 'Online' not in locations and 'Live Virtual' not in locations:
        return 'Onsite-self-paced'
    elif 'Online' in locations or "Blended" in locations:
        types = 'Blended - Onsite & self-paced'
    elif 'Live Virtual' in locations:
        types = 'Blended - Onsite & Live Virtual'
    return types