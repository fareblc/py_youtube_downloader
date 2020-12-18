# from pytube import YouTube, Playlist
# # from pytubemp3 import YouTube as YT_mp3
# # from moviepy.audio.io.AudioFileClip import AudioFileClip
# # import ffmpeg
# # import tempfile
# # from pytubemp3.exceptions import RegexMatchError, HTMLParseError, LiveStreamError
# import os
# import re
# from pathlib import Path
# # from core.eventbus import EventBus
# import writer as wt
# import sys
# # import subprocess
#
# # event_bus = EventBus()
#
#
# class Downloader(object):
#     url: str
#     list_url: str
#     is_audio_only: bool
#     main_save_path: str
#     video_path: str
#     music_path: str
#     _is_running: bool
#
#     def __init__(self):
#         self._is_running = False
#         self.main_save_path = str(Path.home() / 'Documents') + '/Youtube_Downloader'
#         self.video_path = self.main_save_path + '/Videos/'
#         self.music_path = self.main_save_path + '/Music/'
#         self._check_if_dirs_exists()
#         # sys.stdout = tempfile.TemporaryFile()
#
#     def _check_if_dirs_exists(self):
#         if not os.path.exists(self.main_save_path):
#             os.makedirs(self.main_save_path)
#         if not os.path.exists(self.video_path):
#             os.makedirs(self.video_path)
#         if not os.path.exists(self.music_path):
#             os.makedirs(self.music_path)
#
#     def check_if_playlist(self, url: str) -> bool:
#         checklist = ['list=', 'playlist=', 'playlist', 'list']
#         for item in checklist:
#             if item in str(url):
#                 return True
#         return False
#
#     def get_video(self):
#         obj = YouTube(self.url)
#         videos = obj.streams
#         vid = videos.get_by_itag(22) if videos.get_by_itag(22) is not None else videos.first()
#         vid_title = self._sanitize_filename(vid.title)
#         # sys.stdout.write(str('Downloading %s\n' % str(vid_title)))
#         # sys.stdout.flush()
#         wt.write(str('Downloading %s\n' % str(vid_title)))
#         vid.download(filename=vid_title, output_path=self.video_path)
#         # sys.stdout.write('Finished downloading %s\n' % str(vid_title))
#         # sys.stdout.flush()
#         wt.write('Finished downloading %s\n' % str(vid_title))
#
#     # def get_audio(self):
#     #     # audio_track = pytube.YouTube(self.url).streams.filter(only_audio=True).first()
#     #     audio_track = YT_mp3(self.url).streams.filter(only_audio=True).first()
#     #     audio_title = self._sanitize_filename(audio_track.title)
#     #     if len(audio_title) > 50:
#     #         audio_title = audio_title[0:50]
#     #     # sys.stdout.write(str('Downloading {0}\n'.format(str(audio_title))))
#     #     # sys.stdout.flush()
#     #     wt.write(str('Downloading {0}\n'.format(str(audio_title))))
#     #     audio_track.download(filename=audio_title, output_path=self.music_path)
#     #     # sys.stdout.write(str('Finished downloading %s\n' % str(audio_title)))
#     #     # sys.stdout.flush()
#     #     # clip = AudioFileClip(f'{self.music_path}/{audio_title}.mp4')
#     #     # clip.write_audiofile(f'{self.music_path}/{audio_title}.mp3', logger=None)
#     #     # clip.close()
#     #     # os.remove(f'{self.music_path}/{audio_title}.mp4')
#     #     wt.write(str('Finished downloading %s\n' % str(audio_title)))
#     #     # mp4 = f'{self.music_path}/{audio_title}.mp4'
#     #     # mp3 = f'{self.music_path}/{audio_title}.mp3'
#     #     # ffmpeg2 = ('ffmpeg -i %s %s ' % (mp4, mp3))
#     #     # inp = ffmpeg.input(mp4)
#     #     # audio = inp.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
#     #     # ffmpeg.output(audio, 'out.mp3', f="mp3").run()
#     #
#     #     # subprocess.check_output(ffmpeg2, shell=True)
#     #     # os.remove(f'{self.music_path}/{audio_title}.mp4')
#
#     def get_from_playlist(self):
#         download_asset = 'videos' if not self.is_audio_only else 'tracks'
#         play_list = Playlist(self.list_url)
#         play_list_title = self._sanitize_filename(play_list.title)
#         # sys.stdout.write('Started downloading %s %s from playlist --%s--\n' % (
#         #     str(int(len(play_list.video_urls))), str(download_asset), str(play_list_title)))
#         # sys.stdout.flush()
#         wt.write('Started downloading %s %s from playlist --%s--\n' % (
#             str(int(len(play_list.video_urls))), str(download_asset), str(play_list_title)))
#         for vid_url in play_list.video_urls:
#             self.url = vid_url
#             if self.is_audio_only:
#                 # self.get_audio()
#                 pass
#             elif not self.is_audio_only:
#                 self.get_video()
#         # sys.stdout.write(
#         #     f'\nAll {str(int(len(play_list.video_urls)))} {str(download_asset)} from playlist --'
#         #     f'{str(play_list_title)}-- have been downloaded in directory {str(self.main_save_path)}\n')
#         # sys.stdout.flush()
#         wt.write(
#             f'\nAll {str(int(len(play_list.video_urls)))} {str(download_asset)} from playlist --'
#             f'{str(play_list_title)}-- have been downloaded in directory {str(self.main_save_path)}\n')
#
#     def choose_video_or_audio(self):
#         if self.is_audio_only:
#             # self.get_audio()
#             pass
#         else:
#             self.get_video()
#
#     def download_chooser(self, url: str, is_audio_only: bool):
#         self._is_running = True
#         self.is_audio_only = is_audio_only
#         flag = self.check_if_playlist(url)
#         if flag:
#             try:
#                 self.list_url = url
#                 self.get_from_playlist()
#             except Exception as e:
#                 print(e)
#                 # sys.stdout.write(str(e) + '\n')
#                 # sys.stdout.flush()
#                 # sys.stdout.write(
#                 #     'Please make sure your internet connection is working and/or make sure your URL is valid\n')
#                 # sys.stdout.flush()
#                 wt.write(str(e) + '\n')
#                 wt.write(
#                     'Please make sure your internet connection is working and/or make sure your URL is valid\n')
#             # event_bus = EventBus()
#             # event_bus.trigger('toggle_on', 'Toggle-On')
#
#         else:
#             try:
#                 self.url = url
#                 self.choose_video_or_audio()
#             except Exception as e:
#                 print(e)
#                 # sys.stdout.write(str(e) + '\n')
#                 # sys.stdout.flush()
#                 # print(str(e))
#                 # sys.stdout.write(
#                 #     'Please make sure your internet connection is working and/or  make sure your URL is valid\n')
#                 # sys.stdout.flush()
#                 wt.write(str(e) + '\n')
#                 wt.write(
#                     'Please make sure your internet connection is working and/or  make sure your URL is valid\n')
#         # event_bus.trigger('toggle_on', 'Toggle-On')
#         self._is_running = False
#
#     def _sanitize_filename(self, dirty_name: str) -> str:
#         s = str(dirty_name).strip().replace(' ', '_')
#         return re.sub(r'(?u)[^-\w.]', '', s)
#
#     @property
#     def is_running(self):
#         return self._is_running
#
#
# def main():
#     # download_chooser(sys.argv[1], is_audio_only=bool(int(sys.argv[2])))
#     dow = Downloader()
#     # dow.download_chooser('https://www.youtube.com/watch?v=YqNVhJPhsN8',
#     #                      is_audio_only=True)
#
#     dow.download_chooser('https://www.youtube.com/playlist?list=PLH0MZrlBewkDYjPMbsVcvhSKdprZZ48IO', is_audio_only=False)
#
#
# if __name__ == '__main__':
#     main()
