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
