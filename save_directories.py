import os
import writer as wt
from pathlib import Path
from core.singleton import Singleton


class SaveDirectories(metaclass=Singleton):

    main_path: str
    vid_path: str
    music_path: str

    def __init__(self):
        self.check_save_file()
        self.main_path = self.get_main_path() + '/Youtube_Downloader'
        self.vid_path = self.main_path + '/Videos/'
        self.music_path = self.main_path + '/Music/'

    def get_main_path(self) -> str:
        path = wt.read('./save_path.txt')
        if os.path.exists(path):
            return path
        wt.clear(file_name='./save_path.txt')
        self.check_save_file()
        return str(Path.home() / 'Documents')

    def path_refresh(self):
        self.main_path = self.get_main_path() + '/Youtube_Downloader'
        self.vid_path = self.main_path + '/Videos/'
        self.music_path = self.main_path + '/Music/'

    def check_save_file(self):
        if not wt.check_if_file_has_data('./save_path.txt'):
            path = str(Path.home() / 'Documents')
            wt.write(msg=path, file_name='./save_path.txt')
