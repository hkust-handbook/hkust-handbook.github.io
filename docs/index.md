# Home

## Contributing

### Notes

1. Prepare a link to the notes.
1. Upload the link to the website by editting `raw/notes.json` though [this link](https://github.com/HKUST-Courses/HKUST-Courses.github.io/edit/master/raw/notes.json)
    - `raw/notes.json` looks like
```json
[
    { 
        record 1
    },
    ...
    { 
        record n
    }
]
```
    A single course can have multiple records, each corresponding to one
    hyperlink to notes. Note the comma after each record except the last one. You can insert the new
      records into any position.

    - The record format should exactly match the template below:
```json
{
    "code": "comp1021",
    "title": "Text displayed on the link",
    "link": "https://...",
    "offering": "22-23Fall",
    "format": "PDF", 
    "author": "Your name, optional.",
    "remark": "Optional"
}
```
      Note: All field values must be surronded by a double quotation mark.
3. After finishing your editting, scroll to the bottom, **select "Create a new
   branch ... start a pull request ..."**, fill in the blank above the brief of
   your editting (e.g., which courses you add notes for), and finally choose "Propose changes".

### Course advise, exchange experience, research and others

For course related advice, add/edit files in `raw`:

- Advise on some course: add/edit `raw/codes/<course-code>.md`.
- Review of some subject: add/edit `raw/subjects/<subjetc>.md`.

For other advice, add/edit files in `docs/`:

- Exchange experience: add/edit `docs/ex/<school-abbr>.md`
- Research: add/edit `docs/res/<title>.md`

No need to manually update `mkdocs.yml`.

## To preview locally

1. Clone this repo.
```shell
git clone git@github.com:HKUST-Courses/HKUST-Courses.github.io.git
cd HKUST-Courses.github.io
```
2. Install required Python packages.
```shell
pip install -r requirements-dev.txt
```
3. Run mkdocs server
   ```shell
   mkdocs serve
   ```
4. Preview the website at localhost:8000
