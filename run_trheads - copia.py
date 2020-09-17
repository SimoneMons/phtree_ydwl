from PyQt5.QtCore import pyqtSignal, QThread
import youtube_dl
import os, sys
import re

# Global variables
SAVE_PATH = os.path.expanduser('~/Downloads')

ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'outtmpl': SAVE_PATH + '/_video/%(title)s.%(ext)s',
}

ydl_audio = {
    'format': 'bestaudio/best',
    'outtmpl': SAVE_PATH + '/_audio/%(title)s.%(ext)s',
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

    def run(self):
        # Download videos

        # .exe
        #ffmpeg_path = "./ffmpeg/ffmpeg.exe"


        # pycharm exe
        ffmpeg_path = ".\\ffmpeg\\ffmpeg.exe"

        # create directories
        video_directory = os.path.join(SAVE_PATH, '_video')

        if not os.path.isdir(video_directory):
            os.mkdir(video_directory)

        audio_directory = os.path.join(SAVE_PATH, '_audio')

        if not os.path.isdir(audio_directory):
            os.mkdir(audio_directory)

        video_path = os.path.expanduser('~\Downloads\_video')
        audio_path = os.path.expanduser('~\Downloads\_audio')

        # Only music
        if self.dwl_choice == 'Only Music':
            #self.l.setText("Downloading Music")
            with youtube_dl.YoutubeDL(ydl_audio) as ydlaudio:
                for id_video in self.video_id_list:
                    ydlaudio.download([id_video])

            # convert to webm to mp3
            arr_webm = [x for x in os.listdir(audio_path) if x.endswith(".webm") or x.endswith(".m4a")]
            print(arr_webm)

            #self.tab1.textmessage.setText('Creating MP3 files')

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
                os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # exe
                #os.system(resource_path(ffmpeg_path) + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                os.remove(audio_path + '\\' + filename_new)

        # Only video
        elif self.dwl_choice == 'Only Video':
            #self.tab1.textmessage.setText('Downloading Videos')
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                for id_video in self.video_id_list:
                    ydlvideo.download([id_video])

        else:
            #self.tab1.textmessage.setText('Downloading Videos')
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                for id_video in self.video_id_list:
                    ydlvideo.download([id_video])

            # Create audio files
            #self.tab1.textmessage.setText('Creating MP3 files')

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
                    if filename_new_mp3 not in os.listdir(audio_path):
                        os.system(ffmpeg_path + ' -i ' + resource_path(video_path + video_name) +
                                  ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

                    # .exe
                    #if filename_new_mp3 not in os.listdir(audio_path):
                    #    os.system(resource_path(ffmpeg_path) + ' -i ' + resource_path(video_path + video_name) +
                    #              ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

        self.signal.emit('Holaaaaaaa')




