import shutil
import os

import json
import yaml
import pandas as pd

def update_mkdocs():
    mkdocs_name = 'mkdocs.yml'
    config_name = 'config.yml'
    nav_name = 'nav.yml'
    with open(mkdocs_name, 'w') as fo:
        with open(config_name, 'r') as fi:
            fo.write(fi.read())
        with open(nav_name, 'r') as fi:
            fo.write(fi.read())

def parse_notes():
    """
    |-- parser.py
    |-- config.yml
    |-- nav.yml
    |-- mkdocs.yml
    |-- raw
        |-- notes.json
        |-- courses.csv
    |-- docs
        |-- notes
            |-- <subject>
                |-- index.md
                |-- <course>.md
    """
    file_name = 'raw/notes.json'
    backup_name = 'raw/notes-backup.json'
    shutil.copy(file_name, backup_name)

    records = pd.read_json(file_name, orient='records', dtype=False)

    # Normalize course code
    def normalize_code(code):
        code = code.replace(" ", "")
        code = code.lower()
        return code
    records['code'] = records['code'].apply(normalize_code)
    code_list = sorted(set(records['code'].tolist()))
    subject_list = sorted(set([code[:4] for code in code_list]))

    # Sort by course code and offering
    records.sort_values(by=['code', 'offering'], inplace=True, ignore_index=True)

    # Overwrite the original file (Modifications above do not break the format)
    with open(file_name, 'w') as f:
        json.dump(json.loads(records.to_json(orient='records')), f, indent=2)

    # Synthesize hyperlink
    records['link'] = '[' + records['title'] + '](' + records['link'] + ')'
    records.drop(['title'], axis='columns', inplace=True)

    # Update nav



    course_index_name = 'notes/index.md'
    nav = load_nav()
    nav_notes = next(filter(lambda x:list(x.keys()) == ['Courses'], nav['nav']))
    nav_notes['Courses'].extend(['notes/' + _ + '.md' for _ in subject_list])
    nav_notes['Courses'].remove(course_index_name)
    nav_notes['Courses'] = [course_index_name] + sorted(set(nav_notes['Courses']))
    dump_nav(nav)

    subjects_csv_name = 'raw/subjects.csv'
    subjects_csv = pd.read_csv(subjects_csv_name, header='infer', index_col='abbr')

    # Create <subject>.md files
    for subject in subject_list:
        dest_name = f'docs/notes/{subject}.md'
        os.makedirs(os.path.dirname(dest_name), exist_ok=True)
        with open(dest_name, 'w') as fo:
            subject_entry = subjects_csv.loc[subject.upper()]
            fo.write(f'# {subject.upper()} - {subject_entry[("name")]}\n\n')
            rem_name = f'raw/subjects/{subject}.md'
            if os.path.exists(rem_name):
                with open(rem_name, 'r') as fi:
                    fo.write(fi.read())
                    fo.write('\n')

    # Load courses.csv for course information
    courses_csv_name = 'raw/courses.csv'
    courses_info = pd.read_csv(courses_csv_name, header='infer', index_col='Course Code')

    # Fill in <subject>.md files
    for code in code_list:
        subject = code[:4]
        code_display = code.upper()
        dest_name = f'docs/notes/{subject}.md'
        with open(dest_name, 'a') as f:
            # Write headline
            f.write(f'## {code_display}\n\n')

            # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
            # Write course information
            f.write(f'Course Name: {courses_info.loc[code, ("Course Name")]}\n\n')
            if not courses_info.loc[code, ('Previous Course Code(s)')]:
                f.write(f'Previous Course Code(s): {courses_info.loc[code, ("Previous Course Code(s)")]}\n\n')
            if not courses_info.loc[code, ('Alternate code(s)')]:
                f.write(f'Alternate code(s): {courses_info.loc[code, ("Alternate code(s)")]}\n')
            # Write table of notes
            f.write('### Notes\n\n')
            records_this_code = records.groupby(by='code').get_group(code)
            records_this_code = records_this_code.loc[:, records_this_code.columns != 'code']
            f.write(records_this_code.to_markdown(index=False))
            f.write('\n\n')
            # Write review
            rem_name = f'raw/codes/{code}.md'
            if os.path.exists(rem_name):
                with open(rem_name, 'r') as fi:
                    f.write('### Review\n\n')
                    f.write(fi.read())
                    f.write('\n')

