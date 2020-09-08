import time
import youtube_dl
from PyQt5.QtCore import QThread, pyqtSignal

import main_ydwl_lv1


ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'outtmpl': main_ydwl_lv1.SAVE_PATH + '/_video/%(title)s.%(ext)s',
}

class Showbar(QThread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    aaaa = pyqtSignal(str)

    bbbb = pyqtSignal(str)


    def run(self):
        count = 0
        filesize_list = []

        with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
            result = ydlvideo.extract_info(self.name, download=False)
            print(result)
            for key in result:
                if key == 'formats':
                    for i in range(0, len(key)):
                        filesize_list.append(result[key][i]['filesize'])

        filesize = max(filesize_list)

        print(filesize)

        rate = 12

        dwl_time = int(((filesize / 1000000) / rate) * 1.5)

        time_sleep = int((dwl_time / 10) + 1)

        print('Time sleep', time_sleep)

        time_limit = 100
        while count < time_limit:
            count += 10
            msg = "Downloading File"
            #self.counter = count
            time.sleep(time_sleep)
            self.countChanged.emit(count)
            self.aaaa.emit(msg)

        time.sleep(1)
        msg = 'Creating file'
        self.bbbb.emit(msg)