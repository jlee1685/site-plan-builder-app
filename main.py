"""Turner HSEP Safety Inscriber / Site Plan Builder (pywebview + React)."""
import base64
import os

import webview

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _dialog_type(name):
    enum = getattr(webview, "FileDialog", None)
    if enum is not None and hasattr(enum, name):
        return getattr(enum, name)
    return getattr(webview, name + "_DIALOG")


class Api:
    def list_templates(self):
        found = []
        for folder in (BASE_DIR, os.path.join(BASE_DIR, "templates")):
            if not os.path.isdir(folder):
                continue
            for name in sorted(os.listdir(folder)):
                if name.lower().endswith(".pdf"):
                    found.append({"name": name, "path": os.path.join(folder, name)})
        return found

    def read_pdf(self, path):
        try:
            with open(path, "rb") as f:
                return {"ok": True, "data": base64.b64encode(f.read()).decode("ascii")}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc)}

    def open_dialog(self):
        try:
            res = webview.windows[0].create_file_dialog(
                _dialog_type("OPEN"), allow_multiple=True,
                file_types=("PDF Files (*.pdf)",))
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "files": []}
        files = [{"name": os.path.basename(p), "path": p} for p in (res or [])]
        return {"ok": True, "files": files}

    def save_dialog(self, b64, suggested):
        try:
            res = webview.windows[0].create_file_dialog(
                _dialog_type("SAVE"), save_filename=suggested,
                file_types=("PDF Files (*.pdf)",))
            if not res:
                return {"ok": False, "cancelled": True}
            path = res if isinstance(res, str) else res[0]
            if not path.lower().endswith(".pdf"):
                path += ".pdf"
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
            return {"ok": True, "path": path}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc)}


with open(os.path.join(BASE_DIR, "web", "index.html"), encoding="utf-8") as _f:
    HTML = _f.read()


def main():
    api = Api()
    webview.create_window(
        "Turner HSEP Safety Inscriber", html=HTML, js_api=api, width=1280, height=900)
    webview.start()


if __name__ == "__main__":
    main()
