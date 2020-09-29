from PyQt5.QtCore import pyqtSignal, QThread
import youtube_dl
import os, sys
import re
import time

# Global variables
SAVE_PATH = os.path.expanduser('~/Downloads')

count_percent = 0
number_of_downloads = 0

number_of_downloads_ended = 0


def my_hook(d):
    global count_percent
    global number_of_downloads_ended

    print('hjhjhjhjh')
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Moooooooons Done downloading {}".format(file_tuple[1]))
        print('total dln:', number_of_downloads)

        number_of_downloads_ended += 1
        print('ended:', number_of_downloads_ended)

        if number_of_downloads_ended < number_of_downloads:
            count_percent = 0
        else:
            count_percent = 100

    if d['status'] == 'downloading':
        # print('111111', d['filename'])
        # count_percent = d['filename']
        # print('2222222', d['_percent_str'])
        # print('dddddddddddd', d['_eta_str'])
        print(d['_percent_str'])
        count_percent = int(d['_percent_str'][0:3])
        print('aquii count', count_percent)


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
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, video_id_list, dwl_choice, parent=None):
        super(DownloadData, self).__init__(parent)
        self.video_id_list = video_id_list
        self.dwl_choice = dwl_choice

        global number_of_downloads
        number_of_downloads = len(self.video_id_list)

    def run(self):
        # Download videos

        # .exe
        ffmpeg_path = "./ffmpeg/ffmpeg.exe"

        # pycharm exe
        # ffmpeg_path = ".\\ffmpeg\\ffmpeg.exe"

        # create directories
        video_directory = os.path.join(SAVE_PATH, 'yuhook_videos')

        if not os.path.isdir(video_directory):
            os.mkdir(video_directory)

        audio_directory = os.path.join(SAVE_PATH, 'yuhook_music')

        if not os.path.isdir(audio_directory):
            os.mkdir(audio_directory)

        video_path = os.path.expanduser('~\Downloads\yuhook_videos')
        audio_path = os.path.expanduser('~\Downloads\yuhook_music')

        # Only music
        if self.dwl_choice == 'Only Music':
            # self.l.setText("Downloading Music")
            with youtube_dl.YoutubeDL(ydl_audio) as ydlaudio:
                for id_video in self.video_id_list:
                    ydlaudio.download([id_video])

            # convert to webm to mp3
            arr_webm = [x for x in os.listdir(audio_path) if x.endswith(".webm") or x.endswith(".m4a")]
            print(arr_webm)

            # self.tab1.textmessage.setText('Creating MP3 files')

            for file in arr_webm:
                filename_old = file
                # filename_new_ap = re.sub(r"\s+", '_', filename_old)
                # filename_new = re.sub(r"&+", '_', filename_new_ap)

                filename_new = filename_old.replace("&", "_")

                filename_new = filename_new.replace(" ", "_")

                os.rename(audio_path + '\\' + filename_old, audio_path + '\\' + filename_new)
                print('old ', filename_old)
                print('new ', filename_new)
                # pycharm exe
                # os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                #os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # exe
                os.system(resource_path(ffmpeg_path) + ' -i ' + audio_path + '\\' + filename_new +
                          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                os.remove(audio_path + '\\' + filename_new)

        # Only video
        elif self.dwl_choice == 'Only Video':
            # self.tab1.textmessage.setText('Downloading Videos')
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                for id_video in self.video_id_list:
                    ydlvideo.download([id_video])

        else:
            # self.tab1.textmessage.setText('Downloading Videos')
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                for id_video in self.video_id_list:
                    ydlvideo.download([id_video])

            # Create audio files
            # self.tab1.textmessage.setText('Creating MP3 files')

            for file in os.listdir(video_path):
                if file.endswith(".mp4"):
                    filename = file
                    filename_new = re.sub(r"\s+", '_', filename)
                    # Rename file

                    filename_new_mp3 = filename_new[:-4] + '.mp3'

                    old_file = os.path.join(video_path, filename)

                    new_file = os.path.join(video_path, filename_new)

                    if filename_new not in os.listdir(video_path):
                        os.rename(old_file, new_file)

                    video_name = '\\' + filename_new
                    audio_name = '\\' + os.path.splitext(video_name)[0] + '.mp3'

                    print(video_name)
                    print(audio_name)

                    # Generate audio
                    # pycharm exe
                    #if filename_new_mp3 not in os.listdir(audio_path):
                    #    os.system(ffmpeg_path + ' -i ' + resource_path(video_path + video_name) +
                    #              ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

                    # .exe
                    if filename_new_mp3 not in os.listdir(audio_path):
                        os.system(resource_path(ffmpeg_path) + ' -i ' + resource_path(video_path + video_name) +
                                  ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

        self.signal.emit('Holaaaaaaa')


class Progressbar(QThread):
    signal_prgb = pyqtSignal(int)

    signal_end = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None):
        super(Progressbar, self).__init__(parent)

    def run(self):
        # Fill progress bar
        global count_percent

        cnt = 0
        while cnt < 98:
            cnt = count_percent
            time.sleep(2)
            print('count111111', count_percent)
            self.signal_prgb.emit(count_percent)

        time.sleep(1)

        self.signal_end.emit('Holaaaffffaaaa')
