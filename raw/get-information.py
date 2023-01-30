# This code is retrieved from https://github.com/zory233/CurriculumMap/blob/main/get-information/get-information.py

'''
This part of the python code collects the course information on the HKUST website

https://prog-crs.ust.hk/ugcourse

and provides two Excel saving format (.xls) and (.csv).

The collected data will be used for mapping.

'''

import re
import csv
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

#for .xls file you should use

'''
import xlwt
url = 'https://prog-crs.ust.hk/ugcourse/2022-23'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "lxml")
'''

#special case detector (abandoned)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def get_content(content):
    # content is a string
    # badstring
    content = content.replace("&amp;", "&")
    # content = content.replace("&quot;", "$")
    # content = content.replace("&apos;", "#")
    content = content.replace("“","$")
    content = content.replace("”","$")
    content = content.replace("\"", "$")
    content = content.replace("‘","#")
    content = content.replace("’","#")
    content = content.replace("\'","#")
    content = content.replace("&lt;", "<")
    content = content.replace("&gt;", ">")
    # csv specific
    content = content.replace(",", "@")
    content = content.strip('\xa0')
    return content

def get_subject_list(soup):
    subject_prefix = [ chr(ord('A') + i) for i in range(26)]
    subject_list = []
    for prefix in tqdm(subject_prefix, desc="Crawling Subjects"):
        subject_this_prefix = soup.find_all("li", {"class" : "subject subject-prefix-" + prefix})
        for subject in subject_this_prefix:
            abbr = subject.a.get("title")[:4]
            name = subject.a.get("title")[6:]
            url = "https://prog-crs.hkust.edu.hk" + str(subject.a.get("href"))
            subject_list.append({'abbr': abbr, 'name': name, 'url': url})
    return subject_list

def get_courses(subject_list):
    courses = []
    for subject in tqdm(subject_list, desc="Crawling Courses"):
        url = subject['url']
        #use soup to find "li" Label and specified classes
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        courses.extend(soup.find_all("li", {"class": "crse accordion-item"}))
    return courses

def process_courses(courses):
    all_row = []

    # Regular Expression
    reg = re.compile("<[^>]*>")

    for course in tqdm(courses, desc="Processing Courses"):
        row = [] # Operation row
        st = reg.sub('$', str(course))  # Regular Expression Replace
        st = st.strip()
        #print(st)
        entries = st.split('$')
        entries = list(filter(None, entries))
        #print(entries)
        # Course Code
        course_code = get_content(entries[0])
        course_code = course_code.replace(" ", "")
        course_code = course_code.lower()
        row.append(course_code)
        row.append(get_content(entries[1])) # Name
        row.append(get_content(entries[2])) # Credits

        #Prerequisite(s)
        cnt = entries.count('Prerequisite(s)')
        if cnt != 0:
            index = entries.index('Prerequisite(s)')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Exclusion(s)
        cnt = entries.count('Exclusion(s)')
        if cnt != 0:
            index = entries.index('Exclusion(s)')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Corequisite(s)
        cnt = entries.count('Corequisite(s)')
        if cnt != 0:
            index = entries.index('Corequisite(s)')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Co-list with
        cnt = entries.count('Co-list with')
        if cnt != 0:
            index = entries.index('Co-list with')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Mode of Delivery
        cnt = entries.count('Mode of Delivery')
        if cnt != 0:
            index = entries.index('Mode of Delivery')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Previous Course Code(s)
        cnt = entries.count('Previous Course Code(s)')
        if cnt != 0:
            index = entries.index('Previous Course Code(s)')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Alternate code(s)
        cnt = entries.count('Alternate code(s)')
        if cnt != 0:
            index = entries.index('Alternate code(s)')
            row.append(get_content(entries[index + 1]))
        else:
            row.append('')

        #Description
        cnt = entries.count('Description')
        if cnt != 0:
            index = entries.index('Description')
            temp = get_content(entries[index + 1])
            row.append(temp)
        else:
            row.append('')

        all_row.append(row)

    return all_row

def output_subjects_csv(path, subject_list_ug, subject_list_pg):
    df_ug = pd.DataFrame.from_records(subject_list_ug).drop(['url'], axis='columns')
    df_pg = pd.DataFrame.from_records(subject_list_pg).drop(['url'], axis='columns')
    df = pd.concat((df_ug, df_pg)).drop_duplicates('abbr')
    df.to_csv(path, header=True, index=False, index_label='abbr')

def output_csv(path, all_row):
    all_row_length = len(all_row)
    #supporting Chinese by 'utf-8-sig'
    with open(path,'w',newline = '', encoding="utf-8-sig") as file_csv:
        csv_write = csv.writer(file_csv)
        csv_head = ['Course Code', 'Course Name', 'Course Credits', 'Prerequisite(s)', 'Exclusion(s)','Corequisite(s)','Co-list with','Mode of Delivery','Previous Course Code(s)','Alternate code(s)', 'Description']
        csv_write.writerow(csv_head)
        for sub_list in all_row:
            csv_write.writerow(sub_list)

def main():
    # reserved for special case with '\xa0'
    '''
    temp = temp.strip('\xa0')
    temp = temp.strip(';')
    '''

    #a special case may be used in the following sections

    '''
    if t_list and t_list[0] != '': #special cases
        if is_number(t_list[0][0]) and len(t_list[0]) <= 10:
            row.append(t_list[0])
    '''

    print("Loading HTML")

    base_url_ug = 'https://prog-crs.ust.hk/ugcourse/'
    base_url_pg = 'https://prog-crs.ust.hk/pgcourse/'
    
    html_ug = urllib.request.urlopen(base_url_ug).read()
    soup_ug = BeautifulSoup(html_ug, "lxml")
    html_pg = urllib.request.urlopen(base_url_pg).read()
    soup_pg = BeautifulSoup(html_pg, "lxml")

    subject_list_ug = get_subject_list(soup_ug)
    subject_list_pg = get_subject_list(soup_pg)
    output_subjects_csv('subjects.csv', subject_list_ug, subject_list_pg)

    courses_ug = get_courses(subject_list_ug)
    courses_pg = get_courses(subject_list_pg)
    courses = courses_ug + courses_pg
    print(type(courses))
    all_row = process_courses(courses)

    output_csv("courses.csv", all_row)

if __name__ == '__main__':
    main()

"""
"""