def parse_others():
    title_path_list = [('Exchange and Credit Transfer', 'docs/ex/'),
                       ('Research', 'docs/res/')]

    # Update nav
    nav = load_nav()

    for title, path in title_path_list:
        nav_title = next(filter(lambda x:list(x.keys()) == [title], nav['nav']))
        nav_title[title] = []
        for child_dir in os.listdir(path):
            child_path = os.path.join(path, child_dir)
            if not os.path.isfile(child_path): continue
            ext = os.path.splitext(child_path)[1]
            if ext != '.md': continue
            nav_title[title].append(child_path.removeprefix('docs/'))
        nav_title[title] = sorted(set(nav_title[title]))
    dump_nav(nav)

def get_subject_fullname(subject_csv, subject_abbr):
    return subject_csv.loc[subject_abbr.upper()][("name")]

def get_course_info(course_csv, course_code):
    course_fullname = course_csv.loc[course_code, ("Course Name")]
    return course_fullname
    # if not courses_info.loc[code, ('Previous Course Code(s)')]:
    #     f.write(f'Previous Course Code(s): {courses_info.loc[code, ("Previous Course Code(s)")]}\n\n')
    # if not courses_info.loc[code, ('Alternate code(s)')]:
    #     f.write(f'Alternate code(s): {courses_info.loc[code, ("Alternate code(s)")]}\n')

def update_notes_nav():
    notes_root = 'docs/notes/'

    subject_csv_filename = 'raw/subjects.csv'
    subject_csv = pd.read_csv(subject_csv_filename, header='infer', index_col='abbr')

    course_csv_name = 'raw/courses.csv'
    course_csv = pd.read_csv(course_csv_name, header='infer', index_col='Course Code')

    notes_nav = []
    for nowdir, subdirs, files in os.walk(notes_root):
        docdir = nowdir.removeprefix('docs/') # root used in nav.yml
        md_files = [f for f in files if f.endswith(".md")]
        md_files = sorted(md_files)

        print(nowdir, subdirs, md_files)
        print()
        if nowdir == notes_root:
            notes_nav.append(os.path.join(docdir, 'index.md'))
            notes_nav.append({f'Enrollment': os.path.join(docdir, 'enroll.md')})
        else:
            subject_abbr = nowdir.removeprefix(notes_root)
            subject_abbr_upper = subject_abbr.upper()
            subject_fullname = get_subject_fullname(subject_csv, subject_abbr)
            print('subject', subject_abbr, subject_abbr_upper, subject_fullname)

            local_nav = []

            if 'index.md' in md_files:
                local_nav.append(os.path.join(docdir, 'index.md'))
            for file in md_files:
                fullpath = os.path.join(docdir, file)
                if file == 'index.md':
                    continue
                else:
                    course_code = file.removesuffix('.md')
                    course_code_upper = course_code.upper()
                    course_fullname = get_course_info(course_csv, course_code)
                    local_nav.append({f'{course_code_upper} - {course_fullname}': fullpath})

            print(local_nav)
            # Write table of notes

            notes_nav.append({f'{subject_abbr_upper} - {subject_fullname}': local_nav})

    return notes_nav

def load_nav():
    nav_name = 'nav.yml'
    with open(nav_name, 'r') as f:
        nav = yaml.safe_load(f)
    return nav

def dump_nav(nav):
    nav_name = 'nav.yml'
    with open(nav_name, 'w') as f:
        yaml.dump(nav, f)

def on_config(config, **kwargs):
    print('Running hook (on_config): parser.py')
    # parse_notes() # update nav
    # parse_others() # update nav
    notes_nav = update_notes_nav()
    print('=' * 10)
    print(notes_nav)
    nav = load_nav()
    nav_notes = next(filter(lambda x:list(x.keys()) == ['Courses'], nav['nav']))
    nav_notes['Courses'] = notes_nav
    print('=' * 10)
    print(nav)
    dump_nav(nav)
    config.nav = nav['nav']
    return config

if __name__=='__main__':
    on_config()
