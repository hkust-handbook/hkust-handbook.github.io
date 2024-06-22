# Home

## Contributing

If you create new files, please update `nav.yml` accordingly.

### Notes

1. Prepare a link to the notes.
2. Find the markdown file for the corresponding subject in `docs/notes/`. E.g.,
   `comp.md` is for Computer Science courses. You may create a new markdown file
   if there has not been one for the subject.
3. In the file, please follow this format:
   ```markdown
   # <subject abbreviation> - <subject full name>

   ## <course code>

   Course Name: <course full name>

   ### Notes

   | link | offering | format | author | remark |
   | :-: | :- | :- | :- | :- |
   | <link> | <offering> | <format> | <author> | <remark> |

   ### Review / Comment / Suggestions
   ```

### Advise, exchange experience, research and others

For other advice, add/edit files in `docs/`:

- Exchange experience: add/edit `docs/ex/<school-abbr>.md`
- Research: add/edit `docs/res/<title>.md`

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

<script type="text/javascript" id="clustrmaps" src="//clustrmaps.com/map_v2.js?d=PaqeDe8F2IV9P2v-hbqlzig6VSY4S1GB8pNRwUoFTe8&cl=ffffff&w=a"></script>