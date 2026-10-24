# Site Plan Builder (Turner HSEP Safety Inscriber)

Desktop app (Python + [pywebview](https://pywebview.flowrl.com/) + embedded React UI) for walking
through and filling AcroForm fields of HSEP / site plan PDF templates, then saving the filled PDF.

## Setup

- Python 3.10 – 3.12 recommended.
- `pip install pywebview` (or `pip install -r requirements.txt`).
- On Linux pywebview additionally needs a GTK or Qt backend (see the pywebview install docs).

## Run

```
python main.py
```

## Templates layout

PDFs are loaded at start from the current directory and from `templates/`:

```
main.py
templates/
    HSEP 5.05.pdf
    ...other .pdf templates
```

Use **Open PDF…** to add files from anywhere else. **Save PDF** opens a native save dialog.
File names containing `HSEP` and `5.05` get the custom heat-stress fields injected on page 2.

## Internet note

The frontend libraries (React, pdf.js, pdf-lib) are loaded from CDNs (cdnjs / unpkg), so the
first launch requires an internet connection.

## Web version (Netlify)

`web/index.html` is the same UI and is used by `main.py`. In a normal browser (no pywebview) it
falls back to file upload for **Open PDF…** and a download for **Save PDF**.

- Deploy: connect the repo in Netlify (settings come from `netlify.toml`; publish dir `web`), or run
  `npx netlify-cli deploy --prod`.
- Template PDFs in `templates/` are copied to the site at build time. List their file names in
  `templates/index.json`, e.g. `["HSEP 5.05.pdf"]`, to have them preload on the site.

## Install with a desktop shortcut

Download/clone this repo to a permanent folder, then run `python install.py`. It creates a
local virtual environment, installs the requirements, and puts a "Site Plan Builder" shortcut on
your Desktop (`.lnk` on Windows, `.command` on macOS, `.desktop` on Linux). The shortcut runs the
app from that folder, so don't move or delete it afterwards.

## Windows exe

The `Build Windows exe` GitHub Action builds `SitePlanBuilder.exe` with PyInstaller. Run it from
the repo's **Actions** tab (*Run workflow*) and download the `SitePlanBuilder-windows` artifact, or
push a tag like `v1.0` to publish the exe on the Releases page. Put a `templates/` folder next to
the exe to preload template PDFs. Internet is still required for the frontend CDN libraries.
