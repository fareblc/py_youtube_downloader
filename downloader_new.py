import writer as wt
from core.statics import check_if_dirs_exists  # , sanitize_filename
from save_directories import SaveDirectories
from bs4 import BeautifulSoup
import urllib.request as req
import json
import youtube_dl

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
    # obj = pt.YouTube(url)
    # videos = obj.streams

    # if len(videos) == 0:
    #     wt.write("No streams available for video with url %s\n" % url)
    #     return

    # vid = videos.get_by_itag(22) if videos.get_by_itag(22) is not None else videos.first()

    # vid_title = sanitize_filename(vid.title)

    # wt.write(str('Downloading %s\n' % str(vid_title)))

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{sd.vid_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        vid = ydl.extract_info(url, download=False)
        print(str(vid['title']))
        wt.write(str('-----\nDownloading %s\n' % str(vid['title'])))
        ydl.download([url])
        print(str(vid['title']))
        wt.write('Finished downloading %s\n-----\n' % str(vid['title']))

    # vid.download(filename=vid_title, output_path=sd.vid_path)

    # wt.write('Finished downloading %s\n' % str(vid_title))


def get_audio(url):
    # obj = pt.YouTube(url).streams
    #
    # if len(obj) == 0:
    #     wt.write("No streams available for video with url %s\n" % url)
    #     return
    #
    # audio_track = obj.filter(only_audio=True).first()
    #
    # audio_title = sanitize_filename(audio_track.title)
    #
    # wt.write(str('Downloading {}\n'.format(str(audio_title))))
    #
    # audio_track.download(filename=audio_title, output_path=sd.music_path, get_mp3=True)
    #
    # wt.write(str('Finished downloading %s\n' % str(audio_title)))

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{sd.music_path}/%(title)s.mp3',
        'noplaylist': True,
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
        for url in url_list:
            callback(url)
    else:
        callback(download_url)
    wt.write(str('FINISHED!!!\n'))


# if __name__ == "__main__":
#     get_video('https://www.youtube.com/watch?v=Io0fBr1XBUA')
#     get_audio('https://www.youtube.com/watch?v=Io0fBr1XBUA')
# download_chooser("https://www.youtube.com/playlist?list=PLynhp4cZEpTbRs_PYISQ8v_uwO0_mDg_X", True)
# play_list = pt.Playlist("https://www.youtube.com/watch?v=nYh-n7EOtMA&list=PLH0MZrlBewkDYjPMbsVcvhSKdprZZ48IO")
# play_list._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
# play_list2 = get_from_playlist(
# "https://www.youtube.com/watch?v=nYh-n7EOtMA&list=PLH0MZrlBewkDYjPMbsVcvhSKdprZZ48IO")
# getPlaylistLinks("https://www.youtube.com/watch?v=nYh-n7EOtMA&list=PLH0MZrlBewkDYjPMbsVcvhSKdprZZ48IO")

# url_list = get_from_playlist(
# 'https://www.youtube.com/watch?v=Io0fBr1XBUA&list=PLH0MZrlBewkBYSYoQKqMk2MPfI81yeZ1c')
# print(play_list2)
# for video in play_list.videos:
#     print(video)
