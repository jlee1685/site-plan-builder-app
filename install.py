"""Install Site Plan Builder dependencies and create a Desktop shortcut.

Usage: python install.py
Run it from a downloaded/cloned copy of the repo; the app runs from this folder.
"""
import os
import platform
import stat
import subprocess
import sys

APP_NAME = "Site Plan Builder"
BASE = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(BASE, ".venv")


def desktop_dir():
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "[Environment]::GetFolderPath('Desktop')"],
                capture_output=True, text=True, check=True).stdout.strip()
            if out:
                return out
        except Exception:
            pass
    d = os.path.join(home, "Desktop")
    return d if os.path.isdir(d) else home


def venv_python(windowed=False):
    if platform.system() == "Windows":
        return os.path.join(VENV, "Scripts", "pythonw.exe" if windowed else "python.exe")
    return os.path.join(VENV, "bin", "python")


def make_shortcut():
    desk = desktop_dir()
    main = os.path.join(BASE, "main.py")
    system = platform.system()
    if system == "Windows":
        path = os.path.join(desk, APP_NAME + ".lnk")
        ps = (
            "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%s');"
            "$s.TargetPath='%s';$s.Arguments='\"%s\"';$s.WorkingDirectory='%s';$s.Save()"
            % (path, venv_python(True), main, BASE)
        ).replace("'%s'" % path, "'%s'" % path)
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    elif system == "Darwin":
        path = os.path.join(desk, APP_NAME + ".command")
        with open(path, "w") as f:
            f.write('#!/bin/bash\ncd "%s"\nexec "%s" "%s"\n' % (BASE, venv_python(), main))
        os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    else:
        path = os.path.join(desk, APP_NAME + ".desktop")
        with open(path, "w") as f:
            f.write("[Desktop Entry]\nType=Application\nName=%s\nExec=\"%s\" \"%s\"\n"
                    "Path=%s\nTerminal=false\nCategories=Office;\n"
                    % (APP_NAME, venv_python(), main, BASE))
        os.chmod(path, 0o755)
    return path


def main():
    if sys.version_info < (3, 9):
        sys.exit("Python 3.9+ is required.")
    if not os.path.isdir(VENV):
        subprocess.check_call([sys.executable, "-m", "venv", VENV])
    subprocess.check_call([venv_python(), "-m", "pip", "install", "-r",
                           os.path.join(BASE, "requirements.txt")])
    print("Desktop shortcut created:", make_shortcut())


if __name__ == "__main__":
    main()
