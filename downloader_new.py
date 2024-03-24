import json
import youtube_dl
import writer as wt
import multiprocessing as mp
import urllib.request as req
from bs4 import BeautifulSoup
from save_directories import SaveDirectories
from core.statics import check_if_dirs_exists  # , sanitize_filename

sd = SaveDirectories()


def my_hook(d):
    if d['status'] == 'finished':
        wt.write('Done downloading, now converting ...\n')


def check_if_playlist(url: str) -> bool:
    checklist = ['list=', 'playlist=', 'playlist', 'list']
    for item in checklist:
        if item in str(url):
            return True
    return False


def get_from_playlist(url):
    dict_to_check = {}
    domain = 'https://www.youtube.com/watch?v='
    url = url.split('list=')[-1]

    list_url = 'https://www.youtube.com/playlist?list=' + url

    html_page = req.urlopen(list_url)

    soup = BeautifulSoup(html_page, 'html.parser')

    res = soup.find_all('script')

    for item in res:
        if 'var ytInitialData' in str(item):
            a = str(item).split('var ytInitialData = ')[-1]
            b = str(a).split(';</script>')[0]
            new = json.loads(b)
            dict_to_check = new["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]['contents'][0]['itemSectionRenderer']['contents'][0][
                'playlistVideoListRenderer']['contents']

    list_url = [domain + str(f['playlistVideoRenderer']['videoId']) for f in dict_to_check]

    # print(list_url)
    return list_url


def get_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{sd.vid_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'extractor_retries': 'auto',
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        vid = ydl.extract_info(url, download=False)
        print(str(vid['title']))
        wt.write(str('-----\nDownloading %s\n' % str(vid['title'])))
        ydl.download([url])
        print(str(vid['title']))
        wt.write('Finished downloading %s\n-----\n' % str(vid['title']))


def get_audio(url):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{sd.music_path}/%(title)s.mp3',
        'noplaylist': True,
        'extractor_retries': 'auto',
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        vid = ydl.extract_info(url, download=False)
        print(str(vid['title']))
        wt.write(str('-----\nDownloading %s\n' % str(vid['title'])))
        ydl.download([url])
        print(str(vid['title']))
        wt.write('Finished downloading %s\n-----\n' % str(vid['title']))


def download_chooser(download_url: str, audio_only=True):
    callback = get_audio if audio_only else get_video
    check_if_dirs_exists(main_sp=sd.main_path, video_p=sd.vid_path, music_p=sd.music_path)
    if check_if_playlist(download_url):
        url_list = get_from_playlist(download_url)

        with mp.Pool(mp.cpu_count() // 2) as pool:
            pool.map(callback, url_list)
    else:
        callback(download_url)
    wt.write(str('FINISHED!!!\n'))
