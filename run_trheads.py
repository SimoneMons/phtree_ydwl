from PyQt5.QtCore import pyqtSignal, QThread
import youtube_dl
import os

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

class DownloadVideo(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, dwl_link, parent=None):
        super(DownloadVideo, self).__init__(parent)
        self.dwl_link = dwl_link


    def run(self):
        # Download video
        with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
            ydlvideo.download([self.dwl_link])

        self.signal.emit('Holaaaaaaa')



