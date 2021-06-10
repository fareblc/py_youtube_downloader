import os
import re
import sys


def sanitize_filename(dirty_name: str) -> str:
    s = str(dirty_name).strip().replace(' ', '_')
    file_name = re.sub(r'(?u)[^-\w.]', '', s)
    if len(file_name) > 50:
        return file_name[0:50]
    return file_name


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def check_if_dirs_exists(main_sp, video_p, music_p):
    if not os.path.exists(main_sp):
        os.makedirs(main_sp)
    if not os.path.exists(video_p):
        os.makedirs(video_p)
    if not os.path.exists(music_p):
        os.makedirs(music_p)
