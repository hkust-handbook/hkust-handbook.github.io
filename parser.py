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
    |-- docs
        |-- notes
            |-- <subject>.md
    """
    file_name = 'raw/notes.json'
    backup_name = 'raw/notes-backup.json'
    shutil.copy(file_name, backup_name)
    
    records = pd.read_json(file_name, orient='records', dtype=False)
    records.sort_values(by=['subject', 'code', 'offering'], inplace=True, ignore_index=True)

    with open(file_name, 'w') as f:
        json.dump(json.loads(records.to_json(orient='records')), f, indent=2)
        
    # hyperlink
    records['link'] = '[' + records['title'] + '](' + records['link'] + ')'

    subjects = sorted(set(records['subject'].tolist()))

    # Update nav
    nav_name = 'nav.yml'
    with open(nav_name, 'r') as f:
        navs = yaml.safe_load(f)
        for item in navs['nav']:
            if list(item.keys()) == ['Course Notes']:
                item['Course Notes'] = ['notes/' + _.lower() + '.md' for _ in subjects]
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
    
    for subject in subjects:
        records_this_subject = records.groupby(by='subject').get_group(subject)
        
        dest_name = f'docs/notes/{subject}.md'
        os.makedirs(os.path.dirname(dest_name), exist_ok=True)

        with open(dest_name, 'w') as f:
            f.write(f'# {subject}\n\n')
            
            codes = sorted(set(records_this_subject['code'].tolist()))

            for code in codes:
                f.write(f'## {subject} {code}\n\n')
                records_this_code = records_this_subject.groupby(by='code').get_group(code)
                records_this_code.drop(['subject', 'code', 'title'], axis='columns', inplace=True)
                f.write(records_this_code.to_markdown(index=False))
                f.write('\n')
        

if __name__=='__main__':
    parse_notes()
