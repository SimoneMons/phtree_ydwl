import os
import sys
import time

import youtube_dl
from PyQt5.QtCore import pyqtSignal, QThread
from validate_link import validate_link

# Global variables
SAVE_PATH = os.path.expanduser('~/Downloads')

count_percent = 0
number_of_downloads = 0
number_of_downloads_ended = 0
number_of_not_valid_videos = 0


def my_hook(d):
    global count_percent
    global number_of_downloads_ended
    global number_of_not_valid_videos

    print('hjhjhjhjh')
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        #print("Moooooooons Done downloading {}".format(file_tuple[1]))
        #print('total dln:', number_of_downloads)

        number_of_downloads_ended += 1
        print('number of download ended:', number_of_downloads_ended)
        print('number of not valid videos:', number_of_not_valid_videos)
        print('number of total downloads:', number_of_downloads)

        if number_of_downloads_ended + number_of_not_valid_videos < number_of_downloads:
            count_percent = 0
        else:
            count_percent = 100

        print('finished', count_percent)

    if d['status'] == 'downloading':
        # print('111111', d['filename'])
        # count_percent = d['filename']
        # print('2222222', d['_percent_str'])
        # print('dddddddddddd', d['_eta_str'])
        print(d['_percent_str'])
        count_percent = int(d['_percent_str'][0:3])
        print('count downloading', count_percent)


ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_PATH + '/yuhook_videos/%(title)s.%(ext)s',
}

ydl_audio = {
    'format': 'bestaudio/best',
    'progress_hooks': [my_hook],
    'outtmpl': SAVE_PATH + '/yuhook_music/%(title)s.%(ext)s',
}


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        print(' ')
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("venv"), relative_path)


class DownloadData(QThread):
    signal_end_download = pyqtSignal('PyQt_PyObject')

    signal_num_video_dwnld = pyqtSignal(int, int)

    signal_num_mp3_created = pyqtSignal(int, int)

    def __init__(self, video_id_list, dwl_choice, parent=None):
        super(DownloadData, self).__init__(parent)
        self.video_id_list = video_id_list
        self.dwl_choice = dwl_choice

        global number_of_downloads
        number_of_downloads = len(self.video_id_list)

    def run(self):
        global number_of_not_valid_videos
        number_of_not_valid_videos = 0

        # .exe
        ffmpeg_path = "./ffmpeg/ffmpeg.exe"

        # pycharm exe
        #ffmpeg_path = ".\\ffmpeg\\ffmpeg.exe"

        # create directories
        video_directory = os.path.join(SAVE_PATH, 'yuhook_videos')

        if not os.path.isdir(video_directory):
            os.mkdir(video_directory)

        audio_directory = os.path.join(SAVE_PATH, 'yuhook_music')

        if not os.path.isdir(audio_directory):
            os.mkdir(audio_directory)

        video_path = os.path.expanduser('~\Downloads\yuhook_videos')
        audio_path = os.path.expanduser('~\Downloads\yuhook_music')

        # print('simone111111111111111', self.video_id_list)

        # Only music
        if self.dwl_choice == 'Only Music':
            count_videos = 0
            with youtube_dl.YoutubeDL(ydl_audio) as ydlaudio:
                for id_video in self.video_id_list:
                    if validate_link(id_video) == 0:
                        count_videos += 1
                        self.signal_num_video_dwnld.emit(count_videos, len(self.video_id_list))
                        time.sleep(1)
                        ydlaudio.download([id_video])
                    else:
                        number_of_not_valid_videos += 1
                        pass

            # convert webm to mp3
            arr_webm = [x for x in os.listdir(audio_path) if x.endswith(".webm") or x.endswith(".m4a")]
            print(arr_webm)

            # self.tab1.textmessage.setText('Creating MP3 files')

            count_mp3 = 0
            for file in arr_webm:
                filename_old = file
                # filename_new_ap = re.sub(r"\s+", '_', filename_old)
                # filename_new = re.sub(r"&+", '_', filename_new_ap)

                filename_new = filename_old.replace("&", "_")

                filename_new = filename_new.replace(" ", "_")

                filename_new = filename_new.replace("•", "_")

                os.rename(audio_path + '\\' + filename_old, audio_path + '\\' + filename_new)
                print('old ', filename_old)
                print('new ', filename_new)
                # pycharm exe
                #os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # exe
                os.system(resource_path(ffmpeg_path) + ' -i ' + audio_path + '\\' + filename_new +
                          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                os.remove(audio_path + '\\' + filename_new)
                count_mp3 += 1
                self.signal_num_mp3_created.emit(count_mp3, len(arr_webm))

        # Only video
        elif self.dwl_choice == 'Only Video':
            count_videos_ov = 0
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                for id_video in self.video_id_list:
                    if validate_link(id_video) == 0:
                        count_videos_ov += 1
                        self.signal_num_video_dwnld.emit(count_videos_ov, len(self.video_id_list))
                        ydlvideo.download([id_video])
                    else:
                        number_of_not_valid_videos += 1
                        pass

        # Music & Video
        else:
            # Downloading Video
            count_videos_mv = 0
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                for id_video in self.video_id_list:
                    valid_id = validate_link(id_video)
                    if valid_id == 0:
                        print('Video available:', id_video)
                        count_videos_mv += 1
                        self.signal_num_video_dwnld.emit(count_videos_mv, len(self.video_id_list))
                        ydlvideo.download([id_video])
                    else:
                        print('Video not available aaaaa: ', id_video)
                        number_of_not_valid_videos += 1
                        print('numer not valid', number_of_not_valid_videos)
                        pass

            # Downloading Music
            with youtube_dl.YoutubeDL(ydl_audio) as ydlaudio:
                for id_video in self.video_id_list:
                    valid_id = validate_link(id_video)
                    if valid_id == 0:
                        print('Video available:', id_video)
                        ydlaudio.download([id_video])
                    else:
                        print('Video not available: ', id_video)
                        number_of_not_valid_videos += 1
                        pass

            # Convert webm to mp3
            arr_webm = [x for x in os.listdir(audio_path) if x.endswith(".webm") or x.endswith(".m4a")]

            count_mp3_mv = 0
            for file in arr_webm:
                filename_old = file
                # filename_new_ap = re.sub(r"\s+", '_', filename_old)
                # filename_new = re.sub(r"&+", '_', filename_new_ap)

                filename_new = filename_old.replace("&", "_")

                filename_new = filename_new.replace(" ", "_")

                filename_new = filename_new.replace("•", "_")

                os.rename(audio_path + '\\' + filename_old, audio_path + '\\' + filename_new)
                print('old ', filename_old)
                print('new ', filename_new)
                # pycharm exe
                #os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # exe
                os.system(resource_path(ffmpeg_path) + ' -i ' + audio_path + '\\' + filename_new +
                          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                os.remove(audio_path + '\\' + filename_new)
                count_mp3_mv += 1
                self.signal_num_mp3_created.emit(count_mp3_mv, len(arr_webm))


        self.signal_end_download.emit('Downloadcompleted')


class Progressbar(QThread):
    signal_prgb = pyqtSignal(int)
    signal_prgb_end = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Progressbar, self).__init__(parent)

    def run(self):
        # Fill progress bar
        global count_percent
        global number_of_downloads
        global number_of_downloads_ended

        while number_of_downloads_ended < number_of_downloads:
            print('count111111 inside prgb', number_of_downloads_ended)
            print('hhhhh', number_of_downloads)
            print('percetn to prb', count_percent)
            self.signal_prgb.emit(count_percent)
            time.sleep(0.5)

        val_end = 0
        self.signal_prgb_end.emit(val_end)
