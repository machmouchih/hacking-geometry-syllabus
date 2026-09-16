# Moodle version

`syllabus-moodle.html` is an HTML **fragment** for pasting into a Moodle Page
resource. `preview.html` wraps the same fragment so it can be opened in a
browser. `build_moodle.py` generates both; edit the content lists at the top of
that script rather than the generated files.

## Why this is a separate build

Moodle strips `<script>` and `<style>` from Page resources and blocks external
stylesheets, so the Tailwind CDN and Google Fonts used by `index.html` do not
survive. Everything here is an inline `style=` attribute, which Moodle keeps.
There are no classes, no ids, no JavaScript, and no external requests. Layout is
single column so it works inside Moodle's themed content area on a phone.

Fonts fall back through the stack: Libre Franklin, then Franklin Gothic, then
Roboto, then Arial. Students see the intended face if they have it and a
reasonable substitute if not.

## Adding it to Moodle

1. Turn editing on, then **Add an activity or resource** and choose **Page**.
2. Give it a name, for example `Syllabus`.
3. In the **Page content** editor, open the HTML source view. In TinyMCE this is
   under the three-dot menu as **Source code**; in Atto it is the `< >` button.
4. Paste the entire contents of `syllabus-moodle.html`, save, and view the page.

Check it after the first save. Moodle sanitises content on save, and a hardened
install may still strip some inline styles.

## Rebuilding

    python3 moodle/build_moodle.py
