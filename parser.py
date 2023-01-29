import shutil
import os

import json
import yaml
import pandas as pd

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
            |-- <subject>.md
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
    nav_name = 'nav.yml'
    with open(nav_name, 'r') as f:
        navs = yaml.safe_load(f)
        for item in navs['nav']:
            if list(item.keys()) == ['Course Notes']:
                item['Course Notes'] = ['notes/' + _ + '.md' for _ in subject_list]
    with open(nav_name, 'w') as f:
        yaml.dump(navs, f)

    # Update mkdocs
    mkdocs_name = 'mkdocs.yml'
    config_name = 'config.yml'
    with open(mkdocs_name, 'w') as fo:
        with open(config_name, 'r') as fi:
            fo.write(fi.read())
        with open(nav_name, 'r') as fi:
            fo.write(fi.read())

    # Create <subject>.md files
    for subject in subject_list:
        dest_name = f'docs/notes/{subject}.md'
        os.makedirs(os.path.dirname(dest_name), exist_ok=True)
        with open(dest_name, 'w') as f:
            f.write(f'# {subject.upper()}\n\n')

    # Load courses.csv for course information
    csv_name = 'raw/courses.csv'
    courses_info = pd.read_csv(csv_name, header='infer', index_col='Course Code')
    
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
            records_this_code = records.groupby(by='code').get_group(code)
            records_this_code = records_this_code.loc[:, records_this_code.columns != 'code']
            f.write(records_this_code.to_markdown(index=False))
            f.write('\n')
        

if __name__=='__main__':
    parse_notes()
